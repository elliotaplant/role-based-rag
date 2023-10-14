from llama_index.retrievers import BaseRetriever
from llama_index import QueryBundle
from constants import ROLES_KEY


class CustomRetriever(BaseRetriever):
    # Roles is a set of strings. Please help
    def __init__(self,
                 vector_retriever,
                 roles):
        self._vector_retriever = vector_retriever
        self._roles = roles

    def _retrieve(self, query_bundle: QueryBundle):
        vector_nodes = self._vector_retriever.retrieve(query_bundle)
        print(f"ORiginally {len(vector_nodes)} nodes")
        print("metadata", vector_nodes[0].metadata)
        filtered = [
            node for node in vector_nodes if any(role in self._roles for role in node.metadata[ROLES_KEY])]
        print(f"After {len(filtered)} nodes")
        return filtered
