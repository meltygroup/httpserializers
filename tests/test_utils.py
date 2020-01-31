from httpserializers.utils import as_absolute


def test_as_absolute():
    assert as_absolute("http://localhost/", "/foo") == as_absolute(
        "http://localhost/", "http://localhost/foo"
    )
