from urllib.request import urlopen
from urllib.parse import urlparse
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


def get_all_links(url, page='all'):
    domain = urlparse(url).netloc
    links_to_check = set([url])
    links_checked = set([])
    while links_checked != links_to_check:
        source_code = urlopen(url).read()
        soup = BeautifulSoup(source_code, 'html.parser')
        for link in soup.find_all('a'):
            link = check_link(domain, link)
            if link:
                links_to_check.add(link)
        if page == 'current':
            return {soup.title.string: links_to_check - set([url])}
        links_checked.add(url)
        url = links_to_check - links_checked
        if len(url) >= 1:
            url = url.pop()
    return links_checked


def site_map(url):
    all_links = get_all_links(url)
    domain_mapping = {}
    for link in all_links:
        domain_mapping.setdefault(link, get_all_links(link, page='current'))
    return domain_mapping


if __name__ == '__main__':
    web_url = 'http://127.0.0.1:8000'
    site_map(web_url)
