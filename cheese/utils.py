def stringify_children(node):
    #http://stackoverflow.com/questions/4624062/get-all-text-inside-a-tag-in-lxml
    from itertools import chain
    parts = ([node.text] +
            list(chain(*([c.text, c.tail] for c in node.getchildren()))) +
            [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))

def get_text_or_none(ele):
    if ele is not None:
        return ele.text
    else:
        return None

def get_first_text_or_none(hxs , xpath):
    texts = hxs.select(xpath).extract()
    if texts:
        return texts[0]
    else:
        return None

#http://www.quora.com/How-do-you-print-a-python-unicode-data-structure
import pprint


class MyPP(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        ret = pprint.PrettyPrinter.format(self, object, context, maxlevels, level)
        if isinstance(object, unicode):
            ret = (object.encode('utf-8'), ret[1], ret[2])
        return ret

unicode_pprint = MyPP()

