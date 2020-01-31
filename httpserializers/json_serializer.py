import json

from httpserializers.types import Document, Link, Field
from httpserializers.utils import as_absolute
from httpserializers.registry import serializers


def _json_serializer(node, base_url=None):
    if isinstance(node, Document):
        return {
            key: _json_serializer(value, base_url=base_url)
            for key, value in node.data.items()
        }

    if isinstance(node, Link):
        return as_absolute(base_url, node.url)

    if isinstance(node, Field):
        return node.name

    if isinstance(node, list):
        return [_json_serializer(value, base_url=base_url) for value in node]

    return node


@serializers(media_types={"application/json"}, default=False)
def json_serializer(node, base_url=None):
    """Serialize a response to basic json.
    """
    return json.dumps(_json_serializer(node, base_url), indent=4).encode("UTF-8")
