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
#http://snippets.scrapy.org/snippets/27/
#http://groups.google.com/group/scrapy-users/browse_thread/thread/997f5dd39a9c670f
#http://hidemyass.com/proxy-list/

USE_PROXY = True
RANDOM_AGENT = True

DOWNLOADER_MIDDLEWARES = {
    'cheese.random_user_agent.RandomUserAgentProxyMiddleware': 400,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
}

ITEM_PIPELINES = [
    'cheese.pipelines.RecipePipeline',
]

def setup_django_env(path):
    import imp
    from django.core.management import setup_environ

    f, filename, desc = imp.find_module('settings', [path])
    project = imp.load_module('settings', f, filename, desc)

    setup_environ(project)

setup_django_env('/Users/ytsui/try/dumpling/rcheese/')


