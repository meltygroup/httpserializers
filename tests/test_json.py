import httpserializers as serializers
from httpserializers import Document, Link, Field


def test_json_serializer_full_document():
    corejson = serializers.serializers["application/json"]
    assert corejson(
        Document(
            url="/users/",
            title="Users",
            content={
                "users": [],
                "register_user": Link(
                    url="/users/",
                    action="post",
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
    ) == {"register_user": "/users/", "users": []}


def test_json_serializer():
    json_serializer = serializers.serializers["application/json"]
    assert json_serializer([]) == []
    assert json_serializer("Hello world") == "Hello world"
    assert json_serializer(Document(url="/", title="Test", content={})) == {}
    assert json_serializer(Link(url="/link/", action="POST", title="Foo")) == "/link/"
    assert (
        json_serializer(
            Field(name="username", required=False, description="Just a login")
        )
        == "username"
    )
