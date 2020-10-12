import json
import httpserializers as serializers
from httpserializers.coreapi_serializer import CoreAPISerializer
from httpserializers import Document, Link, Field

import pytest


@pytest.fixture
def coreapi():
    return serializers.serializers["application/vnd.coreapi+json"]


@pytest.fixture
def coreapi_serializer(coreapi):
    def serialize(document: Document):
        return json.loads(coreapi.serialize(document).decode("UTF-8"))

    return serialize


def test_coreapi_serializer(coreapi):
    assert isinstance(coreapi, CoreAPISerializer)


def test_coreapi_serializer_small_document(coreapi_serializer):
    body = coreapi_serializer(
        Document(url="/users/", title="Users", content={"users": ["1", "2", "3"]})
    )
    assert body == {
        "_type": "document",
        "_meta": {"url": "/users/", "title": "Users"},
        "users": ["1", "2", "3"],
    }


def test_coreapi_serializer_full_document(coreapi_serializer):
    body = coreapi_serializer(
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
    assert body == {
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


def test_coreapi_serializer_link(coreapi_serializer):
    body = coreapi_serializer(
        Link(
            href="/users/",
            allow=["POST"],
            description="POSTing to this endpoint creates a new user",
            fields=[Field(name="username")],
        )
    )
    assert body == {
        "_type": "link",
        "url": "/users/",
        "description": "POSTing to this endpoint creates a new user",
        "action": "post",
        "fields": [{"name": "username"}],
    }


def test_coreapi_serializer_link_with_no_allow(coreapi_serializer):
    body = coreapi_serializer(
        Link(
            href="/users/",
            description="POSTing to this endpoint creates a new user",
            fields=[Field(name="username")],
        )
    )
    assert body == {
        "_type": "link",
        "url": "/users/",
        "description": "POSTing to this endpoint creates a new user",
        "fields": [{"name": "username"}],
    }


def test_coreapi_serializer_link_not_required(coreapi_serializer):
    body = coreapi_serializer(
        Link(
            href="/users/",
            allow=["POST"],
            description="POSTing to this endpoint creates a new user",
        )
    )
    assert body == {
        "_type": "link",
        "url": "/users/",
        "description": "POSTing to this endpoint creates a new user",
        "action": "post",
    }
