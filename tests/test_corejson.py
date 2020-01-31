import json
import httpserializers as serializers
from httpserializers.corejson_serializer import coreapi_serializer
from httpserializers import Document, Link, Field


def test_corejson_serializer():
    assert serializers.serializers["application/coreapi+json"] is coreapi_serializer


def test_corejson_serializer_small_document():
    corejson = serializers.serializers["application/coreapi+json"]
    body = corejson(
        Document(url="/users/", title="Users", content={"users": ["1", "2", "3"]})
    )
    assert json.loads(body.decode("UTF-8")) == {
        "_type": "document",
        "_meta": {"url": "/users/", "title": "Users"},
        "users": ["1", "2", "3"],
    }


def test_corejson_serializer_full_document():
    corejson = serializers.serializers["application/coreapi+json"]
    body = corejson(
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
    )
    assert json.loads(body.decode("UTF-8")) == {
        "_type": "document",
        "_meta": {"url": "/users/", "title": "Users"},
        "users": [],
        "register_user": {
            "_type": "link",
            "url": "/users/",
            "title": "Register a new user",
            "description": "POSTing to this endpoint creates a new user",
            "action": "post",
            "fields": [
                {
                    "name": "username",
                    "required": True,
                    "schema": {"type": "string", "minLength": 3},
                },
                {
                    "name": "password",
                    "required": True,
                    "schema": {"type": "string", "minLength": 5, "format": "password"},
                },
            ],
        },
    }


def test_corejson_serializer_link():
    corejson = serializers.serializers["application/coreapi+json"]
    body = corejson(
        Link(
            url="/users/",
            action="post",
            description="POSTing to this endpoint creates a new user",
            fields=[Field(name="username")],
        ),
    )
    assert json.loads(body.decode("UTF-8")) == {
        "_type": "link",
        "url": "/users/",
        "description": "POSTing to this endpoint creates a new user",
        "action": "post",
        "fields": [{"name": "username"}],
    }


def test_corejson_serializer_link_not_required():
    corejson = serializers.serializers["application/coreapi+json"]
    body = corejson(
        Link(
            url="/users/",
            action="post",
            description="POSTing to this endpoint creates a new user",
        ),
    )
    assert json.loads(body.decode("UTF-8")) == {
        "_type": "link",
        "url": "/users/",
        "description": "POSTing to this endpoint creates a new user",
        "action": "post",
    }
