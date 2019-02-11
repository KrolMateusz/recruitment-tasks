import sys
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError
from urllib.request import URLError
from bs4 import BeautifulSoup


def check_link(domain, link):
    http = 'http://'
    https = 'https://'
    link = link.get('href')
    if not (link.startswith(http) or link.startswith(https)):
        link = 'http://' + domain + link
    if not link.startswith(http + domain):
        return None
    return link


def get_domain(url):
    return urlparse(url).netloc


def get_title_of_page(url):
    try:
        source_code = urlopen(url).read()
        soup = BeautifulSoup(source_code, 'html.parser')
        return soup.title.string
    except (URLError, HTTPError):
        sys.stderr.write(f'Wrong url address: {url}\n')


def get_links_from_page(url):
    domain = get_domain(url)
    links = set([])
    try:
        source_code = urlopen(url).read()
        soup = BeautifulSoup(source_code, 'html.parser')
        for link in soup.find_all('a'):
            link = check_link(domain, link)
            if link:
                links.add(link)
        return set(links) - set([url])
    except (URLError, HTTPError):
        sys.stderr.write(f'Wrong url address: {url}\n')


def get_links_from_domain(url):
    domain = 'http://' + get_domain(url)
    links_to_check = set([domain])
    links_checked = set([])
    try:
        while links_checked != links_to_check:
            for link in get_links_from_page(url):
                links_to_check.add(link)
            links_checked.add(url)
            urls = links_to_check - links_checked
            if len(urls) > 0:
                url = urls.pop()
    except TypeError:
        sys.exit('No URLs to check')
    return links_checked


def site_map(url):
    domain_mapping = {}
    for link in get_links_from_domain(url):
        domain_mapping.setdefault(link, {get_title_of_page(link): get_links_from_page(link)})
    return domain_mapping


if __name__ == '__main__':
    web_url = 'http://127.0.0.1:8000/example.html'
    print(site_map(web_url))
