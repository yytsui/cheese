from cheese.settings import OVER_WRITE_EXISTED_RECORD
from scrapy.conf import settings
from scrapy.exceptions import IgnoreRequest
import pymongo
from scrapy import log


def get_mongo_collection():
    connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
    db = connection[settings['MONGODB_DB']]
    collection = db[settings['MONGODB_COLLECTION']]
    return collection

mongo_collection = get_mongo_collection()

class NoOverWriteMiddleware(object):

    def process_request(self, request, spider):
        if OVER_WRITE_EXISTED_RECORD:
            return None
        else:
            if mongo_collection.find_one({'url': request.url, 'image_download_completed':True}):
                log.msg("%s existed and image download completed!, ignored." % request.url, log.INFO)
                raise IgnoreRequest

