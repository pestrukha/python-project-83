from urllib.parse import urlparse
import validators


def normalize_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def validate_url(url):
    if len(url) > 255:
        return 'URL больше 255 символов'
    elif validators.url(url) is not True:
        return 'Некорректный URL'
