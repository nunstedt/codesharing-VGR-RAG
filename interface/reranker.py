from llama_index.core.schema import MetadataMode, NodeWithScore
import requests  # type: ignore
from IPython import embed
import time

import logging

logger = logging.getLogger(__name__)


class TEIReranker:
    def __init__(self, url: str) -> None:
        self.url = url

    def rerank(
        self,
        query: str,
        nodes: list[NodeWithScore],
        top_k: int = 10,
        truncate: bool = True,
        metadata_mode: MetadataMode = MetadataMode.EMBED,
    ) -> list[NodeWithScore]:
        if not nodes:
            return []

        payload = {
            "query": query,
            "texts": [node.get_content(metadata_mode) for node in nodes],
            "truncate": truncate,
        }

        try:
            response = requests.post(f"{self.url}/rerank", json=payload, timeout=30)
        except requests.Timeout as exc:
            logger.exception(str(exc))
            raise ValueError("Reranker request timed out") from exc

        try:
            response.raise_for_status()
        except Exception as exc:
            logger.exception(str(exc))
            raise ValueError("Error in reranker") from exc

        response_data = response.json()

        out_nodes = []
        for rank in response_data:
            node = nodes[rank["index"]]
            if node.score:
                node.node.metadata["embedding_similarity"] = node.score
            node.score = rank["score"]
            out_nodes.append(node)

        return sorted(out_nodes, key=lambda node: -node.score)[:top_k]

    def postprocess_nodes(self, nodes, query_bundle=None, **kwargs):
        query = query_bundle.query_str if query_bundle else ""
        return self.rerank(query, nodes)

