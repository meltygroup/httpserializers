"""HTML Serializer.
"""

import json

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter

from functools import lru_cache
from jinja2 import Template
from httpserializers.utils import as_absolute

HTML = Template(
    """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{{title|e}}</title>
  {{ style }}
</head>
<body>
  <h1>Content</h1>
  {{content}}
  <h1>OpenAPI section</h1>
  {{schema}}
</body>
</html>"""
)


@lru_cache(1)
def get_pygments_style():
    html = highlight("[]", JsonLexer(), HtmlFormatter(full=True))
    return (
        '<style type="text/css">'
        + html.split('<style type="text/css">')[1].split("</style>")[0]
        + "</style>"
    )


def _html_serializer(node, base_url, path, schema):
    """Serializes a document to HTML."""
    content = json.dumps(node, indent=4)
    node_schema = json.dumps(schema["paths"][path], indent=4)
    return HTML.render(
        title=schema["info"]["title"],
        style=get_pygments_style(),
        content=highlight(content, JsonLexer(), HtmlFormatter()),
        schema=highlight(node_schema, JsonLexer(), HtmlFormatter()),
    )


class HTMLSerializer:
    """HTML serializer."""

    media_type = "text/html"

    def serialize(self, document, base_url: str, path, schema) -> str:
        """Serializes a document to HTML."""
        return _html_serializer(document, base_url, path, schema)
