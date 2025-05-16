import pyperclip

poem_raw = pyperclip.paste()
if not poem_raw:
    powm_raw = '<Error>\n<Error>'

lines = poem_raw.splitlines()
first_line = lines[0]
body_lines = lines[1:]
caption = first_line
content_by_list = body_lines
content_by_str = '\n'.join(content_by_list)

poem_normalized = f'''```
『{caption}』
{content_by_str}
```
'''

pyperclip.copy(poem_normalized)

