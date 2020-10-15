"""Serialisers using coreapi, the idea is to (in the future) provide
various representations of our resources like mason, json-ld, hal, ...

"""

from typing import Tuple, Union

from httpserializers.registry import Serializers

from httpserializers.coreapi_serializer import CoreAPISerializer
from httpserializers.json_serializer import JSONSerializer
from httpserializers.json_home_serializer import JSONHomeSerializer
from httpserializers.hal_serializer import HALSerializer
from httpserializers.html_serializer import HTMLSerializer

serializers = Serializers(default=JSONSerializer())  # pylint: disable=invalid-name
serializers["application/vnd.coreapi+json"] = CoreAPISerializer()
serializers["application/hal+json"] = HALSerializer()
serializers["text/html"] = HTMLSerializer()
serializers["application/json"] = JSONSerializer()
serializers["application/json-home"] = JSONHomeSerializer()


__all__ = [
    "CoreAPISerializer",
    "JSONSerializer",
    "JSONHomeSerializer",
    "HALSerializer",
    "serializers",
    "serialize",
]


def serialize(
    document: Union[dict, list],
    *,
    accept_header: str,
    hostname: str,
    path: str,
    schema: dict
) -> Tuple[str, str]:
    """Serialize the given document according to the Accept header of the
    given request.
    """
    serializer = serializers[accept_header]
    return (
        serializer.media_type,
        serializer.serialize(document, hostname, path, schema),
    )
