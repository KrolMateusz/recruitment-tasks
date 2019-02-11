import sys
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError
from urllib.request import URLError
from bs4 import BeautifulSoup


def check_link(domain, link):
    """Returns link within domain.

    If a link was without http protocol and domain, function automatically
    adds these elements.

    :param str domain: domain of the website
    :param str link: link to the website
    :return None or str: None if link does not belong to given domain
    """
    http = 'http://'
    https = 'https://'
    link = link.get('href')
    # avoiding anchor links
    if '#' in link:
        return None
    # adding http and domain if only endpoint was given e.g. /site.html
    if not (link.startswith(http) or link.startswith(https)):
        link = 'http://' + domain + link
    if not link.startswith(http + domain):
        return None
    return link


def get_domain(url):
    """Returns domain of URL address.

    :param str url: URL address
    :return str: domain of website
    """
    return urlparse(url).netloc


def get_title_of_page(url):
    """Returns title of page.

    :param str url: URL address
    :return str: title of website
    """
    # checks if URL address can be opened
    try:
        source_code = urlopen(url).read()
        soup = BeautifulSoup(source_code, 'html.parser')
        return soup.title.string
    except (URLError, HTTPError):
        sys.stderr.write(f'Wrong url address: {url}\n')


def get_links_from_page(url):
    """Returns set of all links within same domain as url on website.

    :param str url: URL address
    :return set: all unique links
    """
    domain = get_domain(url)
    links = set([])
    # checks if URL address can be opened
    try:
        source_code = urlopen(url).read()
        soup = BeautifulSoup(source_code, 'html.parser')
        # checks every link on page
        for link in soup.find_all('a'):
            link = check_link(domain, link)
            # if link is correct, it is adding to set
            if link:
                links.add(link)
        return set(links) - set([url])
    except (URLError, HTTPError):
        sys.stderr.write(f'Wrong url address: {url}\n')


def get_links_from_domain(url):
    """Returns set of all links on all pages within domain.

    :param str url: URL address
    :return set: set of all unique links on domain
    """
    domain = 'http://' + get_domain(url)
    links_to_check = set([domain])
    links_checked = set([])
    try:
        # every iteration checked URL address is added to links_checked. When
        # links_checked is the same as set links_to_check, means that all
        # links were checked and they are returned.
        while links_checked != links_to_check:
            for link in get_links_from_page(url):
                links_to_check.add(link)
            links_checked.add(url)
            # urls to check are difference two sets, which means pages that
            # were not extracted
            urls = links_to_check - links_checked
            if len(urls) > 0:
                url = urls.pop()
    except TypeError:
        sys.exit('No URLs to check')
    return links_checked


def site_map(url):
    """Returns mapping of domain.

    Mapping of domain is dictionary with URL as key, and dictionary as value.
    Nested dictionary contains of site title as key and set of links as value.
    E.g. {'Index': {'http://127.0.0.1:8000/site.html',
    'http://127.0.0.1:8000/example.html'}}

    :param url:
    :return:
    """
    domain_mapping = {}
    for link in get_links_from_domain(url):
        domain_mapping.setdefault(link, {
            get_title_of_page(link): get_links_from_page(link)
        })
    return domain_mapping


if __name__ == '__main__':
    web_url = 'http://127.0.0.1:8000'
    print(site_map(web_url))
