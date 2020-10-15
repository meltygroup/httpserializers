"""Exposes types for httpserializers: Document, Link, and Field.
"""

from abc import ABC, abstractmethod
from typing import Optional, Union, List, Sequence, Any, Mapping


class Field:
    """API Field, represent a key and a value in a document.
    Schema conforms to http://spec.openapis.org/oas/v3.0.2
    """

    def __init__(
        self, name=False, required="", location=None, schema=None, description=None
    ):  # pylint: disable=too-many-arguments
        self.name = name
        self.schema = schema
        self.required = required
        self.location = location
        self.description = description


class Link:  # pylint: disable=too-many-instance-attributes
    """Links represent the actions that a client may perform.
    Parameters:
    - allow: The list of methods allowed on this link, like: ["GET", "DELETE"]
    - formats: List of representations types that the resource make available.
    """

    def __init__(
        self,
        href: str = None,
        href_template: str = None,
        href_vars: Mapping[str, str] = None,
        allow: Sequence[str] = None,
        formats: Sequence[str] = None,
        transform: str = None,
        title: str = None,
        description: str = None,
        fields: List[Union[Field, str]] = None,
    ):  # pylint: disable=too-many-arguments
        self.href = href
        self.href_template = href_template
        self.href_vars = href_vars
        if href and href_template:
            raise ValueError("Please choose between href or href_template.")
        self.allow = allow or []
        self.formats = formats or []
        self.transform = "" if (transform is None) else transform
        self.title = "" if (title is None) else title
        self.description = "" if (description is None) else description
        if fields is None:
            self.fields: Sequence[Field] = []
        else:
            self.fields = [
                item
                if isinstance(item, Field)
                else Field(item, required=False, location="")
                for item in fields
            ]


class Attribute:
    def __init__(self, IRI, default=None, schema=None):
        """Schema conforms to http://spec.openapis.org/oas/v3.0.2

        with an extra string format being: "url".
        """
        self.IRI = IRI
        self.default = default
        self.schema = schema

    def __get__(self, instance, owner=None):
        return instance._content.get(self.name, self.default)

    def __set__(self, instance, value):
        instance._content[self.name] = value

    def __delete__(self, instance):
        del instance._content[self.name]

    def __set_name__(self, owner, name):
        self.name = name


class Document:
    """An API response.

    Expresses the data that the client may access,
    and the actions that the client may perform.

    It's not a good idea to use this class directly, better inherit
    from Document to specify default values, context, links, fields a
    single time, to use it later.
    """

    def __init__(
        self,
        url: Optional[str] = None,
        # title: Optional[str] = None, # Deprecated, use class name.
        description: Optional[str] = None,
        # content: Optional[Mapping[str, Any]] = None,
        # links: Optional[Mapping[str, Link]] = None,
        **kwargs
    ):  # pylint: disable=too-many-arguments
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.url = "" if (url is None) else url
        self.description = "" if (description is None) else description

    def items(self):
        for key, value in self._content.items():
            yield key, value


class Serializer(ABC):
    """Base class for all serializers."""

    media_type: str = ""

    @abstractmethod
    def serialize(self, document: Document, base_url: str = None) -> bytes:
        """Serializers should implement this method."""
