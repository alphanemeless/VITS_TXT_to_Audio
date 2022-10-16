import sys, re

import torch.cuda
from torch import no_grad, LongTensor
import logging

logging.getLogger('numba').setLevel(logging.WARNING)

import commons
import utils
from models import SynthesizerTrn
from text import text_to_sequence, _clean_text
from mel_processing import spectrogram_torch

from scipy.io.wavfile import write

from my_tools import make_ffmpeg_outputfile

def get_text(text, hps, cleaned=False):
    if cleaned:
        text_norm = text_to_sequence(text, hps.symbols, [])
    else:
        text_norm = text_to_sequence(text, hps.symbols, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm


def ask_if_continue():
    while True:
        answer = input('Continue? (y/n): ')
        if answer == 'y':
            break
        elif answer == 'n':
            sys.exit(0)


def print_speakers(speakers):
    print('ID\tSpeaker')
    for id, name in enumerate(speakers):
        print(str(id) + '\t' + name)


def get_speaker_id(message):
    speaker_id = input(message)
    try:
        speaker_id = int(speaker_id)
    except:
        print(str(speaker_id) + ' is not a valid ID!')
        sys.exit(1)
    return speaker_id


def get_label_value(text, label, default, warning_name='value'):
    value = re.search(rf'\[{label}=(.+?)\]', text)
    if value:
        try:
            text = re.sub(rf'\[{label}=(.+?)\]', '', text, 1)
            value = float(value.group(1))
        except:
            print(f'Invalid {warning_name}!')
            sys.exit(1)
    else:
        value = default
    return value, text


def get_label(text, label):
    if f'[{label}]' in text:
        return True, text.replace(f'[{label}]', '')
    else:
        return False, text


class my_class:
    def __init__(self, *x):  # *x is a variable length parameter
        if len(x) == 2:
            self.seq = x[0]
            self.text = x[1]
            self.filenumber = 0  # only used to regenerate the failed audio
        elif len(x) == 0:
            self.seq = ""
            self.text = ""
            self.filenumber = 0
        elif len(x) == 3:
            self.seq = x[0]
            self.text = x[1]
            self.filenumber = x[2]
        else:
            raise AssertionError("Parameter error")


def my_get_txtflie(txtpath):
    # Read the txt file by line. You need to preprocess the text
    # remove blank lines, and use | to separate the speaker's serial number and speech content
    # return value is a class list. class has two attributes, serial number and text content
    class_list = []
    req = open(txtpath, encoding="utf-8").readlines()
    for line in req:
        line = str(line)
        if len(line) != 0:
            seq, line_text = line.split("|", 1)
            line_class = my_class()
            line_class.seq = seq
            line_class.text = line_text
            class_list.append(line_class)
        else:
            print("This line is blank")
    return class_list


def my_voice_maker(character_seq, text, output_path):
    length_scale, text = get_label_value(text, 'LENGTH', 1.1, 'length scale')
    noise_scale, text = get_label_value(text, 'NOISE', 0.667, 'noise scale')
    noise_scale_w, text = get_label_value(text, 'NOISEW', 0.8, 'deviation of noise')
    cleaned, text = get_label(text, 'CLEANED')

    stn_tst = get_text(text, hps_ms, cleaned=cleaned)

    character_seq = int(character_seq)
    speaker_id = character_seq
    out_path = output_path

    print("Raw_Text:", text)
    print("Cleaned_Text:", _clean_text(text, hps_ms.data.text_cleaners))

    with no_grad():
        x_tst = stn_tst.unsqueeze(0).to(dev)
        x_tst_lengths = LongTensor([stn_tst.size(0)]).to(dev)
        sid = LongTensor([speaker_id]).to(dev)
        audio = net_g_ms.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=noise_scale, noise_scale_w=noise_scale_w,
                               length_scale=length_scale)[0][0, 0].data.cpu().float().numpy()
    write(out_path, hps_ms.data.sampling_rate, audio)


if __name__ == '__main__':
    model = input('Path of a VITS model: ') #input your path of vits model
    config = input('Path of a Json config file: ') #input your path of config
    print("Loading model......")

    dev = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    hps_ms = utils.get_hparams_from_file(config)
    n_speakers = hps_ms.data.n_speakers if 'n_speakers' in hps_ms.data.keys() else 0
    n_symbols = len(hps_ms.symbols) if 'symbols' in hps_ms.keys() else 0
    speakers = hps_ms.speakers if 'speakers' in hps_ms.keys() else ['0']

    net_g_ms = SynthesizerTrn(
        n_symbols,
        hps_ms.data.filter_length // 2 + 1,
        hps_ms.train.segment_size // hps_ms.data.hop_length,
        n_speakers=n_speakers,
        **hps_ms.model).to(dev)
    _ = net_g_ms.eval()
    utils.load_checkpoint(model, net_g_ms)

    while True:
        txt_path = input('Path of a txt file: ')
        output_path = input('Path of a Output: ')

        class_from_txt_list = my_get_txtflie(txt_path)
        class_get_loss_list = []

        file_number = 1

        flag = input("Do you want to set start number of wav file?y or n:")
        if flag == "y":
            set_number = input('wav file start number: ')
            try:
                set_number = int(set_number)
                file_number = set_number
            except:
                print("input number:", set_number, "is Invild")
        else:
            pass

        for class_fromtxt in class_from_txt_list:
            str_file_number = str(file_number).zfill(4)
            try:
                output_path_name = output_path + "/" + str_file_number + ".wav"
                my_voice_maker(class_fromtxt.seq, class_fromtxt.text, output_path_name)
            except Exception as the_erro:
                print("file：", output_path_name, "content：", class_fromtxt.text, "generate failed")
                class_file_loss = my_class(class_fromtxt.seq, class_fromtxt.text, file_number)
                class_get_loss_list.append(class_file_loss)
                print(the_erro)
            file_number = file_number + 1

        if class_get_loss_list:
            for class_loss in class_get_loss_list:
                str_file_number_loss = str(class_loss.filenumber).zfill(4)  # the insufficient digits are filled with zeros
                try:
                    output_path_name2 = output_path + "/" + str_file_number_loss + ".wav"
                    my_voice_maker(class_loss.seq, class_loss.text, output_path_name2)
                except:
                    print("file：", output_path_name2, "content：", class_loss.text, "generate failed")
                    class_file_loss2 = my_class(class_loss.seq, class_loss.text, class_loss.filenumber)
                    class_get_loss_list.append(class_file_loss2)

        print("Voice Generated Sucessful")
        flag2 = input("Do you want to concat all the wavfiles?(need ffmpeg)y or n:")
        if flag2 == "y":
            ffmpeg_path = input('input bin path in ffmpeg folder(eg:D:/ffmpeg/bin) :')
            # silent_audiofile_path = input('input the path of silence audio file(you can find it in directory silence): ')
            silent_audiofile_path = "silent/silent-audio07_re_32bit.wav"
            make_ffmpeg_outputfile.use_ffmpeg_make_output_file(wav_raw_path=output_path,
                                                               silent_audiofile_path=silent_audiofile_path,
                                                               ffmpeg_path=ffmpeg_path)
            # print("The console output of ffmpeg is red,no need to worry")
            print("concat successed")
        else:
            pass
        ask_if_continue()