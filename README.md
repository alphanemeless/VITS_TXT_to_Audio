# Forked from
- [MoeGoe](https://github.com/CjangCjengh/MoeGoe)

# 简介
 
 这是一个VITS音频生成工具，基于MoeGoe制作
 
 你可以将大量的文本放进一个txt文件中，然后程序会自动对文本生成音频
 
 txt文本中的每一行都会生成一个音频文件
 
 当所有音频生成完毕后，会使用[ffmpeg](https://ffmpeg.org/)将音频文件连接起来，输出一个长音频文件
 
 你可以在[Colab](https://colab.research.google.com/drive/1ha1t0vVO0Bg-2vQXyv0wm5VaMt_yDGtZ?usp=sharing)的Demo上尝试一下：

# 如何使用
- Windows: 运行 txt_to_audio_win.py

- Linux: 运行 txt_to_audio_linux.py
```
Path of a VITS model: D:\Download\243_epochs.pth
Path of a Json config file: D:\Download\config.json
Path of a txt file:D:\Download\text_file.txt
Path of a Output: D:\output
Do you want to set start number of wav file?y or n:(if you don't want to set,input n)
```
如果出现torch.cuda.is_available() is False

请尝试重新安装torch

你可以在[pytorch](https://pytorch.org/get-started/locally/)找到适用于你的CUDA版本torch

## 连接音频
- 本工具使用ffmpeg来连接音频，第一次使用该功能，会自动从ffmpeg下载相应的组件

- 如果您使用linux系统，可以使用 sudo apt install ffmpeg 命令来安装

```
#default output
Do you want to concat all the wavfiles?(y or n):y
create mylist.txt success
copy silence audio success
```

在silent文件夹中，提供了一个时长0.7秒的静音文件，用于在不同句子之间，增加语音间隔

## TXT文件样例
你需要将说话人的编号和文本内容隔开

分割符号为 | 

Sample.txt:
```
1|こんにちは
5|今日もあなたに会えてとっても嬉しいです
0|可愛いですよ
5|こちらの部屋に来て下さい。
7|楽しみですよね
5|それじゃあ、始めますね
3|どうでしょうか？
5|来週楽しみにしていますね
2|よろしくお願いします
5|では、本日はここまで。
```
建议对文本进行预处理，尽量删除其中的空行和特殊符号

## 样例输出
```
0001.wav
0002.wav
0003.wav
0004.wav
0005.wav
0006.wav
0007.wav
0008.wav
0009.wav
0010.wav
mylist.txt
silent-audio07_re_32bit.wav
test_all.wav

#test_all.wav  concat all audio files
```
