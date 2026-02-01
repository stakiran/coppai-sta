import pyperclip

def get_latest_week_entries(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        # ファイルの内容を行ごとにリストとして保存
        lines = file.readlines()
    
    latest_week_entries = []
    current_week_entries = []
    
    for line in lines:
        if line.startswith('# '):
            # 見出しが見つかったらそれまでのcurrent_week_entriesをlatest_week_entriesに設定
            latest_week_entries = current_week_entries
            current_week_entries = []  # 現在の週を新たに構築
        current_week_entries.append(line.strip())
    
    # ループから出た後、最終エントリをチェック
    latest_week_entries = current_week_entries if current_week_entries else latest_week_entries
    
    return latest_week_entries

file_path = 'D:\\Dropbox\\franklog.md'
latest_week_entries = get_latest_week_entries(file_path)

# 最新週のエントリを出力
s = '\n'.join(latest_week_entries)
pyperclip.copy(s)
