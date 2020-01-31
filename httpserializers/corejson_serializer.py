import json

from httpserializers.types import Document, Link, Field
from httpserializers.utils import as_absolute
from httpserializers.registry import serializers


def _coreapi_serializer(node, base_url=None):
    """Take a Core API document and return Python primitives
    ready to be rendered into the JSON style encoding.
    """
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
                for key, value in node.data.items()
            ]
        )
        return ret

    if isinstance(node, Link):
        ret = {}
        ret["_type"] = "link"
        url = node.url
        ret["url"] = as_absolute(base_url, url)
        ret["action"] = node.action
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


@serializers(media_types={"application/coreapi+json"}, default=True)
def coreapi_serializer(node, base_url=None):
    return json.dumps(_coreapi_serializer(node, base_url), indent=4).encode("UTF-8")
