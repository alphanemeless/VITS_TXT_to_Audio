from pydub import AudioSegment
import os

def create_sub(wav_path,txt_path,silent_audiofile_path):
    dir_filelist = os.listdir(wav_path)
    dir_filelist.sort()
    total_duration = 0
    output_sound = []
    count = 0
    txt_str = []

    words_ = open(txt_path, encoding="utf-8").read().replace("[ZH]","").replace("[JA]","").replace("[EN]","").replace("[KO]","").splitlines()
    words = []
    for i in range(len(words_)):
        if words_[i].find("|") != -1:
            words.append(words_[i].split('|'))
    print(words)

    def num2timestr(num):
        return str(int(int(num) / 3600)) + ':' + str(int(int(num) / 60)) + ':' + str(int(int(num) % 60)) + ',' + str(int(int(num * 10000000) % 10000000)).zfill(7)

    silent_sound = AudioSegment.from_wav(silent_audiofile_path)
    silent_duration = silent_sound.duration_seconds
    for filename in dir_filelist:
        filename = str(filename)
        if filename.endswith(".wav"):

            sound = AudioSegment.from_wav(wav_path + '/' + filename)
            duration = sound.duration_seconds  # 音频时长（ms）
            print(total_duration)
            print(duration)
            if output_sound == []:
                output_sound = sound + silent_sound
            else:
                output_sound = output_sound + sound + silent_sound

            txt_str.append(str(count))
            txt_str.append(num2timestr(total_duration) + ' --> ' + (num2timestr(total_duration + duration)))
            txt_str.append(str(words[count][1]) + "\n")
            total_duration = total_duration + duration + silent_duration
            count = count + 1

    with open(wav_path + "\\" + "subtitle.srt", "w", encoding="utf8") as f:
        f.write("\n".join(txt_str))
    output_sound.export(wav_path + "\\" + "concat_all.wav", format="wav")