from urllib.parse import urljoin


def as_absolute(base, url):
    """Ensure an URL is absolute on the given base.
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        return urljoin(base, url)
    return url
