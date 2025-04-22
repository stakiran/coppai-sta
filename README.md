# coppai-sta
[coppai](https://github.com/stakiran/coppai) の、自分用設定

## install

### 1: coppai.py はコピペや DL などで持ってくる

### 2: 各種スニペットはこのリポジトリで管理

### 3: coppai の呼び出し
ひとまず ahk で。以下は ctrl + alt + c の例。

```ahk
!^c::
	run, "D:\work\github\stakiran_sub\coppai-sta\coppai.bat"
return
```

ラッパーとしてバッチファイルをつくっている。カレントディレクトリが合わないと動かないので `pushd %~dp0` つき。
