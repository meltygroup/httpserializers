"""Serialize using the JSON-Home format
https://mnot.github.io/I-D/json-home/.
"""
import json

from httpserializers.utils import as_absolute


class JSONHomeSerializer:
    """JSON-Home serializer."""

    media_type = "application/json-home"

    def serialize(self, document, base_url: str, path, schema) -> str:
        """Serialize a Document to the JSON-home format."""
        home = {
            "api": {
                "title": schema["info"]["title"],
                "links": {
                    "author": schema["info"]["contact"]["name"],
                    "describedBy": "",
                },
            },
            "resources": {},
        }
        for path, path_desc in schema["paths"].items():
            home["resources"][path.strip("/")] = {
                "href": as_absolute(base_url, path),
                "hints": {"allow": [key.upper() for key in path_desc.keys()]},
            }
        return json.dumps(home, indent=4)
