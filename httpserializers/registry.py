"""Helper class and instance to pick the right serializer according to
an Accept header.
"""

from werkzeug.http import parse_accept_header


class Serializers(dict):
    """This class only holds available serializers as an easy to use dict."""

    def __init__(self, default, **kwargs):
        self.default = default
        super().__init__(**kwargs)

    def __getitem__(self, accept: str):
        """Find the best serializer for the given Accept header."""
        if not accept:
            return self.default
        media_type = parse_accept_header(accept).best_match(self.keys())
        if not media_type:
            return self.default
        return super().__getitem__(media_type)
