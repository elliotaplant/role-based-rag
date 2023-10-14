from llama_index.query_engine import CustomQueryEngine
from llama_index.retrievers import BaseRetriever
from llama_index.response_synthesizers import get_response_synthesizer, BaseSynthesizer


class RAGQueryEngine(CustomQueryEngine):
    """RAG Query Engine."""

    retriever: BaseRetriever
    response_synthesizer: BaseSynthesizer

    def custom_query(self, query_str: str):
        print(query_str)
        nodes = self.retriever.retrieve(query_str)
        print(nodes)
        response_obj = self.response_synthesizer.synthesize(query_str, nodes)
        return response_obj
