import httpserializers as serializers
from httpserializers.html_serializer import html_serializer
from httpserializers import Document, Link, Field


def test_html_serializer():
    assert serializers.serializers["text/html"] is html_serializer


def test_html_serializer_small_document():
    html = serializers.serializers["text/html"]
    body = html(
        Document(url="/users/", title="Users", content={"users": ["1", "2", "3"]})
    )
    assert "Users" in body.decode("UTF-8")


def test_html_serializer_full_document():
    html = serializers.serializers["text/html"]
    body = html(
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
    ).decode("UTF-8")
    assert "Register a new user" in body
    assert "password" in body


def test_html_serializer_link():
    html = serializers.serializers["text/html"]
    body = html(
        Link(
            href="/users/",
            allow=["POST"],
            description="Posting to this endpoint creates a new user",
            fields=[Field(name="username")],
        )
    )
    assert "POST" in body.decode("UTF-8")


def test_no_field():
    html = serializers.serializers["text/html"]
    body = html(
        Link(
            href="/users/",
            allow=["POST"],
            description="Posting to this endpoint creates a new user",
        )
    ).decode("UTF-8")
    assert "POST" in body
    assert "field" not in body
