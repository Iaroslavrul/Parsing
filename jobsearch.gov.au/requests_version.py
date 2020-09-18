import requests
from lxml import html

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}


def get_regions():
    """ Получаю список id регионов, чтобы в дальнейшем отправлять POST запросы """
    r = requests.get('https://jobsearch.gov.au/job/search/', headers=HEADERS, timeout=60)
    tree = html.fromstring(r.text)
    regions = tree.xpath('//select[@id="Location"]/optgroup/option')
    regions = [region.get('value') for region in regions]
    return regions


def get_urls(regions):
    """ Последовательно для каждого региона загружаю страницу выдачи. Со страницы собираю ссылки на вакансии """
    result = []
    for region in regions:
        r = requests.post('https://jobsearch.gov.au/job/search/results',
                          headers=HEADERS,
                          timeout=60,
                          data={'Location': region})
        tree = html.fromstring(r.text)
        urls = tree.xpath('//div[@class="result-title"]/a/@href')
        result.extend(urls)
    return result


def main():
    regions = get_regions()
    urls = get_urls(regions)
    print(urls)
    print(len(urls))
    print(len(set(urls)))


if __name__ == '__main__':
    main()