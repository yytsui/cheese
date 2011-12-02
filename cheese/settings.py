# Scrapy settings for cheese project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'cheese'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['cheese.spiders']
NEWSPIDER_MODULE = 'cheese.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

#http://www.useragentstring.com/pages/useragentstring.php
USER_AGENT_LIST = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110613 Firefox/6.0a2',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7'
]

DOWNLOADER_MIDDLEWARES = {
    'cheese.random_user_agent.RandomUserAgentMiddleware': 400,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
}

