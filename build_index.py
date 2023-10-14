from llama_index.node_parser import SimpleNodeParser
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from constants import ALLOWED_VALUE, ENGINEERING_ROLE, FINANCE_ROLE


engineering_docs = SimpleDirectoryReader(
    'documents/engineering').load_data()

finance_docs = SimpleDirectoryReader(
    'documents/finance').load_data()

parser = SimpleNodeParser.from_defaults()

engineering_nodes = parser.get_nodes_from_documents(engineering_docs)
for node in engineering_nodes:
    node.metadata[ENGINEERING_ROLE] = ALLOWED_VALUE

finance_nodes = parser.get_nodes_from_documents(finance_docs)
for node in finance_nodes:
    node.metadata[FINANCE_ROLE] = ALLOWED_VALUE

index = VectorStoreIndex(engineering_nodes + finance_nodes)

index.storage_context.persist()
