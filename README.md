# Http Serializers

This projects try to unify different media types, like:

- [HAL](https://www.ietf.org/archive/id/draft-kelly-json-hal-08.txt).
- [coreapi+json](https://www.coreapi.org/specification/encoding/).
- Plain old HTML, just in case you're on a web browser.
- Simple JSON, in case your documentation is out of band and you want the bare minimum.
- [JSON-home](https://mnot.github.io/I-D/json-home/).
- Any other if you implement them.


## Example usage

Imagine a simple document describing an article, having a title, a
body, and a link to its comments, you can describe it using simple
Python:

```python
>>> from httpserializers import Document, Link

>>> article = Document(
...     title="Article",
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
>>> from httpserializers import json_serializer
>>> print(json_serializer(article).decode("UTF-8"))
{
    "title": "Wild fires over there",
    "body": "Firefighters spotted …",
    "comments": "/articles/123/comments/"
}

```

Or use `coreapi+json`:

```python
>>> from httpserializers import coreapi_serializer
>>> print(coreapi_serializer(article).decode("UTF-8"))
{
    "_type": "document",
    "_meta": {
        "url": "",
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
