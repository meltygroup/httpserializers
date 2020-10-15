"""Serializes using HAL
(https://www.ietf.org/archive/id/draft-kelly-json-hal-08.txt).
"""

import json
from warnings import warn

from httpserializers.utils import as_absolute


def _hal_serializer(node, base_url, path, schema):
    """Recursively serialize a Document to the HAL format."""
    document = {
        "_links": {
            "self": {
                "href": as_absolute(base_url, path),
                "title": schema["paths"][path]["get"].get("summary"),
            },
            **node,
        }
    }
    return document


class HALSerializer:
    """HAL serializer."""

    media_type = "application/hal+json"

    def serialize(self, document, base_url: str, path, schema) -> str:
        """Recursively serialize a Document to the HAL format."""
        return json.dumps(_hal_serializer(document, base_url, path, schema), indent=4)
