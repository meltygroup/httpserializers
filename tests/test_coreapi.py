import json
import httpserializers as serializers
from httpserializers.coreapi_serializer import coreapi_serializer
from httpserializers import Document, Link, Field


def test_coreapi_serializer():
    assert serializers.serializers["application/coreapi+json"] is coreapi_serializer


def test_coreapi_serializer_small_document():
    coreapi = serializers.serializers["application/coreapi+json"]
    body = coreapi(
        Document(url="/users/", title="Users", content={"users": ["1", "2", "3"]})
    )
    assert json.loads(body.decode("UTF-8")) == {
        "_type": "document",
        "_meta": {"url": "/users/", "title": "Users"},
        "users": ["1", "2", "3"],
    }


def test_coreapi_serializer_full_document():
    coreapi = serializers.serializers["application/coreapi+json"]
    body = coreapi(
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


def test_coreapi_serializer_link():
    coreapi = serializers.serializers["application/coreapi+json"]
    body = coreapi(
        Link(
            href="/users/",
            allow=["POST"],
            description="POSTing to this endpoint creates a new user",
            fields=[Field(name="username")],
        )
    )
    assert json.loads(body.decode("UTF-8")) == {
        "_type": "link",
        "url": "/users/",
        "description": "POSTing to this endpoint creates a new user",
        "action": "post",
        "fields": [{"name": "username"}],
    }


def test_coreapi_serializer_link_with_no_allow():
    coreapi = serializers.serializers["application/coreapi+json"]
    body = coreapi(
        Link(
            href="/users/",
            description="POSTing to this endpoint creates a new user",
            fields=[Field(name="username")],
        )
    )
    assert json.loads(body.decode("UTF-8")) == {
        "_type": "link",
        "url": "/users/",
        "description": "POSTing to this endpoint creates a new user",
        "fields": [{"name": "username"}],
    }


def test_coreapi_serializer_link_not_required():
    coreapi = serializers.serializers["application/coreapi+json"]
    body = coreapi(
        Link(
            href="/users/",
            allow=["POST"],
            description="POSTing to this endpoint creates a new user",
        )
    )
    assert json.loads(body.decode("UTF-8")) == {
        "_type": "link",
        "url": "/users/",
        "description": "POSTing to this endpoint creates a new user",
        "action": "post",
    }
