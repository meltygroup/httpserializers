"""Serialisers using coreapi, the idea is to (in the future) provide
various representations of our resources like mason, json-ld, hal, ...

"""

from typing import Tuple

from httpserializers.types import Document, Link, Field
from httpserializers.coreapi_serializer import coreapi_serializer
from httpserializers.json_serializer import json_serializer
from httpserializers.json_home_serializer import json_home_serializer
from httpserializers.hal_serializer import hal_serializer
from httpserializers.registry import serializers

__all__ = [
    "Document",
    "Link",
    "Field",
    "coreapi_serializer",
    "json_serializer",
    "json_home_serializer",
    "hal_serializer",
    "serializers",
]


def serialize(
    document: Document, accept_header: str, hostname: str
) -> Tuple[str, bytes]:
    """Serialize the given document according to the Accept header of the
    given request.
    """
    serializer = serializers[accept_header]
    return (list(serializer.media_types)[0], serializer(document, hostname))
