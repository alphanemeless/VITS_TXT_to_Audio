import os

def make_ffmpeg_filelists(wavpath):
    FileName_Output = wavpath + "/" + "mylist.txt"
    dir_filelist = os.listdir(wavpath)
    for filename in dir_filelist:
        with open(FileName_Output, 'a', encoding='utf-8')as file:
            file.write("file '" + filename + "'" + "\n")
            file.write("file 'silent-audio07_re_32bit.wav'" + "\n")
    print("create mylist.txt successed")

def muti_folder_make_filelists(raw_path):
    sub_path = os.listdir(raw_path)
    for path_name in sub_path:
        true_path = raw_path + "/" + path_name
        print(true_path)
        make_ffmpeg_filelists(true_path)