import pymongo
import os.path
import os
import sys

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

def count_stat():
    connection = pymongo.Connection(MONGODB_SERVER, MONGODB_PORT)
    db = connection[MONGODB_DB]
    total = db.recipes.find().count()
    image_download_not_completed = db.recipes.find({'image_download_completed': False}).count()
    percentage = float(image_download_not_completed)/total * 100
    print "total %d, image_download_not_completed %d, failed rate %.2f%%" % (total, image_download_not_completed, percentage )
    return percentage


def check_no_images():
    connection = pymongo.Connection(MONGODB_SERVER, MONGODB_PORT)
    db = connection[MONGODB_DB]
    count = 0
    for r in db.recipes.find():
        if len(r['images']) == 0:
            count += 1

    print '%d recipes do not have any images!' % count
    return count


def keep_running():
    count = 0
    fail_percentage = count_stat()
    number_of_no_images = check_no_images()
    while fail_percentage > 1 or number_of_no_images > 100:
        os.system('scrapy crawl ytower --logfile=/tmp/crawl.log')
        #os.system('scrapy crawl icooktw')
        #os.system('scrapy crawl cookshow')
        #os.system('scrapy crawl dodocook')
        count += 1
        print "finished %d run" % count
        print "-"*150
        fail_percentage = count_stat()
        number_of_no_images = check_no_images()


if __name__ == '__main__':
    #check_pictures()
    #check_url_uniquness()
    #count_stat()
    #check_no_images()
    if len(sys.argv) > 1 and sys.argv[1] == '-c':
        print 'checking...'
        check_url_uniquness()
        count_stat()
        check_no_images()
    else:
        keep_running()
