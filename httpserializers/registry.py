"""Helper class and instance to pick the right serializer according to
an Accept header.
"""
from typing import Set

from werkzeug.http import parse_accept_header


class Serializers(dict):
    """This class only holds available serializers as an easy to use dict.
    """

    def __init__(self, **kwargs):
        self.default = None
        super().__init__(**kwargs)

    def __call__(self, media_types: Set[str], default: bool):
        """Register a new serializer with a set of accepted media types.
        """

        def _(serializer):
            serializer.media_types = media_types
            for media_type in media_types:
                self[media_type] = serializer
            if default:
                self.default = serializer
            return serializer

        return _

    def __getitem__(self, accept: str):
        """Find the best serializer for the given Accept header.
        """
        if not accept:
            return self.default
        media_type = parse_accept_header(accept).best_match(self.keys())
        if not media_type:
            return self.default
        return super().__getitem__(media_type)


serializers = Serializers()  # pylint: disable=invalid-name
