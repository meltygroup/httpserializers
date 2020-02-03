"""HTML Serializer.
"""

from jinja2 import Template


from httpserializers.types import Document, Link, Field
from httpserializers.utils import as_absolute
from httpserializers.registry import serializers


def _html_serializer(node, base_url=None):
    """Recursively serializes a document to HTML.
    """
    if isinstance(node, Document):
        ret = [
            Template("<div><h1>{{ title|e }}</h1>{{ url|urlize }}").render(
                url=as_absolute(base_url, node.url), title=node.title
            )
        ]
        ret.append("<ul class='document'>")
        ret.extend(
            [
                "<li>" + _html_serializer(value, base_url=base_url) + "</li>"
                for key, value in node.content.items()
            ]
        )
        ret.append("</ul>Links:")
        ret.append("<ul class='links'>")
        ret.extend(
            [
                "<li>" + _html_serializer(value, base_url=base_url) + "</li>"
                for key, value in node.links.items()
            ]
        )
        ret.append("</ul></div>")
        return "".join(ret)

    if isinstance(node, Link):
        ret = [
            Template(
                """<div><h2>{{ title|e }}</h2>
        {{ action|upper|e }}&nbsp;{{ url|urlize }}
            <p>{{ description|e }}</p>"""
            ).render(
                url=as_absolute(base_url, node.href),
                title=node.title,
                action=node.allow,
                description=node.description,
            )
        ]
        if node.fields:
            ret.append("Fields: <ul class='fields'>")
            ret.extend(
                [
                    "<li>" + _html_serializer(field, base_url=base_url) + "</li>"
                    for field in node.fields
                ]
            )
            ret.append("</ul>")
        ret.append("</div>")
        return "".join(ret)

    if isinstance(node, Field):
        return Template(
            """<div>{{ name }}
            {% if required %}(required){% endif %}
            {% if description %}<p>{{description}}</p>{% endif %}
            {% if schema %}
            <ul>
            {% for key, value in schema.items() %}
                <li>{{ key|e }}:&nbsp;{{ value|e }}</li>
            {% endfor %}
            </ul>
            {% endif %}"""
        ).render(
            name=node.name,
            required=node.required,
            schema=node.schema,
            description=node.description,
        )

    if isinstance(node, list):
        ret = ["<ul class='list'>"]
        ret.extend(
            [
                "<li>" + _html_serializer(value, base_url=base_url) + "</li>"
                for value in node
            ]
        )
        ret.append("</ul>")
        return "".join(ret)

    return node


@serializers(media_types={"text/html"}, default=True)
def html_serializer(node, base_url=None):
    """HTML serializer.
    """
    return _html_serializer(node, base_url).encode("UTF-8")
