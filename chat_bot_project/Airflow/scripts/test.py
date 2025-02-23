import os
from pymilvus.model.reranker import CrossEncoderRerankFunction


reranker = CrossEncoderRerankFunction(
    model_name=os.getenv("RERANKER_MODEL"),
    device="cpu",
)
