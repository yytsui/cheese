import pymongo
import os.path

MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'thechef2'
MONGODB_COLLECTION = 'recipes'

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))

IMAGES_STORE =  '%s/image_store' % CURRENT_PATH


def check_pictures():
    connection = pymongo.Connection(MONGODB_SERVER, MONGODB_PORT)
    db = connection[MONGODB_DB]
    for r in db.recipes.find():
    #for r in db.recipes.find({'url':'http://icook.tw/recipes/15092'}):
        for img_url in r['image_urls']:
            for img in r['images']:
                if img_url == img['url']:
                    abs_path = '%s/%s' % (IMAGES_STORE, img['path'])
                    if os.path.isfile(abs_path) is False:
                        print "%s is not existed!" % abs_path
                    else:
                        #print "%s done!" % abs_path
                        pass

        _images = [ s['picture'] for s in r['steps'] if s['picture']] + [r['main_picture']]
        final_save_image_urls = [m['url'] for m in r['images']]
        if len(_images) != len(r['images']):
            print r['url'], ' ', len(_images), len(final_save_image_urls)
            """
            print _images,
            print "-"*100
            print final_save_image_urls
            print "="*100
            """
            for i in _images:
                if i not in final_save_image_urls:
                    print i
        else:
            print '%s good!' % r['url']
        print "-" * 100


def check_url_uniquness():
    connection = pymongo.Connection(MONGODB_SERVER, MONGODB_PORT)
    db = connection[MONGODB_DB]
    for r in db.recipes.find():
        try:
            assert db.recipes.find({'url': r['url']}).count() == 1
        except AssertionError:
            print '%s failed to pass uniquness test' % r['url']
            raise
    print "url uniquness check pass."


if __name__ == '__main__':
    #check_pictures()
    check_url_uniquness()
