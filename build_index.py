from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.node_parser import SimpleNodeParser
from llama_index.node_parser.extractors import (
    MetadataExtractor,
    MetadataFeatureExtractor
)
from constants import ALLOWED_VALUE, ENGINEERING_ROLE, FINANCE_ROLE


# Connect documents to their permissions based on directory
# In a real applications, this would come from the source api
# (eg, from GoogleDrive's file metadata)
documents = [
    ('engineering', [ENGINEERING_ROLE]),
    ('finance', [FINANCE_ROLE]),
    ('both', [ENGINEERING_ROLE, FINANCE_ROLE])]

nodes = []
for directory, roles in documents:
    docs = SimpleDirectoryReader(f'documents/{directory}').load_data()

    class CustomExtractor(MetadataFeatureExtractor):
        def class_name():
            return 'CustomExtractor'

        # Attach an allowlist of roles to each document as metadata
        def extract(self, nodes):
            return [{role: ALLOWED_VALUE for role in roles}] * len(nodes)

    # Use the CustomExtractor to attach metadata to nodes based on their defined permissions
    extractor = MetadataExtractor(extractors=[CustomExtractor()])
    parser = SimpleNodeParser.from_defaults(metadata_extractor=extractor)
    nodes = nodes + parser.get_nodes_from_documents(docs)

# Create the index with all nodes including their role-based metadata
index = VectorStoreIndex(nodes)

# Persist the index for querying in a different script to reduce OpenAI API usage
index.storage_context.persist()
print("Index persisted")
