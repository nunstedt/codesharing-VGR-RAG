from llama_index.core.schema import MetadataMode, NodeWithScore
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import logging

logger = logging.getLogger(__name__)




class TEIReranker:
    def __init__(self, model_name: str = "Alibaba-NLP/gte-multilingual-reranker-base"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name, trust_remote_code=True)
        self.model.eval()

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

        # Prepare pairs for scoring
        texts = [node.get_content(metadata_mode) for node in nodes]
        pairs = [(query, text) for text in texts]

        # Tokenize and score
        inputs = self.tokenizer(
            [p[0] for p in pairs],
            [p[1] for p in pairs],
            padding=True,
            truncation=True,
            return_tensors="pt"
        )
        with torch.no_grad():
            scores = self.model(**inputs).logits.squeeze(-1)
            if scores.dim() == 0:
                scores = scores.unsqueeze(0)
            scores = scores.cpu().numpy()

        # Assign scores to nodes
        out_nodes = []
        for i, node in enumerate(nodes):
            node.score = float(scores[i])
            out_nodes.append(node)

        return sorted(out_nodes, key=lambda node: -node.score)[:top_k]

    def postprocess_nodes(self, nodes, query_bundle=None, **kwargs):
        query = query_bundle.query_str if query_bundle else ""
        return self.rerank(query, nodes)
