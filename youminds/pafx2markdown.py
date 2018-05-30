#!/usr/local/bin/python

import sys
import xml.etree.ElementTree as xmlET

def get_cardbox_all_attrs(cardbox):
    props_dict = {}
    props = cardbox.find('properties')
    if props != None:
        for prop in props:
            prop_subnodes = prop.getchildren()
            if len(prop_subnodes) > 0 and \
                prop_subnodes[0].tag == 'value':
                props_dict[prop.get('symbolname')] = prop_subnodes[0].text
            else:
                pass
    else:
        pass
    return props_dict  
def get_cardbox_content(cardbox):
    content_dict = {}
    content = cardbox.find('content')
    if content != None:
        print(content.get('symbolname'))
        if content.get('contentrepresentation') == 'text' and \
            content.get('styledtext') == 'true':
            content_dict['text'] = content.find('text').text
            content_dict['styledtext'] = content.find('styledtext').text
        if content.get('contentrepresentation') == 'text' and \
            content.get('styledtext') == None:
            content_dict['text'] = content.text
        elif content.get('contentrepresentation') == 'stream':
            content_dict['stream'] = content.text
    return content_dict
def get_sub_cardbox_list(cardbox):
    return
def pafx2md_by_level(cardbox, level):
    return

# begin main script

files = sys.argv[1:]

for file in files:
    pafx_obj = xmlET.parse(file).getroot()
    root_cardbox = pafx_obj[0][0]
    for cardbox in root_cardbox.findall('childs')[0].getchildren():
        print("======== %s ========" % cardbox.get('id'))
        # cardbox_attr_dict = get_cardbox_all_attrs(cardbox)
        cardbox_content_dict = get_cardbox_content(cardbox)
        if 'text' in cardbox_content_dict.keys():
            print(cardbox_content_dict['text'])
        if 'styledtext' in cardbox_content_dict.keys():
            print(cardbox_content_dict['styledtext'][-5:])
        if 'stream' in cardbox_content_dict.keys():
            print(cardbox_content_dict['stream'][-5:])