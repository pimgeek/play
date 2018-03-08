import re

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
    repl_str = "\n"
    sub_str = "&#10;"
    return zim_file_content.replace(repl_str, sub_str)

def export_zim_file_to_opml(zim_file_path):
  file_lines = load_zim_file(zim_file_path)
  title = get_zim_file_title(file_lines[4])
  content = "".join(file_lines)
  opml = """
<?xml version="1.0" encoding="utf-8"?>
<opml version="2.0">
  <body>
    <outline text="%s" _note="%s" />
  </body>
</opml>
    """ % (title, format_zim_file_content(content))
  return opml
