from llama_index.node_parser.extractors import MetadataFeatureExtractor
from constants import ALLOWED_VALUE


class RoleMetadataExtractor(MetadataFeatureExtractor):
    def __init__(self, role):
        self._role = role

    def extract(self, nodes):
        metadata_list = [
            {
                self._role: ALLOWED_VALUE
            }
            for node in nodes
        ]
        print(metadata_list)
        return metadata_list

    def class_name():
        return 'lol idk'
