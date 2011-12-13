from cheese.user_agents_list import USER_AGENT_LIST
from cheese.settings import USE_PROXY, RANDOM_AGENT
import random
from scrapy import log
from lxml import etree

def get_free_proxy():
    #TODO: set user-agent
    #http://pzwart3.wdka.hro.nl/wiki/Simple_Web_Spider_in_Python

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
    def process_request(self, request, spider):
        if RANDOM_AGENT:
            ua  = random.choice(USER_AGENT_LIST)
        else:
            ua = USER_AGENT_LIST[0]
        if ua:
            request.headers.setdefault('User-Agent', ua)

        if USE_PROXY:
            if self.count % 200 == 0:
                #TODO: save proxies first time, and choose from there, mabybe only get proxies again after every 1000 times.
                free_proxy = random.choice(get_free_proxy())
                request.meta['proxy'] = free_proxy
                log.msg("Change proxy to %s" % free_proxy, log.INFO)
            self.count += 1
        log.msg("Request Headers %s" % request.headers, log.INFO)

if __name__ == '__main__':
    print get_free_proxy()
