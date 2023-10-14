import argparse
from llama_index import StorageContext, load_index_from_storage
# from RolesRetriever import RolesRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.response_synthesizers import get_response_synthesizer
from rag_query_engine import RAGQueryEngine
from custom_retriever import CustomRetriever
from llama_index.retrievers import VectorIndexRetriever
from constants import ALLOWED_VALUE
from llama_index.vector_stores.types import MetadataFilters

parser = argparse.ArgumentParser(description='Process some arguments.')
parser.add_argument('--role', type=str, required=True,
                    help='Role must be in [ENGINEERING, FINANCE]')
parser.add_argument('--query', type=str, required=True,
                    help='Query text string')

args = parser.parse_args()

print(args.query)

storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)

# Customer retriever
# retriever = RolesRetriever()

# query_engine = RetrieverQueryEngine(retriever=retriever)

metadata_filters = MetadataFilters.from_dict({args.role: ALLOWED_VALUE})

vector_retriever = VectorIndexRetriever(index=index, filters=metadata_filters)

# query_engine = index.as_query_engine(retriever=custom_retriever)
query_engine = RetrieverQueryEngine.from_args(
    retriever=vector_retriever, service_context=index.service_context)
# retriever = index.as_retriever()
# synthesizer = get_response_synthesizer(response_mode="compact")
# query_engine = RAGQueryEngine(
#     retriever=retriever, response_synthesizer=synthesizer)

response = query_engine.query(args.query)

print(str(response))
