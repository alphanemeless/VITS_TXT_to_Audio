# VITS_TXT_to_Audio
-  Modified from [MoeGoe](https://github.com/CjangCjengh/MoeGoe), thanks to CjangCjengh's great work
- Update: Added subtitle generation,use pydub to rewrite some functions implemented by ffmpeg in the old version

# What is this
 This is a convenient tool for generating audio files

 You can put all the content in a txt file, and the program will automatically generate audio files
 
 When all the files have been generated, the program will use pydub to concat them and create srt subtitle
 
 You can use it on Google Colab:
 - [Colab, original by me](https://colab.research.google.com/drive/11rJasgCQah-VhhPrC4J8mM5UoWQp6oID?usp=sharing)

# How to use
- Run txt_to_audio.py
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
## Concat audio files and create subtitle
To simplify the code, I rewrites the concat function implemented by ffmpeg

The old version code can be found in [ffmpeg_concat](https://github.com/alphanemeless/VITS_TXT_to_Audio/tree/ffmpeg_concat) branch

After concat successful, srt subtitle will be automatically generated

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

#subtitle.srt    the subtitle of concat_all.wav
#concat_all.wav  concat all audio files
```
