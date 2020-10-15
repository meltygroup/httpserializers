"""Serializes using JSON-LD
(https://json-ld.org/).
"""

import json
from warnings import warn

from httpserializers.utils import as_absolute


def _ld_serializer(node, base_url=None):
    """Recursively serialize a Document to the JSON-LD format."""
    if isinstance(node, Document):
        ret = {
            key: _ld_serializer(value, base_url=base_url)
            for key, value in node.content.items()
        }
        if not node.url:
            warn("Each Resource Object SHOULD contain a 'self' link")
        ret["_links"] = {"self": {"href": as_absolute(base_url, node.url)}}
        if node.title:
            ret["_links"]["self"]["title"] = node.title
        ret["_links"].update(
            {
                key: _ld_serializer(item, base_url=base_url)
                for key, item in node.links.items()
            }
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
        return [_ld_serializer(value, base_url=base_url) for value in node]

    return node


class HALSerializer(Serializer):
    """HAL serializer."""

    media_type = "application/hal+json"

    def serialize(self, document, base_url: str, path, schema) -> str:
        """Recursively serialize a Document to the HAL format."""
        return json.dumps(_ld_serializer(document, base_url), indent=4).encode("UTF-8")
