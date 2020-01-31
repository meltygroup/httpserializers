"""Serialisers using coreapi, the idea is to (in the future) provide
various representations of our resources like mason, json-ld, hal, ...

"""

from typing import Tuple

from httpserializers.types import Document, Link, Field
from httpserializers.corejson_serializer import coreapi_serializer
from httpserializers.json_serializer import json_serializer
from httpserializers.html_serializer import html_serializer
from httpserializers.registry import serializers


def serialize(
    document: Document, accept_header: str, hostname: str
) -> Tuple[str, bytes]:
    """Serialize the given document according to the Accept header of the
    given request.
    """
    serializer = serializers[accept_header]
    return (list(serializer.media_types)[0], serializer(document, hostname))
