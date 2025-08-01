# Running docker services

Commands are specified in the `Makefile`

To run services:

```sh
make up
```

To end services:

```sh
make down
```

Locations of docker services can be found in the `ports` field for each service. 

# docker-compose file

Setup to run with GPU, think you can just remove the GPU parts to run it all on cpu.

You can select models and so on under the `-command` line for the services.

# Getting stuff from services

Setting up embedding model/reranker (url is just `localhost:PORT`):

```sh
    embeddor = TextEmbeddingsInference(
        EMBEDDING_MODEL,
        base_url=EMBEDDING_URL,
        text_instruction="",  # Instructions for intfloat/multilingual-e5-instruct for retrieval
        query_instruction=QUERY_PREFIX,
        auth_token=AUTH_TOKEN,
        embed_batch_size=BATCH_SIZE,
    )
    Settings.embed_model = embeddor
    reranker = TEIReranker(RERANKER_URL)
```

Reranker TEI implementation from `reranker.py`

Setting up vector database:

```sh
    distance_metric = Distance.COSINE

    client = qc.QdrantClient(QDRANT_URL, timeout=60)
    vector_store = QdrantVectorStore(client=client,
                                     collection_name='test',
                                     vectors_config=VectorParams(size=vector_size, 
                                                                 distance=distance_metric),
                                     batch_size=batch_size)
```

