#!/usr/local/bin/python

import sys
import os
import base64
import pypandoc
import shortuuid
import xml.etree.ElementTree as xmlET

os.environ.setdefault('PYPANDOC_PANDOC', 'C:/Users/pimgeek/AppData/Local/Pandoc/pandoc.exe')

# 获取当前卡片盒的所有属性
def get_cardbox_all_attrs(cardbox):
    props_dict = { 'description': '' }
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

# 获取当前卡片盒的备注信息（若有嵌入图片，也要导出）
def get_cardbox_content(cardbox):
    content_dict = { 'text': '', 'stream':'' }
    content = cardbox.find('content')
    if content != None:
        if content.get('contentrepresentation') == 'text' and \
            content.get('styledtext') == 'true':
            content_dict['text'] = content.find('text').text
            content_dict['styledtext'] = content.find('styledtext').text
        if content.get('contentrepresentation') == 'text' and \
            content.get('styledtext') == None:
            content_dict['text'] = content.text
        elif content.get('contentrepresentation') == 'stream':
            content_dict['stream'] = content.text
            content_dict['imgtype'] = content.get('mimetype').rsplit('/',1)[-1]
    return content_dict

# 获取当前卡片盒的子卡片盒列表
def get_sub_cardbox_list(cardbox):
    if cardbox == None or \
        cardbox == False or \
        cardbox.find('childs') == None:
        return []
    else:
        return cardbox.find('childs').getchildren()

# 按指定的层次，递归地获取卡片盒中的内容
def pafx2md_by_level(cardbox, level):
    md_list = []
    sub_md_list = []
    if (cardbox == None or cardbox == False):
        return []
    elif (level < 0 or level > 5):
        print("level 数值超出范围（必须是小于 6 的正整数）...")
        return []
    else:
        cardbox_attr_dict = get_cardbox_all_attrs(cardbox)
        cardbox_content_dict = get_cardbox_content(cardbox)
        md_list.append("# " + cardbox_attr_dict['name'])
        if cardbox_attr_dict['description'] != '':
            md_list.append(cardbox_attr_dict['description'] + "\n\n")
        if cardbox_content_dict['text'] != '':
            md_list.append(cardbox_content_dict['text'] + "\n\n")
        if cardbox_content_dict['stream'] != '':
            md_list.append("![img]|%s.%s|%s" % (shortuuid.uuid(), cardbox_content_dict['imgtype'], cardbox_content_dict['stream']))
        sub_cardbox_list = get_sub_cardbox_list(cardbox)
        if (level == 0 or len(sub_cardbox_list) == 0):
            pass
        else:
            for sub_cardbox in sub_cardbox_list:
                sub_md_list += pafx2md_by_level(sub_cardbox, level - 1)
    md_list += list(map(markdown_indent, sub_md_list))
    return md_list

def export_cardbox_in_ascii(cardbox):
    ascii_str = ''
    if cardbox != None:
        cardbox_attr_dict = get_cardbox_all_attrs(cardbox)
        cardbox_content_dict = get_cardbox_content(cardbox)
        ascii_str += '  ┌────────────────────────────────────\n'
        if 'name' in cardbox_attr_dict.keys():
            ascii_str += "  |卡片盒标题：%s\n" % cardbox_attr_dict['name']
        if 'description' in cardbox_attr_dict.keys():
            ascii_str += "  |卡片盒简介：%s\n" % cardbox_attr_dict['description']
        if 'text' in cardbox_attr_dict.keys():
            ascii_str += "  |卡片盒备注：%s\n" % cardbox_attr_dict['text']
        if 'styledtext' in cardbox_attr_dict.keys():
            ascii_str += "  |卡片盒备注（富文本）：%s\n" % cardbox_attr_dict['styledtext'][-10:]
        if 'stream' in cardbox_content_dict.keys():
            ascii_str += "  |卡片盒内嵌图片：%s\n" % cardbox_content_dict['stream'][-10:]
        ascii_str += '  └──────────────────────────────────── \n'
    else:
        pass
    return ascii_str
    
def markdown_indent(md_str):
    if md_str != None and md_str.startswith('#'):
        md_str = '#' + md_str;
    else:
        pass
    return md_str

def write_markdown(md_list, outdir, outfilename):
    if os.path.isdir(outdir):
        deltree(outdir)
    else:
        os.mkdir(outdir)
    md_fh = open(os.path.join(outdir, outfilename), "w+", encoding="utf-8")
    for md_str in md_list:
        if md_str.startswith('![img]'):
            img_data = md_str.split('|')
            md_fh.write("%s(%s)\n\n" % (img_data[0], img_data[1]))
            img_fh = open(os.path.join(outdir, img_data[1]), "wb+")
            img_fh.write(base64.b64decode(img_data[2]))
            img_fh.close()
        else:
            md_fh.write(md_str + "\n")
    md_fh.close()
    return
        
def deltree(dir):
    if os.path.isdir(dir):
        files = os.listdir(dir)
        for file in files:
            os.remove(os.path.join(dir, file))
    else:
        pass

# begin main script

files = sys.argv[1:]

for file in files:
    file_name = os.path.basename(file).rsplit('.', 1)[0]
    file_dir = os.path.join(os.path.dirname(file), file_name)
    md_filename = file_name + os.extsep + 'md'
    docx_filename = file_name + os.extsep + 'docx'
    pafx_obj = xmlET.parse(file).getroot()
    root_cardbox = pafx_obj[0][0]
    # print('\n╔══════════ %s' % file)
    # for cardbox in get_sub_cardbox_list(root_cardbox):
    #     print(export_cardbox_in_ascii(cardbox))
    # print('\n╚══════════════════════════════')
    md_list = pafx2md_by_level(root_cardbox, 5)
    write_markdown(md_list, file_dir, md_filename)
    os.chdir(file_dir)
    output = pypandoc.convert(md_filename, format="md", to='docx', \
        outputfile=docx_filename)
    print(output)
