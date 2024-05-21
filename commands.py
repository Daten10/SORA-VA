import os
import time
import torch
import random
import datetime
import webbrowser
import sounddevice as sd

from num2words import num2words

import config
from sounds import again, do, play_audio

full_path = "C:/Users/User/Desktop/sora_test/"
base = 'D:/pyProjects/Makima'

language = 'ru'
model_id = 'v4_ru'
sample_rate = 48000
speaker = 'baya'
put_accent = True
put_yoo = True
device = torch.device('cpu')
text = 'Приветствую Данил!'

model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                     model='silero_tts',
                                     language=language,
                                     speaker=model_id)
model.to(device)  # gpu or cpu


def create_directory(directory_name):
    os.chdir(full_path)
    os.mkdir(directory_name)
    return f"Directory {directory_name} created"


def remove_directory(directory_name):
    os.chdir(full_path)
    os.rmdir(directory_name)
    return f"Directory {directory_name} removed"


def rename_file(old_name, new_name):
    os.chdir(full_path)
    os.rename(old_name, new_name)
    return f"Renamed {old_name} to {new_name}"


def delete_file(file_name):
    os.remove(file_name)
    return f"File {file_name} deleted"


def va_speak(what: str):
    audio = model.apply_tts(text=what,
                            speaker=speaker,
                            sample_rate=sample_rate)

    sd.play(audio, sample_rate)
    time.sleep(len(audio) / sample_rate + 1)
    sd.stop()


def process_command(command: str):
    command = command.lower()

    if 'время' in command:
        now = datetime.datetime.now()
        hours_text = num2words(now.hour, lang='ru')
        minutes_text = num2words(now.minute, lang='ru')
        play_audio('D:/pyProjects/Makima/audio/commands/seichas.wav')
        response = f" {hours_text} часов {minutes_text} минут"
        va_speak(response)

    elif 'открой' in command and 'браузер' in command:
        play_audio(random.choice(do))
        webbrowser.open("http://www.google.com")

    elif 'экзамен' in command:
        play_audio('D:/pyProjects/Makima/audio/commands/pizdec.wav')

    elif config.VA_CMD in command:
        play_audio(random.choice(do))
        webbrowser.open("https://open.spotify.com")

    elif 'ютуб' in command:
        play_audio(random.choice(do))
        webbrowser.open("https://www.youtube.com")

    elif 'руслан' in command:
        webbrowser.open("https://pbs.twimg.com/media/FAUTjJ6UcAQma_j?format=jpg&name=small")
        play_audio('audio/ruslan.wav')

    elif 'ты' in command and 'молодец' in command:

        play_audio('audio/molodec.wav')

    elif 'гугл' in command and 'поиск' in command:

        play_audio(random.choice(do))
        stroka = command
        st_list = stroka.split()
        search_str = " ".join(st_list[2::1])
        webbrowser.open("https://www.google.com/search?q=" + f"{search_str}")

    elif 'создать папку' in command:
        play_audio(random.choice(do))
        stroka = command
        st_list = stroka.split()
        name_str = " ".join(st_list[2::1])
        create_directory(name_str)
        os.chdir(base)

    elif 'удалить папку' in command:
        play_audio(random.choice(do))
        stroka = command
        st_list = stroka.split()
        name_str = " ".join(st_list[2::1])
        print(full_path + name_str)
        if os.path.exists(full_path + name_str):
            remove_directory(name_str)
            os.chdir(base)
        else:
            print('нету')

    elif 'переименовать папку' in command:
        play_audio(random.choice(do))
        stroka = command
        st_list = stroka.split()
        name_str = " ".join(st_list[2:3:1])
        new_name = ''.join(st_list[-1])
        print(full_path + name_str)
        if os.path.exists(full_path + name_str):
            rename_file(name_str, new_name)
            os.chdir(base)
        else:
            print('нету')

    else:
        play_audio(random.choice(again))
        # response = "Извините, я не понимаю эту команду"
        # va_speak(response)
