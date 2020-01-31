import httpserializers as serializers
from httpserializers import Document, Link, Field


def test_default_serializer():
    assert serializers.serializers[""] is serializers.serializers.default
    assert serializers.serializers[None] is serializers.serializers.default


def test_fallback_serializer():
    assert (
        serializers.serializers["another/contenttype"]
        is serializers.serializers.default
    )


def test_serialize_function():
    assert serializers.serialize(
        Document(), accept_header="application/json", hostname="http://127.0.0.1:8000",
    ) == ("application/json", b"{}")
