"""Serializes using HAL
(https://www.ietf.org/archive/id/draft-kelly-json-hal-08.txt).
"""

import json
from warnings import warn

from httpserializers.types import Document, Link
from httpserializers.utils import as_absolute
from httpserializers.registry import serializers


def _hal_serializer(node, base_url=None):
    """Recursively serialize a Document to the HAL format.
    """
    if isinstance(node, Document):
        ret = {}
        ret["_links"] = {
            key: _hal_serializer(item, base_url=base_url)
            for key, item in node.links.items()
        }
        if not node.url:
            warn("Each Resource Object SHOULD contain a 'self' link")
        ret["_links"]["self"] = {"href": as_absolute(base_url, node.url)}
        if node.title:
            ret["_links"]["self"]["title"] = node.title
        # Fill in key-value content.
        ret.update(
            [
                (key, _hal_serializer(value, base_url=base_url))
                for key, value in node.content.items()
            ]
        )
        return ret

    if isinstance(node, Link):
        # The "templated" property is OPTIONAL.  Its value is boolean and
        # SHOULD be true when the Link Object's "href" property is a URI
        # Template.
        ret = {}
        if node.href:
            ret["href"] = as_absolute(base_url, node.href)
        else:
            ret["href"] = as_absolute(base_url, node.href_template)
            ret["templated"] = True
        if node.formats:
            ret["type"] = node.formats[0]
        if node.title:
            ret["title"] = node.title
        return ret

    if isinstance(node, list):
        return [_hal_serializer(value, base_url=base_url) for value in node]

    return node


@serializers(media_types={"application/hal+json"}, default=True)
def hal_serializer(node, base_url=None):
    """HAL serializer.
    """
    return json.dumps(_hal_serializer(node, base_url), indent=4).encode("UTF-8")
