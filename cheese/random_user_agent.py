from cheese.settings import FREE_PROXY_LIST
from cheese.user_agents_list import USER_AGENT_LIST
import random
from scrapy import log
import urllib
from lxml import etree
import StringIO

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

class RandomUserAgentMiddleware(object):
    
    def process_request(self, request, spider):
        ua  = random.choice(USER_AGENT_LIST)
        if ua:
            request.headers.setdefault('User-Agent', ua)
        proxy = random.choice(FREE_PROXY_LIST)
        request.meta['proxy'] = 'http://%s' % proxy
        #request.meta['proxy'] = 'http://64.90.59.115'
        #log.msg('>>>> UA %s'%request.headers)

if __name__ == '__main__':
    print get_free_proxy()
