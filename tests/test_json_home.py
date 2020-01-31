import json

import httpserializers as serializers
from httpserializers import Document, Link, Field


def test_json_home():
    serializer = serializers.serializers["application/json-home"]
    body = serializer(
        Document(
            title="Identification Provider",
            content={
                "links": {
                    "author": "mailto:julien@palard.fr",
                    "describedBy": "https://kisee.readthedocs.io",
                },
                "create_token": Link(
                    "/jwt/",
                    title="jwt",
                    action="post",
                    description="Create a new JSON Web Token.",
                    fields=[
                        Field("username", required=True),
                        Field("password", required=True),
                    ],
                ),
                "register_user": Link(
                    "/users/",
                    action="post",
                    fields=[
                        Field("username", required=True),
                        Field("password", required=True),
                        Field("email", required=True),
                    ],
                ),
            },
        )
    )
    assert json.loads(body.decode("UTF-8")) == {
        "api": {
            "title": "Identification Provider",
            "links": {
                "author": "mailto:julien@palard.fr",
                "describedBy": "https://kisee.readthedocs.io",
            },
        },
        "resources": {
            "jwt": {
                "href": "http://localhost:8000/jwt/",
                "hints": {
                    "allow": ["GET", "POST"],
                    "formats": {"application/coreapi+json": {}},
                },
            },
            "users": {
                "href": f"http://localhost:8000/users/",
                "hints": {
                    "allow": ["GET", "POST", "PATCH"],
                    "formats": {"application/coreapi+json": {}},
                },
            },
        },
        "actions": {
            "register_user": {
                "href": f"http://localhost:8000/users/",
                "method": "POST",
                "fields": [
                    {"name": "username", "required": True},
                    {"name": "password", "required": True},
                    {"name": "email", "required": True},
                ],
            },
            "create_token": {
                "href": f"http://localhost:8000/jwt/",
                "method": "POST",
                "fields": [
                    {"name": "username", "required": True},
                    {"name": "password", "required": True},
                ],
            },
        },
    }
