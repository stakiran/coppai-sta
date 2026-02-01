import pyperclip

file_path = r"D:\\Dropbox\\franklog.md"
with open(file_path, 'r', encoding='utf-8') as file:
    s = file.read()
pyperclip.copy(s)
