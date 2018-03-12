# 此脚本基于 python 3.6 编写
import os
import glob
import re

def add_meta_viewport_as_needed(html):
  regex = re.compile('<meta name=\"viewport>\"')
  if (regex.search(html)):
    new_html = html
  else:
    new_html = html.replace('</head>','<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no\">\n</head>')
  return new_html

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
    html = load_root_index(index_file_path)
    new_html = add_meta_viewport_as_needed(html)
    rewrite_index_file(index_file_path, new_html)
    ret_val = 0
    sub_website_list = []
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
  ret_val = rebuild_youminds_website_index("D:/pim-wudi/tmp/youminds/test/头马俱乐部（TOASTMASTERS）.html")
  print(ret_val)
