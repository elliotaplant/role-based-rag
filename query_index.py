import argparse
from llama_index import StorageContext, load_index_from_storage
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.retrievers import VectorIndexRetriever
from constants import ALLOWED_VALUE
from llama_index.vector_stores.types import MetadataFilters

# Parse command line arguments
# Note that only one role is allowed because llama_index currently only supports
#   exact-matching metadata keys, which prevents authorization by role "intersection"
parser = argparse.ArgumentParser(description='Process some arguments.')
parser.add_argument('--role', type=str, required=True,
                    help='Role must be in [ENGINEERING, FINANCE]')
parser.add_argument('--query', type=str, required=True,
                    help='Query text string')

args = parser.parse_args()

# Load the index from disk
storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)

# Create a filter that prevents the query from reading documents that do not
#   have the required role allowed in their metadata
metadata_filters = MetadataFilters.from_dict({args.role: ALLOWED_VALUE})

# Use the filter in the query on the index
vector_retriever = VectorIndexRetriever(index=index, filters=metadata_filters)
query_engine = RetrieverQueryEngine.from_args(
    retriever=vector_retriever, service_context=index.service_context)
response = query_engine.query(args.query)

# Display the response to the TTY
print(str(response))
