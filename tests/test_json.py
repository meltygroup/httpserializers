import json
import httpserializers as serializers
from httpserializers import Document, Link, Field


def test_json_serializer_full_document():
    basejson = serializers.serializers["application/json"]
    body = basejson(
        Document(
            url="/users/",
            title="Users",
            content={"users": []},
            links={
                "register_user": Link(
                    href="/users/",
                    allow=["POST"],
                    title="Register a new user",
                    description="POSTing to this endpoint creates a new user",
                    fields=[
                        Field(
                            name="username",
                            required=True,
                            schema={"type": "string", "minLength": 3},
                        ),
                        Field(
                            name="password",
                            required=True,
                            schema={
                                "type": "string",
                                "minLength": 5,
                                "format": "password",
                            },
                        ),
                    ],
                ),
            },
        )
    )
    assert json.loads(body.decode("UTF-8")) == {
        "register_user": "/users/",
        "users": [],
    }


def json_serialize(document):
    body = serializers.serializers["application/json"](document)
    return json.loads(body.decode("utf-8"))


def test_json_serializer():
    assert json_serialize([]) == []
    assert json_serialize("Hello world") == "Hello world"
    assert json_serialize(Document(url="/", title="Test", content={})) == {}
    assert json_serialize(Link(href="/link/", allow=["POST"], title="Foo")) == "/link/"
    assert (
        json_serialize(
            Field(name="username", required=False, description="Just a login")
        )
        == "username"
    )
