import re

pat = r'\d{4}$'
name = 'image_preview_0049'

print(re.split(pat, name))