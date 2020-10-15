# HTTP Serializers

`HTTPSerializers` is a work in progress, stalled, Python library
helping APIs replying correctly to the `Accept` HTTP header.

A way may be to describe an API using an OpenAPI description, (anyway
if you don't have one, write it, you'll see, it's nice).

How it could work:

```python
from httpserializer import serialize

def your_handler(request):
    ...
    return serialize(message, accept_header, openapi_spec)
```

You give the response message, the accept header, the OpenAPI spec to
the httpserializers.serialize function and you'll get an appropriate
response (elementary transformation would be do deliver a very pretty
HTML if the client asks for HTML, or a Markdown rendering if the
client asks for plain text).

Idea is to handle at least those types:

- [JSON-LD](https://json-ld.org).
- [HAL](https://www.ietf.org/archive/id/draft-kelly-json-hal-08.txt).
- Plain old JSON (no transformation of the document).
- Plain old HTML, just in case you're on a web browser.
- Plain text (as Markdown).
- [JSON-home](https://mnot.github.io/I-D/json-home/), autogenerated from OpenAPI spec.


## What about HATEOAS

OpenAPI can't really describe HATEOAS (Issue
[#577](https://github.com/OAI/OpenAPI-Specification/issues/577), so
you're more or less damned from the beginning.

You can still give URLs in responses, it's always a good start, but
It'll probably be hard to properly describe actions near to them in
the responses like HTML have `<form>` to properly describe the
expected content of a POST body.

Anyway, having a fully HATEOAS implementation will not prevent a
client from hardcoding many URL, so it's not the unique ultimate
solution, if at least they follow the `next` links, eventually other
[IANA](http://www.iana.org/assignments/link-relations/link-relations.xhtml)
link relation names, it's a good start.


## Example usage of current WIP implementation

Imagine a simple document describing an article, having a title, a
body, and a link to its comments, you can describe it using simple
Python:

```python
>>> from httpserializers import Document, Link, serializers

>>> article = Document(
...     title="Article",
...     url="/articles/123/",
...     content={
...         "title": "Wild fires over there",
...         "body": "Firefighters spotted …"
...     },
...     links={
...         "comments": Link(
...             href="/articles/123/comments/",
...             title="Wild fires over there comments."
...         )
...     }
... )

```

then you can encode it using various media types, let's start simple:

```python
>>> print(serializers["application/json"].serialize(article).decode("UTF-8"))
{
    "title": "Wild fires over there",
    "body": "Firefighters spotted …",
    "comments": "/articles/123/comments/"
}

```

Or use `coreapi+json`:

```python
>>> print(serializers["application/vnd.coreapi+json"].serialize(article).decode("UTF-8"))
{
    "_type": "document",
    "_meta": {
        "url": "/articles/123/",
        "title": "Article"
    },
    "title": "Wild fires over there",
    "body": "Firefighters spotted \u2026",
    "comments": {
        "_type": "link",
        "url": "/articles/123/comments/",
        "title": "Wild fires over there comments.",
        "description": ""
    }
}

```

Or `application/hal+json`:

```python
>>> print(serializers["application/hal+json"].serialize(article).decode("UTF-8"))
{
    "title": "Wild fires over there",
    "body": "Firefighters spotted \u2026",
    "_links": {
        "self": {
            "href": "/articles/123/",
            "title": "Article"
        },
        "comments": {
            "href": "/articles/123/comments/",
            "title": "Wild fires over there comments."
        }
    }
}

```

Or HTML if it's a browser asking for it:

```python
>>> print(serializers["text/html"].serialize(article).decode("UTF-8"))
<div>
    <h1>Article</h1>
    <h2>/articles/123/</h2>
    <ul class="content">
        <li>
            Wild fires over there
        </li>
        <li>
            Firefighters spotted …
        </li>
    </ul>
    <h2>Links</h2>
    <ul class="links">
        <li>
            <div>
                <h2>Wild fires over there comments.</h2>
                <p>[] /articles/123/comments/</p>
                <p></p>
            </div>
        </li>
    </ul>
</div>

```
