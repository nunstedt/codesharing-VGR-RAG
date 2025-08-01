from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    Settings
)
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import qdrant_client
from typing import Any, Tuple, List

from ingest import parse_and_get_nodes
from reranker import TEIReranker
from llama_index.embeddings.text_embeddings_inference import TextEmbeddingsInference
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters, FilterOperator
import requests

# # set up embedding model to use Docker embeddor
# Settings.embed_model = TextEmbeddingsInference(
#     #Use fine-tuned model
#     #model_name = "trained_embeddings"

#     #Use exported ONNX model
#     #model_name="export_models",

#     #Use default embedding model
#     model_name="sentence-transformers/all-MiniLM-L6-v2",
#     # model_name="intfloat/multilingual-e5-large-instruct",
#     base_url="http://localhost:5080"
# )
# # # Disabled for retrieval demonstration



# set up embedding model to use Docker embeddor
Settings.embed_model = TextEmbeddingsInference(
    model_name="/data",  # must match MODEL_ID in docker-compose
    base_url="http://localhost:5080",
    timeout=180  # or more
    )

# set up reranker to use local inference reranker
reranker = TEIReranker(model_name="Alibaba-NLP/gte-multilingual-reranker-base")
# reranker = TEIReranker("Alibaba-NLP/gte-multilingual-reranker-base")
# reranker = TEIReranker(model_name="BAAI/bge-reranker-base") # Not multilingual, but works for English

def create_qdrant_client(storage_path: str = None) -> qdrant_client.QdrantClient:
    """
    Create and return a Qdrant client for Docker Qdrant.

    Args:
        storage_path (str): Path to the Qdrant database directory.

    Returns:
        qdrant_client.QdrantClient: The Qdrant client instance.
    """
    return qdrant_client.QdrantClient(host="localhost", port=6333)

def create_db_collection(
        client: qdrant_client.QdrantClient, 
        name: str = 'MyCoolVectorStore'
        ) -> Tuple[QdrantVectorStore, str]:
    """
    Create a Qdrant vector store collection.

    Args:
        client (qdrant_client.QdrantClient): The Qdrant client.
        name (str): Name of the collection.

    Returns:
        Tuple[QdrantVectorStore, str]: The vector store and collection name.
    """
    return QdrantVectorStore(client=client, collection_name=name), name

def setup_storage(vector_store: QdrantVectorStore) -> StorageContext:
    """
    Set up the storage context for the vector store.

    Args:
        vector_store (QdrantVectorStore): The vector store.

    Returns:
        StorageContext: The storage context.
    """
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return storage_context

def fill_vectordb(
        data: List[Any], 
        storage_context: StorageContext
        ) -> VectorStoreIndex:
    """
    Fill the vector database with nodes.

    Args:
        data (List[Any]): List of nodes to insert.
        storage_context (StorageContext): The storage context.

    Returns:
        VectorStoreIndex: The vector store index.
    """
    return VectorStoreIndex(
        nodes=data,
        storage_context=storage_context,
    )

def get_vector_index(initial_data: List[Any]) -> Tuple[qdrant_client.QdrantClient, str, VectorStoreIndex]:
    """
    Create a Qdrant client, vector store, and fill the vector database with initial data if needed.
    Also prints whether a new DB is created or an existing one is used, and times each step.
    """
    import time
    start_total = time.time()
    client = create_qdrant_client()
    collection_name = "MyCoolVectorStore"
    # Check if collection exists
    collections = [c.name for c in client.get_collections().collections]
    vector_store, _ = create_db_collection(client, name=collection_name)
    storage_context = setup_storage(vector_store)
    if collection_name not in collections:
        print(f"[INFO] Collection '{collection_name}' does not exist. Creating and filling new vector DB...")
        start_fill = time.time()
        vector_index = fill_vectordb(initial_data, storage_context)
        print(f"[INFO] Vector DB created and filled in {time.time() - start_fill:.2f} seconds.")
    else:
        print(f"[INFO] Collection '{collection_name}' already exists. Connecting to existing vector DB...")
        start_connect = time.time()
        vector_index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)
        print(f"[INFO] Connected to existing vector DB in {time.time() - start_connect:.2f} seconds.")
    print(f"[INFO] get_vector_index total time: {time.time() - start_total:.2f} seconds.")
    return client, collection_name, vector_index

def get_query_engine(vector_index: VectorStoreIndex, filtering: MetadataFilters = None) -> Any:
    """
    Get a query engine from the vector store index, with reranker and similarity cutoff.
    """
    # print(filters)

    # ----------------- Testing different response synthesizers and postprocessors ---------------------
  
    return vector_index.as_query_engine(filters=filtering,
        similarity_top_k=20,  
        node_postprocessors=[
            reranker
            # SimilarityPostprocessor(similarity_cutoff=0.6)  # adjust cutoff as needed
        ]
    )

# ----------------- Testing different response synthesizers and postprocessors ---------------------

    # return vector_index.as_query_engine(response_mode="refine") # info about response modes: https://docs.llamaindex.ai/en/stable/module_guides/querying/response_synthesizers/

    # return vector_index.as_query_engine(
    #         similarity_top_k=10)

    # return vector_index.as_query_engine(
    #         similarity_top_k=10,
    #         node_postprocessors=[
    #             # add reranker and other stuff here
    #             SimilarityPostprocessor(similarity_cutoff=0.5)]
    #     )
     
            
    # return vector_index.as_query_engine(
    #         similarity_top_k=10,
    #         node_postprocessors=[
    #             # add reranker and other stuff here
    #             SimilarityPostprocessor(similarity_cutoff=0.5),
    #             reranker
    #         ]
    #     )

        # return vector_index.as_query_engine(
    #         similarity_top_k=10,
    #         node_postprocessors=[
    #             # add reranker and other stuff here
    #             SimilarityPostprocessor(similarity_cutoff=0.5),
    #             reranker
    #         ]
    #     )

if __name__ == '__main__':
    """
    Main execution block:
    - Initializes Qdrant client and vector store.
    - Loads and inserts nodes into the vector database.
    - Prints the number of vectors before and after insertion.
    - Retrieves and prints results for a sample query.
    - Deletes the collection after use.
    """
    client = create_qdrant_client()
    vector_store, collection_name = create_db_collection(client)
    storage_context = setup_storage(vector_store)

    data: List[Any] = parse_and_get_nodes('data/')
    initial_data: List[Any] = data[:50]

    # create initial vector database
    vector_index: VectorStoreIndex = fill_vectordb(initial_data, storage_context)
    
    num_vectors: int = client.count(
        collection_name=collection_name,
        exact=True # Use exact=True for a precise number
    ).count
    print('Initial vectors/nodes in DB:', num_vectors)

    # test that we can add more data
    additional_data: List[Any] = data[50:]
    print(f'Adding {len(additional_data)} nodes')
    vector_index.insert_nodes(additional_data)

    num_vectors = client.count(
        collection_name=collection_name,
        exact=True # Use exact=True for a precise number
    ).count
    print('Updated vectors/nodes in DB:', num_vectors)

    query_engine = get_query_engine(vector_index)
    results = query_engine.retrieve('did parlament write this document?')

    for i, r in enumerate(results):
        print(f'\nResult {i}:')
        print(r)

    # client.delete_collection(collection_name)