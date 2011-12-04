from cheese.user_agents_list import USER_AGENT_LIST
import random
from scrapy import log
from lxml import etree
import datetime

def get_free_proxy():
    url =  "http://hidemyass.com/proxy-list/search-225783/"
    parser = etree.HTMLParser()
    tree = etree.parse(url, parser)
    #/html/body/div/div/table/tbody/tr[2]/td[2]/span
    proxies = []
    xpath = "id('listtable')/tr"
    proxy = tree.xpath(xpath)
    for p in proxy[:20]:
        ip = p.find('td[2]/span').text
        port = p.find('td[3]').text.strip()
        http_proxy = 'http://%s:%s' % (ip, port)
        proxies.append(http_proxy)
    return proxies

class RandomUserAgentProxyMiddleware(object):
    count = 0
    period_start_time = datetime.datetime.now()
    proxy_list = get_free_proxy()

    def process_request(self, request, spider):
        ua  = random.choice(USER_AGENT_LIST)
        if ua:
            request.headers.setdefault('User-Agent', ua)
        free_proxy = random.choice(self.proxy_list)
        request.meta['proxy'] = free_proxy
        log.msg("Change proxy to %s" % free_proxy, log.INFO)
        self.refresh_proxy_list()

    def refresh_proxy_list(self, minutes=10):
        time_delta = datetime.datetime.now() - self.period_start_time
        if time_delta.seconds > 10:
            self.proxy_list = get_free_proxy()
            self.period_start_time = datetime.datetime.now()


if __name__ == '__main__':
    print get_free_proxy()
