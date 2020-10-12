"""Serializes using https://www.coreapi.org/specification/encoding/
(application/vnd.coreapi+json).
"""

import json

from httpserializers.types import Document, Link, Field, Serializer
from httpserializers.utils import as_absolute


def _coreapi_serializer(node, base_url=None):
    """Recursively serializes a document according to coreapi+json."""
    if isinstance(node, Document):
        ret = {}
        ret["_type"] = "document"

        meta = {}
        url = node.url
        meta["url"] = as_absolute(base_url, url)
        meta["title"] = node.title
        ret["_meta"] = meta

        # Fill in key-value content.
        ret.update(
            [
                (key, _coreapi_serializer(value, base_url=base_url))
                for key, value in node.content.items()
            ]
        )
        ret.update(
            [
                (key, _coreapi_serializer(value, base_url=base_url))
                for key, value in node.links.items()
            ]
        )
        return ret

    if isinstance(node, Link):
        ret = {}
        ret["_type"] = "link"
        ret["url"] = as_absolute(base_url, node.href or node.href_template)
        if node.allow:
            ret["action"] = node.allow[0].lower()
        if node.title:
            ret["title"] = node.title
        ret["description"] = node.description
        if node.fields:
            ret["fields"] = [
                _coreapi_serializer(field, base_url=base_url) for field in node.fields
            ]
        return ret

    if isinstance(node, Field):
        ret = {"name": node.name}
        if node.required:
            ret["required"] = node.required
        if node.schema:
            ret["schema"] = node.schema
        return ret

    if isinstance(node, list):
        return [_coreapi_serializer(value, base_url=base_url) for value in node]

    return node


class CoreAPISerializer(Serializer):
    """coreapi+json serializer."""

    media_type = "application/hal+json"

    def serialize(self, document: Document, base_url: str = None) -> bytes:
        """Serialize a document using Core API serializer."""
        return json.dumps(_coreapi_serializer(document, base_url), indent=4).encode(
            "UTF-8"
        )
