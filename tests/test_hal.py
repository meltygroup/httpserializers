import json
import httpserializers as serializers
from httpserializers.hal_serializer import HALSerializer
from httpserializers import Document, Link, Field, Attribute

import pytest


@pytest.fixture
def hal():
    return serializers.serializers["application/hal+json"]


@pytest.fixture
def hal_serializer(hal):
    def serialize(document: Document):
        return json.loads(hal.serialize(document).decode("UTF-8"))

    return serialize


def test_hal_serializer(hal):
    assert isinstance(hal, HALSerializer)


class Users(Document):
    """Reply for /users/"""

    users = Attribute("https://schema.org/Person", type=list)


def test_hal_serializer_small_document(hal_serializer):
    body = hal_serializer(Users(url="/users/", users=["1", "2", "3"]))
    assert body == {
        "_links": {"self": {"href": "/users/", "title": "Users"}},
        "users": ["1", "2", "3"],
    }


def test_hal_serializer_full_document(hal_serializer):
    body = hal_serializer(
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
        "_links": {
            "self": {"href": "/users/", "title": "Users"},
            "register_user": {"href": "/users/", "title": "Register a new user"},
        },
        "users": [],
    }


def test_hal_serializer_link(hal_serializer):
    body = hal_serializer(
        Link(
            href="/users/",
            allow=["POST"],
            description="POSTing to this endpoint creates a new user",
            fields=[Field(name="username")],
        )
    )
    assert body == {
        "href": "/users/",
    }


def test_warn_if_missing_self(hal_serializer):
    with pytest.warns(UserWarning):
        hal_serializer(Document())


def test_href_template(hal_serializer):
    body = hal_serializer(
        Document(url="/", links={"comments": Link(href_template="/comments{/id}/")})
    )
    assert body == {
        "_links": {
            "self": {"href": "/"},
            "comments": {"href": "/comments{/id}/", "templated": True},
        }
    }


def test_type(hal_serializer):
    body = hal_serializer(
        Document(
            url="/",
            links={
                "comments": Link(
                    href_template="/comments{/id}/", formats=["application/hal+json"]
                )
            },
        )
    )
    assert body == {
        "_links": {
            "self": {"href": "/"},
            "comments": {
                "href": "/comments{/id}/",
                "templated": True,
                "type": "application/hal+json",
            },
        }
    }
