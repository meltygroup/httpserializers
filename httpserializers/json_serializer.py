"""Minimalistic JSON serializer."""

import json


class JSONSerializer:
    """Minimalistic JSON serializer."""

    media_type = "application/json"

    def serialize(self, document, base_url: str, path: str, schema) -> str:
        """Serializes a Document using a minimalistic JSON format."""
        return json.dumps(document, indent=4)
