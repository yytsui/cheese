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
    'cheese.already_existed.NoOverWriteMiddleware': 399,
    'cheese.random_user_agent.RandomUserAgentProxyMiddleware': 400,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
}

MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'thechef'
MONGODB_COLLECTION = 'recipes'

import os.path
CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))

IMAGES_STORE =  '%s/image_store' % CURRENT_PATH

ITEM_PIPELINES = [
    'cheese.pipelines.IgnoreVisitedItems',
    'scrapy.contrib.pipeline.images.ImagesPipeline',
    'cheese.pipelines.MongoDBPipeline',
]

OVER_WRITE_EXISTED_RECORD = False
