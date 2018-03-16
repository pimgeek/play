# 此脚本基于 python 3.6 编写
import bs4
import glob
import html as htm
import markdown
import os
import re
import shutil

def new_html_soup_tag(html_div_code):
  temp_soup = bs4.BeautifulSoup(html_div_code, "html5lib")
  # BeautifulSoup automatically add <html> and <body> tags
  # There is only one 'div' tag, so it's the only member in the 'contents' list
  # new_tag = temp_soup.html.body.contents[0]
  # Or more simply
  div_tag = temp_soup.html.body.div
  return div_tag

def conv_desc_to_markdown_as_needed(html):
  html_soup = bs4.BeautifulSoup(html, "html5lib")
  desc_tag = html_soup.find("div", "description")
  md_to_html_tag = html_soup.find("div", id="desc_md_to_html")
  if (md_to_html_tag != None):
    new_html = html
  elif (desc_tag != None):
    regex_inner_html = re.compile("<div class=\"description\">(.+(?=<\/div>))<\/div>", re.DOTALL)
    result = regex_inner_html.search(desc_tag.prettify())
    if (result != None):
      new_desc_tag = new_html_soup_tag("<div id=\"desc_md_to_html\" class=\"description\">%s</div>" % htm.unescape(markdown.markdown(result.group(1))))
      desc_tag.replace_with(new_desc_tag)
      new_html = html_soup.prettify()
    else:
      new_html = html
  else:
    new_html = html
  return new_html

def conv_text_to_markdown_as_needed(html):
  html_soup = bs4.BeautifulSoup(html, "html5lib")
  text_tag = html_soup.find("div", "textcontent")
  md_to_html_tag = html_soup.find("div", id="textcontent")
  if (md_to_html_tag != None):
    new_html = html
  elif (text_tag != None):
    regex_inner_html = re.compile("<div class=\"textcontent\">[ \t\r\n]*<div>(.+(?=<\/div>))[ \t\r\n]*<\/div>[ \t\r\n]*<\/div>", re.DOTALL)
    result = regex_inner_html.search(text_tag.prettify())
    if (result != None):
      new_text_tag = new_html_soup_tag("<div id=\"text_md_to_html\" class=\"textcontent\"><div>%s</div></div>" % htm.unescape(markdown.markdown(result.group(1))))
      text_tag.replace_with(new_text_tag)
      new_html = html_soup.prettify()
    else:
      new_html = html
  else:
    new_html = html
  return new_html
  
def add_meta_viewport_as_needed(html):
  regex = re.compile('<meta name=\"viewport\"')
  if (regex.search(html)):
    new_html = html
  else:
    new_html = html.replace('</head>','<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no\">\n</head>')
  return new_html
  
def change_sitemap_label_as_needed(html):
  regex = re.compile('<a class=\'sitemap\'([^>]*)>[ \t\r\n]*Sitemap[ \t\r\n]*<\/a>', re.DOTALL)
  if (regex.search(html) == None):
    new_html = html
  else:
    new_html = re.sub(regex, '<a class=\'sitemap\'\g<1>>全站内容索引</a>', html)
  return new_html

def remove_empty_tags_as_needed(html):
  regex = re.compile('<ul>[ \t\r\n]*</ul>')
  if (regex.search(html) == None):
    new_html = html
  else:
    new_html = re.sub(regex, '', html)
  return new_html

def modify_svg_scale_as_needed(html):
  regex = re.compile('transform=\"scale\(1\.0 1\.0\)\"')
  if (regex.search(html) == None):
    new_html = html
  else:
    new_html = re.sub(regex, 'transform=\"scale(0.9 0.9)\"', html)
  return new_html
  
def modify_svg_width_as_needed(html):
  regex = re.compile('(svg style=\"[^\"]+\") width=\"([^"]+)\"')
  if (regex.search(html) == None):
    new_html = html
  else:
    result = regex.search(html)
    new_html = re.sub(regex, '%s width=\"\"' % result.group(1), html)
  return new_html

def add_navigation_label_as_needed(html):
  regex_no_change = re.compile('<div class=\'navigation\'>[ \t\r\n]*<div class=\'label\'')
  regex_has_nav = re.compile('<div class=\'navigation\'>[ \t\r\n]*<div>')
  regex_empty_nav = re.compile('<div class=\'navigation\'>[ \t\r\n]*<div>[ \t\r\n]*</div>')
  if (regex_has_nav.search(html) == None):
    new_html = html
  elif (regex_no_change.search(html) != None):
    new_html = html
  elif (regex_empty_nav.search(html) != None):
    result = regex_empty_nav.search(html)
    new_html = re.sub(regex_empty_nav, '', html)
  else:
    result = regex_has_nav.search(html)
    new_html = re.sub(regex_has_nav, '<div class=\'navigation\'>\n<div class=\'label\'>深入阅读</div>\n<div>', html)
  return new_html

def add_sitepath_label_as_needed(html):
  regex_no_change = re.compile('<div class=\'path\'>[ \t\r\n]*<div class=\'label\'')
  regex_sitepath = re.compile('<div class=\'path\'>[ \t\r\n]*<div>[ \t\r\n]*<a class=\'sitemap\'')
  if (regex_no_change.search(html) != None):
    new_html = html
  else:
    result = regex_sitepath.search(html)
    new_html = re.sub(regex_sitepath, '<div class=\'path\'>\n<div class=\'label\'>回溯阅读 / 关联阅读</div>\n<div>\n<a class=\'sitemap\'', html)
  return new_html

def apply_user_css(path):
  src_file = os.path.join(".", "styles.css")
  dest_file = os.path.join(path, "styles.css")
  if (os.path.isfile(dest_file)):
    shutil.copyfile(src_file, dest_file)
    ret_val = 0
  else:
    ret_val = -1
  return ret_val

def load_root_index(path):
  fh = open(path, encoding='utf8')
  lines = list(fh.readlines())
  content = "".join(lines)
  fh.close()
  return content
  
def rewrite_index_file(path, content):
  fh = open(path, "w", encoding='utf8')
  fh.write(content)
  fh.close()
  return 0

def rebuild_youminds_website_index(index_file_path):
  if (index_file_path[-5:] != ".html"):
    err_msg = "给定文件不是 YouMinds Website 格式！\n"
    print(err_msg)
    ret_val = -1
  else:
    new_html = load_root_index(index_file_path)
    new_html = add_meta_viewport_as_needed(new_html)
    new_html = change_sitemap_label_as_needed(new_html)
    new_html = remove_empty_tags_as_needed(new_html)
    new_html = conv_desc_to_markdown_as_needed(new_html)
    new_html = conv_text_to_markdown_as_needed(new_html)
    new_html = modify_svg_scale_as_needed(new_html)
    new_html = modify_svg_width_as_needed(new_html)
    new_html = add_navigation_label_as_needed(new_html)
    new_html = add_sitepath_label_as_needed(new_html)
    rewrite_index_file(index_file_path, new_html)
    # 以上函数调用也应返回错误信息，以后再修改
    ret_val = apply_user_css(os.path.dirname(index_file_path))
    youminds_website_name = index_file_path[0:-5]
    if (os.path.isdir(youminds_website_name)):
      sub_youminds_websites = glob.glob(os.path.join(youminds_website_name, "*.html"))
      # traverse dir recursively
      for sub_website_index_path in sub_youminds_websites:
        ret_val = rebuild_youminds_website_index(sub_website_index_path)
        if (ret_val != 0):
          break
        else:
          pass
    else:
      pass
  return ret_val

if __name__ == '__main__':
  ret_val = rebuild_youminds_website_index("D:/pim-wudi/tmp/www/youminds_export/pub.html")
  print(ret_val)
