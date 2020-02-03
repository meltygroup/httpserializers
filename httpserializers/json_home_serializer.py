"""Serialize using the JSON-Home format
https://mnot.github.io/I-D/json-home/.
"""
import json

from httpserializers.types import Document, Link
from httpserializers.utils import as_absolute
from httpserializers.registry import serializers


def _json_home_serializer(node, base_url=None):
    """Recursively serialize a document to the JSON-home format.
    """
    if isinstance(node, Document):
        ret = {"api": {"title": node.title}}
        ret["resources"] = {
            key: _json_home_serializer(item, base_url)
            for key, item in node.links.items()
        }

    if isinstance(node, Link):
        # Templated links are indicated with an “hrefTemplate” property,
        # whose value is a URI Template [RFC6570].
        ret = {}
        if node.href:
            ret["href"] = as_absolute(base_url, node.href)
        else:
            ret["hrefTemplate"] = as_absolute(base_url, node.href_template)
        if node.href_vars:
            ret["hrefVars"] = node.href_vars
        if node.formats or node.allow:
            ret["hints"] = {}
        if node.formats:
            ret["hints"]["formats"] = node.formats
        if node.allow:
            ret["hints"]["allow"] = list(node.allow)

    return ret


@serializers(media_types={"application/json_home+json"}, default=True)
def json_home_serializer(node, base_url=None):
    """JSON-Home serializer.
    """
    return json.dumps(_json_home_serializer(node, base_url), indent=4).encode("UTF-8")
