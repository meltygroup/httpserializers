import json

from httpserializers import Document, Link, Field, JSONHomeSerializer


def test_json_home():
    body = JSONHomeSerializer().serialize(
        Document(
            title="Identification Provider",
            links={
                "create_token": Link(
                    "/jwt/",
                    title="jwt",
                    allow=["GET", "POST"],
                    formats={"application/coreapi+json": {}},
                    description="Create a new JSON Web Token.",
                    fields=[
                        Field("username", required=True),
                        Field("password", required=True),
                    ],
                ),
                "users": Link(
                    "/users/",
                    allow=["GET", "POST", "PATCH"],
                    formats={"application/coreapi+json": {}},
                    fields=[
                        Field("username", required=True),
                        Field("password", required=True),
                        Field("email", required=True),
                    ],
                ),
            },
        ),
        base_url="http://localhost:8000/",
    )
    assert json.loads(body.decode("UTF-8")) == {
        "api": {"title": "Identification Provider"},
        "resources": {
            "create_token": {
                "href": "http://localhost:8000/jwt/",
                "hints": {
                    "allow": ["GET", "POST"],
                    "formats": {"application/coreapi+json": {}},
                },
            },
            "users": {
                "href": "http://localhost:8000/users/",
                "hints": {
                    "allow": ["GET", "POST", "PATCH"],
                    "formats": {"application/coreapi+json": {}},
                },
            },
        },
    }


def test_no_link():
    body = JSONHomeSerializer().serialize(Document(title="Articles"))
    assert json.loads(body.decode("UTF-8")) == {
        "api": {"title": "Articles"},
        "resources": {},
    }


def test_href_template():
    body = JSONHomeSerializer().serialize(
        Document(
            url="/",
            title="Articles",
            links={
                "comments": Link(
                    href_template="/comments{/id}/", href_vars={"id": "/params/id/"}
                )
            },
        )
    )
    assert json.loads(body.decode("UTF-8")) == {
        "api": {"title": "Articles"},
        "resources": {
            "comments": {
                "hrefTemplate": "/comments{/id}/",
                "hrefVars": {"id": "/params/id/"},
            },
        },
    }
