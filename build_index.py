from llama_index.node_parser import SimpleNodeParser
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from constants import ALLOWED_VALUE, ENGINEERING, FINANCE
from role_metadata_extractor import RoleMetadataExtractor
from llama_index.node_parser.extractors import (
    MetadataExtractor,
    MetadataFeatureExtractor
)


nodes = []
for role in [ENGINEERING, FINANCE]:
    docs = SimpleDirectoryReader(f'documents/{role}').load_data()

    class CustomExtractor(MetadataFeatureExtractor):
        def class_name():
            return 'CustomExtractor'

        def extract(self, nodes):
            metadata_list = [{role: ALLOWED_VALUE} for node in nodes]
            return metadata_list

    extractor = MetadataExtractor(
        extractors=[CustomExtractor()]
    )
    parser = SimpleNodeParser.from_defaults(metadata_extractor=extractor)
    nodes = nodes + parser.get_nodes_from_documents(docs)

index = VectorStoreIndex(nodes)

index.storage_context.persist()
