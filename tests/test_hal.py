import json
import httpserializers as serializers
from httpserializers.hal_serializer import hal_serializer
from httpserializers import Document, Link, Field

import pytest


def test_hal_serializer():
    assert serializers.serializers["application/hal+json"] is hal_serializer


def test_hal_serializer_small_document():
    hal = serializers.serializers["application/hal+json"]
    body = hal(
        Document(url="/users/", title="Users", content={"users": ["1", "2", "3"]})
    )
    assert json.loads(body.decode("UTF-8")) == {
        "_links": {"self": {"href": "/users/", "title": "Users"}},
        "users": ["1", "2", "3"],
    }


def test_hal_serializer_full_document():
    hal = serializers.serializers["application/hal+json"]
    body = hal(
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
        "_links": {
            "self": {"href": "/users/", "title": "Users"},
            "register_user": {"href": "/users/", "title": "Register a new user"},
        },
        "users": [],
    }


def test_hal_serializer_link():
    hal = serializers.serializers["application/hal+json"]
    body = hal(
        Link(
            href="/users/",
            allow=["POST"],
            description="POSTing to this endpoint creates a new user",
            fields=[Field(name="username")],
        )
    )
    assert json.loads(body.decode("UTF-8")) == {
        "href": "/users/",
    }


def test_warn_if_missing_self():
    hal = serializers.serializers["application/hal+json"]
    with pytest.warns(UserWarning):
        hal(Document())


def test_href_template():
    hal = serializers.serializers["application/hal+json"]
    body = hal(
        Document(url="/", links={"comments": Link(href_template="/comments{/id}/")})
    )
    assert json.loads(body.decode("UTF-8")) == {
        "_links": {
            "self": {"href": "/"},
            "comments": {"href": "/comments{/id}/", "templated": True},
        }
    }


def test_type():
    hal = serializers.serializers["application/hal+json"]
    body = hal(
        Document(
            url="/",
            links={
                "comments": Link(
                    href_template="/comments{/id}/", formats=["application/hal+json"]
                )
            },
        )
    )
    assert json.loads(body.decode("UTF-8")) == {
        "_links": {
            "self": {"href": "/"},
            "comments": {
                "href": "/comments{/id}/",
                "templated": True,
                "type": "application/hal+json",
            },
        }
    }
