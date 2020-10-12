"""Minimalistic JSON serializer.
"""

import json

from httpserializers.types import Document, Link, Field, Serializer
from httpserializers.utils import as_absolute


def _json_serializer(node, base_url=None):
    """Recursively encode a Document using a minimalistic JSON format."""
    if isinstance(node, Document):
        return {
            **{
                key: _json_serializer(value, base_url=base_url)
                for key, value in node.content.items()
            },
            **{
                key: _json_serializer(value, base_url=base_url)
                for key, value in node.links.items()
            },
        }

    if isinstance(node, Link):
        return as_absolute(base_url, node.href or node.href_template)

    if isinstance(node, Field):
        return node.name

    if isinstance(node, list):
        return [_json_serializer(value, base_url=base_url) for value in node]

    return node


class JSONSerializer(Serializer):
    """Minimalistic JSON serializer."""

    media_type = "application/json"

    def serialize(self, document: Document, base_url: str = None) -> bytes:
        """Serializes a Document using a minimalistic JSON format."""
        return json.dumps(_json_serializer(document, base_url), indent=4).encode(
            "UTF-8"
        )
