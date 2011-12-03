from cheese.settings import FREE_PROXY_LIST
from cheese.user_agents_list import USER_AGENT_LIST
import random
from scrapy import log

class RandomUserAgentMiddleware(object):
    
    def process_request(self, request, spider):
        ua  = random.choice(USER_AGENT_LIST)
        if ua:
            request.headers.setdefault('User-Agent', ua)
        proxy = random.choice(FREE_PROXY_LIST)
        request.meta['proxy'] = 'http://%s' % proxy
        #request.meta['proxy'] = 'http://64.90.59.115'
        #log.msg('>>>> UA %s'%request.headers)
