"""HTML Serializer.
"""

from jinja2 import Template


from httpserializers.types import Document, Link, Field, Serializer
from httpserializers.utils import as_absolute


def _html_serializer(node, base_url=None):
    """Recursively serializes a document to HTML."""
    if isinstance(node, Document):
        return Template(
            """
{%- macro document(node) -%}
<div>
    <h1>{{ node.title|e }}</h1>
    <h2>{{ as_absolute(node.url)|urlize }}</h2>
    <ul class="content">
        {% for c in node.content.values() %}
        <li>
            {{ dispatch(c)|indent(12) }}
        </li>
        {% endfor %}
    </ul>
    <h2>Links</h2>
    <ul class="links">
        {% for link in node.links.values() %}
        <li>
            {{ dispatch(link)|indent(12) }}
        </li>
        {% endfor %}
    </ul>
</div>
{%- endmacro -%}

{%- macro link(node) -%}
<div>
    <h2>{{ node.title|e }}</h2>
    <p>{{ node.allow|upper|e }} {{ as_absolute(node.href)|urlize }}</p>
    <p>{{ node.description|e }}</p>
    {% if node.fields %}
        <ul class="fields">
            {% for field in node.fields %}
            <li>
              {{ field }}
            </li>
            {% endfor %}
        </ul>
    {% endif %}
</div>
{%- endmacro -%}

{%- macro field(node) -%}
<div>
    <h2>{{ node.name|e }} {% if node.required %}(required){% endif %}</h2>
    {% if description %}
        <p>{{description}}</p>
    {% endif %}
    {% if node.schema %}
        <ul>
        {% for key, value in node.schema.items() %}
            <li>{{ key|e }}: {{ value|e }}</li>
        {% endfor %}
        </ul>
   {% endif %}
</div>
{%- endmacro -%}

{%- macro list(node) -%}
<ul class="list">
    {% for value in node -%}
        <li>
            {{ dispatch(value)|indent(12) }}
        </li>
    {%- endfor %}
</ul>
{%- endmacro -%}

{%- macro dispatch(node) -%}
    {%- if isinstance(node, Document) -%} {{ document(node) }}
    {%- elif isinstance(node, Link) -%} {{ link(node) }}
    {%- elif isinstance(node, Field) -%} {{ field(node) }}
    {%- elif isinstance(node, _list) -%} {{ list(node) }}
    {%- else -%} {{ node }}
    {%- endif -%}
{%- endmacro -%}
{{- dispatch(node) -}}""",
            trim_blocks=True,
            lstrip_blocks=True,
        ).render(
            node=node,
            type=type,
            isinstance=isinstance,
            Document=Document,
            Link=Link,
            Field=Field,
            _list=list,
            as_absolute=lambda url: as_absolute(base_url, url),
            base_url=base_url,
        )


class HTMLSerializer(Serializer):
    """HTML serializer."""

    media_type = "text/html"

    def serialize(self, document: Document, base_url: str = None) -> bytes:
        """Serializes a document to HTML."""
        return _html_serializer(document, base_url).encode("UTF-8")
