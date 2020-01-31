from typing import Optional, Union, List, Dict, Sequence, Any


class Document:
    """An API response.

    Expresses the data that the client may access,
    and the actions that the client may perform.
    """

    def __init__(
        self,
        url: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        media_type: Optional[str] = None,
        content: Optional[Dict[str, Any]] = None,
    ):  # pylint: disable=too-many-arguments
        content = {} if (content is None) else content

        self.url = "" if (url is None) else url
        self.title = "" if (title is None) else title
        self.description = "" if (description is None) else description
        self.media_type = "" if (media_type is None) else media_type
        self.data = content


class Field:
    """API Field, represent a key and a value in a document.
    Schema conforms to http://spec.openapis.org/oas/v3.0.2
    """

    def __init__(
        self, name=False, required="", location=None, schema=None, description=None,
    ):  # pylint: disable=too-many-arguments
        self.name = name
        self.schema = schema
        self.required = required
        self.location = location
        self.description = description


class Link:
    """Links represent the actions that a client may perform.
    """

    def __init__(
        self,
        url: str,
        action: str = None,
        encoding: str = None,
        transform: str = None,
        title: str = None,
        description: str = None,
        fields: List[Union[Field, str]] = None,
    ):  # pylint: disable=too-many-arguments
        self.url = url
        self.action = "" if (action is None) else action
        self._encoding = "" if (encoding is None) else encoding
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
