from cheese.user_agents_list import USER_AGENT_LIST
from cheese.settings import USE_PROXY, RANDOM_AGENT
import random
from scrapy import log
from lxml import etree

def get_free_proxies():
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
        http_proxy = 'http://60.11.62.176:8088'
        proxies.append(http_proxy)
    return proxies

class RandomUserAgentProxyMiddleware(object):
    count = 0
    #free_proxies = ['http://209.62.12.130:8118']
    #http://spys.ru/en/
    #http://spys.ru/en/anonymous-proxy-list/
    #free_proxies = ['http://211.86.157.95:3128', 'http://213.234.239.90:3128', 'http://190.255.49.38:6588']
    free_proxies = ['http://213.234.239.90:3128']
    ua = USER_AGENT_LIST[0]
    def process_request(self, request, spider):
        if RANDOM_AGENT:
            if self.count % 200 == 0:
                self.ua  = random.choice(USER_AGENT_LIST)
        request.headers.setdefault('User-Agent', self.ua)

        if USE_PROXY:
            if self.count % 200 == 0:
                #TODO: save proxies first time, and choose from there, mabybe only get proxies again after every 1000 times.
                free_proxy = random.choice(self.free_proxies)
                request.meta['proxy'] = free_proxy
                log.msg("Change proxy to %s" % free_proxy, log.INFO)
            #if self.count % 2000 == 0:
                #self.free_proxy = get_free_proxies()
        
        log.msg("Request Headers %s" % request.headers, log.INFO)

if __name__ == '__main__':
    print get_free_proxies()
