import os
import re
import glob

def load_zim_file(path):
  fh = open(path, encoding='utf8')
  lines = list(fh.readlines())
  return lines
  
def get_zim_file_title(title_line):
  regex_str = re.compile('={6}[ ]+([^ ]+)[ ]+={6}')
  regex_result = re.match(regex_str, title_line)
  if (regex_result != None):
    return regex_result.group(1)
  else:
    return "无标题"

def format_zim_file_content(zim_file_content):
    repl_patterns = [ \
      { "repl_str": "\n", "sub_str": "[#endl#]&#10;" }, \
      { "repl_str": "&", "sub_str": "&amp;" }, \
      { "repl_str": "\"", "sub_str": "&quot;" }, \
      { "repl_str": "\'", "sub_str": "&#x27;" }, \
      { "repl_str": ">", "sub_str": "&gt;" }, \
      { "repl_str": "<", "sub_str": "&lt;" } \
    ]
    result_str = "".join(zim_file_content)
    for pair in repl_patterns:
      if (result_str.find(pair.get('repl_str'))):
        result_str = result_str.replace(pair.get('repl_str'), pair.get('sub_str'))
    return result_str

def convert_zim_file_to_outline(zim_file_path):
  leaf_outline_wrapper = '<outline text="%s" _note="%s" />\n'
  nonleaf_outline_wrapper = '<outline text="%s" _note="%s">\n%s\n</outline>\n'
  if (zim_file_path[-4:] != ".txt"):
    err_msg = "给定文件不是 Zim Wiki 格式！"
    print(err_msg)
    outline = leaf_outline_wrapper % ("[提醒] 导入有误", err_msg)
  else:
    file_lines = load_zim_file(zim_file_path)
    title = get_zim_file_title(file_lines[4])
    content = format_zim_file_content(file_lines)
    sub_outline_list = []
    zim_file_name = zim_file_path[0:-4]
    if (os.path.isdir(zim_file_name)):
      sub_zim_files = glob.glob(os.path.join(zim_file_name, "*.txt"))
      # traverse dir recursively
      for zim_file in sub_zim_files:
        sub_outline_list.append(convert_zim_file_to_outline(zim_file))
      sub_outlines = "\n".join(sub_outline_list)
      outline = nonleaf_outline_wrapper % (title, content, sub_outlines)
    else:
      outline = leaf_outline_wrapper % (title, content)
  return outline

def wrap_outline_into_opml(outline):
  opml_template = """<?xml version="1.0" encoding="utf-8"?>
<opml version="2.0">
  <body>
    %s
  </body>
</opml>
"""
  opml_output = opml_template % outline
  return opml_output

if __name__ == '__main__':
  fh = open("./pub.opml","w", encoding="utf8")
  outline = convert_zim_file_to_outline("r:/_zim/pim-wudi/pub.txt")
  fh.write(wrap_outline_into_opml(outline))
  fh.close()
