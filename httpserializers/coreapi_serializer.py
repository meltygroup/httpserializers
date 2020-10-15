"""Serializes using https://www.coreapi.org/specification/encoding/
(application/vnd.coreapi+json).
"""

import json

from httpserializers.utils import as_absolute


def _coreapi_serializer(node, base_url, path, schema):
    """Recursively serializes a document according to coreapi+json."""


class CoreAPISerializer:
    """coreapi+json serializer."""

    media_type = "application/hal+json"

    def serialize(self, document, base_url: str, path: str, schema) -> str:
        """Serialize a document using Core API serializer."""
        doc = {
            "_type": "document",
            "_meta": {
                "url": as_absolute(base_url, path),
                "title": schema["paths"][path]["get"].get("description", ""),
            },
            **document,
        }
        for method, link in schema["paths"][path].items():
            doc[method] = {
                "_type": "link",
                "url": as_absolute(base_url, path),
                "action": method,
                "title": link.get("summary"),
                "description": link.get("description"),
                "fields": [],
            }
            # TODO Add fields from OpenAPI content / application/json / schema ?
        return json.dumps(doc, indent=4)
