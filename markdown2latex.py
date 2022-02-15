"""
File: markdown2latex.py 
-------------------
Active draft version of markdown2latex
How to use:
$ python3 markdown2latex.py input.md > output.tex
"""

import re
import sys


def master_regex(string, raw_value):
  if string == "" or (raw_value == True and r"```" not in string):
    return string
  if r"<center>" == string:
  	return r"\begin{center}"
  if r"</center>" == string:
  	return r"\end{center}"
  if r"<br>" in string:
  	return r"\\"
  if string[0] == r"!" and string[1] == r"[":
    return md_img(string) 
  if r"<img src" in string:
    return html_img(string)
  if r'<blockquote' in string:
    return r"\begin{mdframed}" 
  if r"<markdown>" in string or r"</markdown>" in string:
    return ""
  if r"</blockquote>" in string:
    return r"\end{mdframed}"
  if r"```" in string:
    return code_block(string)
  if string[0] == r"#" and string[1] != r"#":
    if r"<center>" in string:
      return header_one_center(string)
    else:
      return header_one(string)
  if string[0] == r"#" and string[1] == r"#" and string[2] != r"#": 
    return header_two(string)
  if string[0] == r"#" and string[1] == r"#" and string[2] == r"#" and string[3] != r"#": 
    return header_three(string)
  if string[0] == r"#" and string[1] == r"#" and string[2] == r"#" and string[3] == r"#":
    return header_four(string)
  if r"---" in string:
    return horizontal_rule(string)
  else:
    return string

def applied_all(string, raw_value):
  """
  For commands that are universal (i.e. could be in a title), we are best off simply defining a function for this and then calling your master_regex function as normal and then pass that output into this function. So in other words, this function should not be apart of master_regex.

  Note: might need to apply multiple times (i.e. loop through several times). 
  """
  if raw_value == True:
    return string
  if r"[" in string and r"]" in string and r"(" in string and r")" in string:
    return url_link(string)
  if r"-" in string:
    if string.lstrip()[0] == r"-":
      return bullet_points(string)
  if r"<u>" in string:
    return underline_text(string)
  if r"**" in string:
    return bold_text(string) 
  if string.count(r"*") > 0 and string.count(r"*") % 2 == 0:
    return emph_text(string) 
  if r"`" in string and r"```" not in string:
    return inline_code(string)
  else:
    return string

# ------------------------------------------

def header_one(string):
  x = re.sub("# ", r'\\section{', string)
  x += r"}"
  return x

def header_one_center(string):
  x = re.sub(r"# <center> ", r'\\section{', string)
  x = re.sub(" </center>", r'}', x)
  return x

def header_two(string):
  x = re.sub("## ", r'\\subsection{', string)
  x += r"}"
  return x

def header_three(string):
  x = re.sub("### ", r'\\subsubsection{', string)
  x += r"}"
  return x

def header_four(string):
  """
  Note: there is no \subsubsubsection in LaTeX, so this function will 
  just bold this string and then add a new line. 
  """
  x = re.sub("#### ", r'\\textbf{', string)
  x += r"}"
  x += r" \\"
  return x

def horizontal_rule(string):
  x = re.sub("---", r"\\noindent\\rule[0.5ex]{\\linewidth}{0.2pt}", string)
  return x

def inline_code(string):
  """
  Note: you must define a "\codeword" command in
  your LaTeX document. 
  """
  x = re.split(r'(\`)', string)
  counter = 1
  for i in range(len(x)):
    if x[i] == r"`":
      if counter % 2 != 0:
        x[i] = r"\codeword{"
      else:
        x[i] = r"}" 
      counter += 1
  return "".join(x)

def code_block(string):
  """
  Currently, we only support Python, C++, and plain text syntax highlighting,
  but it is very easy to change (just change the language)
  below. 
  """
  if string == r"```python":
    return r"\begin{minted}{python}"
  if string == r"```cpp":
    return r"\begin{minted}{cpp}"
  if string == r"```lang-text": 
    return r"\begin{minted}{text}"
  if string == r"```":
    return r"\end{minted}"
  else:
    # syntax error case
    return string
  
def html_img(string):
  # Extract image path 
  idx = string.index(r"@")
  built_up_str = ""
  for i in range(idx, len(string)):
    if string[i] == r'"':
      break
    built_up_str += string[i]
  built_up_str = built_up_str[1:]
  
  # Extract scale size 
  idx_2 = string.index(r"%")
  scale_str = ""
  for i in range(idx_2 - 4, idx_2):
    if string[i].isnumeric():
      scale_str += string[i]
  
  return r"\begin{figure}[H]" + "\n" + r"\centering" "\n" + r"\includegraphics[scale=" + str(float(scale_str)/100) + r"]{" + built_up_str + r"}" + "\n" + r"\end{figure}"
  # return r"\begin{figure}[t]" + "\n" + r"\includegraphics[scale=" + scale_str + r"%]{" + built_up_str + r"}" + "\n" + r"\end{figure}"

def md_img(string):
  # Extract image path 
  idx = string.index(r"@")
  built_up_str = ""
  for i in range(idx, len(string)):
    if string[i] == r')':
      break
    built_up_str += string[i]
  built_up_str = built_up_str[1:]

  return r"\begin{figure}[H]" "\n" + r"\centering" + "\n" + r"\includegraphics[scale=.7]{" + built_up_str + r"}" + "\n" +r"\end{figure}"

def url_link(string):
  # requires 'hyperref' package
  # Extract image path 
  idx = string.index(r"(")
  if string[idx - 1] != r']':
    return string 
  built_up_str = ""
  for i in range(idx + 1, len(string)):
    if string[i] == r')':
      break
    built_up_str += string[i] 

  # replace the parantheses 
  built_up_str = re.sub(r'%', r'\%', built_up_str)
  
  if idx > 1:
    if string[idx - 2] == r"[":
      return r"\url{" + built_up_str + r"}" 
  
  # Extract label 
  built_up_label_str = ""

  # get label index 
  label_idx = idx - 1 
  while label_idx > 0:
    if string[label_idx] == r"[":
      break
    label_idx -= 1

  # insert label 
  for i in range(label_idx + 1, len(string)):
    if string[i] == r']':
      break
    built_up_label_str += string[i] 
  
  # replace the parantheses 
  built_up_label_str = re.sub(r'%', r'\%', built_up_label_str)
  
  return r"\href{" + built_up_str + r"}{" + built_up_label_str + r"}" 

def bold_text(string): 
  x = re.split(r'\*', string)
  counter = 1
  for i in range(len(x)):
    if x[i] == r"":
      if counter % 2 != 0:
        x[i] = r"\textbf{"
      else:
        x[i] = r"}" 
      counter += 1
  return "".join(x)

def emph_text(string):
  x = re.split(r'\\*', string)
  counter = 1
  for i in range(len(x)):
    if x[i] == r"*":
      if counter % 2 != 0:
        x[i] = r"\emph{"
      else:
        x[i] = r"}" 
      counter += 1
  return "".join(x)

def bullet_points(string):
  x = string
  if string.index('-') == 0:
  	x = x.replace('-', r"\1")
  elif string.index('-') == 2:
  	x = x.replace('-', r"\2")
  elif string.index('-') == 4:
  	x = x.replace('-', r"\3")
  elif string.index('-') == 6:
  	x = x.replace('-', r"\4")
  elif string.index('-') == 8:
  	x = x.replace('-', r"\5")
  return x

def underline_text(string): 
  x = string 
  new_x = ""
  u_val = False
  for i in range(len(x)):
      if x[i] == r"<" and x[i+1] == r"u":
          u_val = True
          new_x += r"\underline{"
          continue
      if x[i] == r"<" and x[i+1] == r"/":
          u_val = True
          new_x += r"}" 
          continue
      if i != 0 and x[i-1] == r">":
          u_val = False
      if u_val == True:
          continue 
      new_x += x[i]
  return new_x





# -----------------------------------------------------------

md_file = open(sys.argv[1])
bp_file = open(sys.argv[1])

line_list = []
for temp_line in bp_file:
  temp_line = temp_line.rstrip()
  line_list.append(temp_line)

converted_string = ""

code_block_count = 0 
math_equation_count = 0
current_line_idx = 0
for line in md_file:
    raw_val = False
    line = line.rstrip()
    input_string = line
    if r"$$" in input_string:
      math_equation_count += 1
    if r"```" in input_string:
      code_block_count += 1      
    if code_block_count % 2 != 0:
      raw_val = True
    if math_equation_count % 2 != 0:
      raw_val = True
    output_line = master_regex(input_string, raw_val)
    for i in range(3):
      output_line = applied_all(output_line, raw_val)
    if current_line_idx != 0 and current_line_idx < (len(line_list) - 1):  
      if r"-" in input_string:
        if input_string.lstrip()[0] == r"-":
          if r"-" not in line_list[current_line_idx - 1]:
            output_line = r"\begin{outline}" +"\n" + output_line
          elif r"-" not in line_list[current_line_idx + 1]:
            output_line = output_line + "\n" + r"\end{outline}"
    converted_string += output_line
    converted_string += "\n"
    current_line_idx += 1

print(converted_string)
