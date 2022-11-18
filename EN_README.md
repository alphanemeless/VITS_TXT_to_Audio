# VITS_TXT_to_Audio
- [MoeGoe](https://github.com/CjangCjengh/MoeGoe)

  Modified from MoeGoe, thanks to CjangCjengh's great work

# What is this
 This is a convenient tool for generating audio files

 You can put all the content in a txt file, and the program will automatically generate audio files
 
 When all the files have been generated, the program will use ffmpeg to concat them
 
 You can use it on Google Colab:
 - [Colab, original by me](https://colab.research.google.com/drive/1ha1t0vVO0Bg-2vQXyv0wm5VaMt_yDGtZ?usp=sharing)

# How to use
- Windows:Run txt_to_audio_win.py

- Linux:Run txt_to_audio_linux.py
```
Path of a VITS model: D:\Download\243_epochs.pth
Path of a Json config file: D:\Download\config.json
Path of a txt file:D:\Download\text_file.txt
Path of a Output: D:\output
Do you want to set start number of wav file?y or n:(if you don't want to set,input n)
```
If torch.cuda.is_available() is False

Please try to reinstall torch

Find a torch version suitable for your CUDA
in [pytorch](https://pytorch.org/get-started/locally/)
## Concat audio files
To concat audio files,you need to install ffmpeg first

Install:

- Windows: download [ffmpeg](https://ffmpeg.org/) (Automatically download when first use)

- Linux: sudo apt install ffmpeg

```
#Need to install ffmpeg first
Do you want to concat all the wavfiles?(y or n):y
create mylist.txt success
copy silence audio success
```

## TXT File Sample
You need to separate the speaker number from the text content with |

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

## Output Sample
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
