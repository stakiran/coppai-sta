import os
import glob
import tkinter as tk
import pathspec
import sys
import pyperclip
import re
import subprocess
import platform

# 定数
COPPAI_DIR = os.path.dirname(os.path.abspath(__file__))
COPPAIIGNORE_FILE = os.path.join(COPPAI_DIR, '.coppaiignore')

def load_ignore_patterns():
    if os.path.exists(COPPAIIGNORE_FILE):
        with open(COPPAIIGNORE_FILE, 'r', encoding='utf-8') as f:
            spec = pathspec.PathSpec.from_lines('gitwildmatch', f)
            return spec
    return None

def is_ignored(path, spec):
    if spec is None:
        return False
    rel_path = os.path.relpath(path, COPPAI_DIR)
    return spec.match_file(rel_path)

def find_snippet_files():
    spec = load_ignore_patterns()
    snippet_files = []
    # 直下のmdファイル
    for file in glob.glob(os.path.join(COPPAI_DIR, '*.md')):
        if not is_ignored(file, spec):
            snippet_files.append(file)
    # 直下のフォルダ内のmdファイル
    for folder in [f for f in os.listdir(COPPAI_DIR) if os.path.isdir(os.path.join(COPPAI_DIR, f))]:
        folder_path = os.path.join(COPPAI_DIR, folder)
        for file in glob.glob(os.path.join(folder_path, '*.md')):
            if not is_ignored(file, spec):
                snippet_files.append(file)
    return snippet_files

def load_snippet(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def run_getter_script(script_name):
    script_path = os.path.join(COPPAI_DIR, f"{script_name}.py")
    if not os.path.isfile(script_path):
        return ""
    try:
        # 実行して結果をクリップボードにコピーするスクリプトなので、実行だけ行う
        subprocess.run([sys.executable, script_path], check=True)
        # 実行後のクリップボード内容を取得
        return pyperclip.paste()
    except Exception as e:
        return ""

def expand_variables(text):
    def replace_getter(match):
        var_name = match.group(1)
        result = run_getter_script(var_name)
        return result

    # まずは cb 変数から処理する
    # これにより cb 変数と getter 変数が混在できる
    cb_content = pyperclip.paste()
    text = text.replace('%cb%', cb_content)

    text = re.sub(r'%getter_([a-zA-Z0-9_]+)%', replace_getter, text)

    return text

def show_popup_menu(snippets):
    root = tk.Tk()
    root.title("coppai - スニペット選択")
    # ウィンドウを最小化せず、適切なサイズで表示
    root.geometry('400x300+100+100')
    root.deiconify()

    def on_select():
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            snippet_text = snippets[index][1]
            expanded_text = expand_variables(snippet_text)
            pyperclip.copy(expanded_text)
        root.destroy()

    def on_key_press(event):
        if event.keysym == 'Return' or event.keysym == 'space':
            on_select()
        elif event.keysym == 'Escape':
            root.destroy()
        elif event.keysym == 'f':
            path = COPPAI_DIR
            # Macでは試してないので動くかわからん
            if platform.system() == 'Windows':
                subprocess.Popen(['explorer', path])
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', path])
            else:
                subprocess.Popen(['xdg-open', path])
            return "break"
        elif event.keysym == 'Up':
            current = listbox.curselection()
            if current:
                index = current[0]
                if index > 0:
                    listbox.selection_clear(0, tk.END)
                    listbox.selection_set(index - 1)
                    listbox.activate(index - 1)
                    listbox.see(index - 1)
                else:
                    # 先頭でupしたら末尾にジャンプ
                    last_index = listbox.size() - 1
                    listbox.selection_clear(0, tk.END)
                    listbox.selection_set(last_index)
                    listbox.activate(last_index)
                    listbox.see(last_index)
            else:
                listbox.selection_set(0)
                listbox.activate(0)
                listbox.see(0)
            # もし `return "break"` がないと、例えば `<Up>` キーを押したときに、`on_key_press` が処理した後、デフォルトのリストボックスのキー処理が続けて行われてしまう可能性があります。その結果、リストボックスの選択が 2 回移動される（例えば 1 回のキー押しで 2 つの項目が飛ばされる）ように見えることがあります。
            return "break"
        elif event.keysym == 'Down':
            current = listbox.curselection()
            if current:
                index = current[0]
                if index < listbox.size() - 1:
                    listbox.selection_clear(0, tk.END)
                    listbox.selection_set(index + 1)
                    listbox.activate(index + 1)
                    listbox.see(index + 1)
                else:
                    listbox.selection_clear(0, tk.END)
                    listbox.selection_set(0)
                    listbox.activate(0)
                    listbox.see(0)
            else:
                listbox.selection_set(0)
                listbox.activate(0)
                listbox.see(0)
            return "break"

    listbox = tk.Listbox(root, width=80, height=20)
    for i, (name, _) in enumerate(snippets):
        listbox.insert(tk.END, f"{i+1} - {name}")
    listbox.pack(fill=tk.BOTH, expand=True)
    listbox.bind('<Key>', on_key_press)
    listbox.focus_set()

    # キャンセル時はウィンドウを閉じる
    def on_cancel(event):
        root.destroy()
    root.bind('<Escape>', on_cancel)

    root.mainloop()

def main():
    snippet_files = find_snippet_files()
    print(f"スニペットファイル数: {len(snippet_files)}")  # 追加: スニペット数を表示
    snippets = []
    for file_path in snippet_files:
        name = os.path.splitext(os.path.basename(file_path))[0]
        content = load_snippet(file_path)
        snippets.append((name, content))

    if not snippets:
        print("スニペットが見つかりませんでした。")
        sys.exit(0)

    show_popup_menu(snippets)

if __name__ == '__main__':
    main()
