# 此脚本基于 python 3.6 编写
import os
import shutil
import glob
import re

def add_meta_viewport_as_needed(html):
  regex = re.compile('<meta name=\"viewport\"')
  if (regex.search(html)):
    new_html = html
  else:
    new_html = html.replace('</head>','<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no\">\n</head>')
  return new_html
  
def remove_empty_tags_as_needed(html):
  regex = re.compile('<ul>[ \r\n]*</ul>')
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
    new_html = remove_empty_tags_as_needed(new_html)
    new_html = modify_svg_scale_as_needed(new_html)
    new_html = modify_svg_width_as_needed(new_html)
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
