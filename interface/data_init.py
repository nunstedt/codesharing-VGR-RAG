"""Data initialization and setup functionality."""

import os
import time
from contextlib import redirect_stdout
from ingest import parse_and_get_nodes
from index import get_vector_index
from config import get_data_directory


# For debugging purposes
from IPython import embed


def initialize_data_and_index(data_dir: str = None, verbose: bool = True):
    """Initialize data parsing and vector index creation."""
    if data_dir is None:
        data_dir = get_data_directory()
    
    total_start = time.time()
    
    if verbose:
        print("[TIMER] Starting parse_and_get_nodes...")
    
    parse_start = time.time()
    
    # Optionally suppress noisy output from parsing
    if verbose:
        data = parse_and_get_nodes(data_dir)
    else:
        with open(os.devnull, "w") as f, redirect_stdout(f):
            data = parse_and_get_nodes(data_dir)
    
    parse_time = time.time() - parse_start
    if verbose:
        print(f"[TIMER] parse_and_get_nodes took {parse_time:.2f} seconds.")
    

    # print("[INFO] Hacky solution to include supplementary AI material in meta filtering")
    # metadata_start = time.time()
    # for node in data:
    #     title = node.metadata.get("pdf_title", "")
        
    #     if title == "Commission Guidelines on AI Prohibitions":
    #         node.metadata["pdf_title"] = "EU AI Act"
    #     elif title == "High Level Summary of the AI Act":
    #         node.metadata["pdf_title"] = "EU AI Act"        
    
    # metadata_time = time.time() - metadata_start
    # if verbose:
    #     print(f"[TIMER] Metadata processing took {metadata_time:.2f} seconds.")
    
    
    # embed()  # For debugging purposes, can be removed in production


    # Creating database
    index_start = time.time()
    DBclient, collection_name, vector_index = get_vector_index(data)
    index_time = time.time() - index_start
    count = DBclient.count(collection_name=collection_name).count
    print(f"[INFO] Number of chunks in '{collection_name}': {count}")
    
    if verbose:
        print(f"[TIMER] get_vector_index took {index_time:.2f} seconds")
        print(f"[TIMER] Total initialization took {time.time() - total_start:.2f} seconds")
    
    return DBclient, collection_name, vector_index
