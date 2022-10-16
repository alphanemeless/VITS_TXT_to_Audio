import os
import shutil

def make_ffmpeg_filelists(wavpath):
    FileName_Output = wavpath + "/" + "mylist.txt"
    dir_filelist = os.listdir(wavpath)
    dir_filelist.sort()
    for filename in dir_filelist:
        filename = str(filename)
        if filename.endswith(".wav"):
            with open(FileName_Output, 'a', encoding='utf-8')as file:
                file.write("file '" + filename + "'" + "\n")
                file.write("file 'silent-audio07_re_32bit.wav'" + "\n")
    print("create mylist.txt success")

def muti_folder_make_filelists(raw_path):
    sub_path = os.listdir(raw_path)
    for path_name in sub_path:
        true_path = raw_path + "/" + path_name
        print(true_path)
        make_ffmpeg_filelists(true_path)

def use_ffmpeg_make_output_file(wav_raw_path, silent_audiofile_path , ffmpeg_path,):
    make_ffmpeg_filelists(wav_raw_path)
    shutil.copy(silent_audiofile_path, wav_raw_path)
    print("copy silence audio success")

    try:
        rsplit_string = wav_raw_path.rsplit("/", 1)[1]
        cmd = ffmpeg_path + "/" + "ffmpeg -f concat -i " + wav_raw_path + "/" + "mylist.txt -c copy " + wav_raw_path + "/" + rsplit_string + "_all.wav"
        print(cmd)
        os.system(cmd)
    except:
        rsplit_string = wav_raw_path.rsplit("\\", 1)[1]
        cmd = ffmpeg_path + "\\" + "ffmpeg -f concat -i " + wav_raw_path + "\\" + "mylist.txt -c copy " + wav_raw_path + "\\" + rsplit_string + "_all.wav"
        print(cmd)
        os.system(cmd)


def use_ffmpeg_make_output_file_linux(wav_raw_path, silent_audiofile_path):
    make_ffmpeg_filelists(wav_raw_path)
    shutil.copy(silent_audiofile_path, wav_raw_path)
    print("copy silence audio success")

    rsplit_string = wav_raw_path.rsplit("/", 1)[1]
    cmd ="ffmpeg -f concat -i " + wav_raw_path + "/" + "mylist.txt -c copy " + wav_raw_path + "/" + rsplit_string + "_all.wav"
    print(cmd)
    os.system(cmd)