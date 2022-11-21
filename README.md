# VITS_TXT_to_Audio
- [MoeGoe](https://github.com/CjangCjengh/MoeGoe)
- [English_README](https://github.com/alphanemeless/VITS_TXT_to_Audio/blob/main/EN_README.md)
- 增加字幕生成功能，优化代码，用pydub重写了旧版本中由ffmpeg实现的部分功能

# 简介
 
 这是一个VITS音频生成工具，加入了字幕生成功能。可以在生成音频的同时，自动生成srt字幕
 
 你可以将大量的文本放进一个txt文件中，然后程序会自动对文本生成音频
 
 txt文件中的每一行都会生成一个音频文件
 
 当所有音频生成完毕后，会使用 pydub 将音频文件连接起来，输出一个长音频文件，同时还会创建与之匹配的srt字幕
 
 你可以在 [Colab](https://colab.research.google.com/drive/11rJasgCQah-VhhPrC4J8mM5UoWQp6oID?usp=sharing) 的Demo上尝试一下：

# 如何使用
- 运行 txt_to_audio.py
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

## 连接音频和生成字幕
- 为了简化代码，本工具将旧版本中由 ffmpeg 实现的音频连接功能改写为了由 pydub实现，旧版代码可以在 [ffmpeg_concat](https://github.com/alphanemeless/VITS_TXT_to_Audio/tree/ffmpeg_concat) 分支中找到

- 在连接音频成功后，会自动生成 srt 字幕

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
subtitle.srt
concat_all.wav


#subtitle.srt    the subtitle of concat_all.wav
#concat_all.wav  concat all audio files
```
