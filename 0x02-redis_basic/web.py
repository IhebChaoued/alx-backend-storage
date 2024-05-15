#!/usr/bin/env python3
"""web"""
import requests
import redis


def track_and_cache(func):
    """Decorator to track URL access count and cache the result."""
    def wrapper(url):
        """Wrapper function to track URL access count and cache result."""
        r = redis.Redis()

        url_key = f"count:{url}"
        r.incr(url_key)

        cached_content = r.get(url)
        if cached_content:
            return cached_content.decode('utf-8')

        response = requests.get(url)
        html_content = response.text

        r.setex(url, 10, html_content)

        return html_content

    return wrapper


@track_and_cache
def get_page(url: str) -> str:
    """Get the HTML content of a URL."""
    return requests.get(url).text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    print(get_page(url))
