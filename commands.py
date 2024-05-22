import g4f
import os
import re
import time
import torch
import random
import datetime
import pyperclip
import webbrowser
import sounddevice as sd
from pycaw.api.endpointvolume import IAudioEndpointVolume
import pyautogui as pg
from stt import va_listen

from num2words import num2words
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities
import config
from sounds import again, do, play_audio
import json

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


def spoty_login(driver):
    # Загрузка cookie из файла
    with open("spotify_cookies.txt", 'r') as file:
        cookies = json.load(file)

        # Добавление cookie к текущей сессии браузера
    for cookie in cookies:
        driver.add_cookie(cookie)
    # Обновление страницы, чтобы использовать загруженные файлы cookie
    driver.refresh()


def convert_numbers_to_words(text: str, lang: str = 'ru') -> str:
    def replace_number(match):
        number = match.group(0)
        return num2words(int(number), lang=lang)

    return re.sub(r'\d+', replace_number, text)


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
    try:
        what = convert_numbers_to_words(what)  # Преобразование чисел в слова
        audio = model.apply_tts(text=what,
                                speaker=speaker,
                                sample_rate=sample_rate)
        sd.play(audio, sample_rate)
        time.sleep(len(audio) / sample_rate + 1)
        sd.stop()
    except ValueError as e:
        print(f"Error in TTS synthesis: {e}")
        va_speak("Произошла ошибка при синтезе речи")


def get_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
    return volume_interface.GetMasterVolumeLevelScalar()


def set_volume(volume):
    if volume < 0:
        volume = 0
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
    volume_interface.SetMasterVolumeLevelScalar(volume, None)


def type_russian_text(ru_text):
    pyperclip.copy(ru_text)  # Копируем текст в буфер обмена


def ask_chatgpt(question: str) -> str:
    # client = Client()
    response = g4f.ChatCompletion.create(
        model="gpt-4",
        messages=[

            # {"role": "system", "content": "You are a voice assistant that helps the user with various tasks."
            #                               " In any task, if numbers are encountered, you must convert them into text "
            #                               "format. For example, 1 into one, 2 into two, 123 into one hundred "
            #                               "twenty-three and etc."},

            {"role": "user", "content": question}
        ],

    )
    return response


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

    elif 'ты молодец' in command:

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

    elif 'ещё больше' in command:
        play_audio(random.choice(do))
        current_volume = get_volume()
        new_volume = min(1.0, current_volume + 0.2)
        set_volume(new_volume)

    elif 'ещё меньше' in command:
        play_audio(random.choice(do))
        current_volume = get_volume()
        new_volume = max(0.0, current_volume - 0.2)
        set_volume(new_volume)

    elif 'громче' in command:
        play_audio(random.choice(do))
        current_volume = get_volume()
        new_volume = min(1.0, current_volume + 0.1)
        set_volume(new_volume)

    elif 'тише' in command:
        play_audio(random.choice(do))
        current_volume = get_volume()
        new_volume = max(0.0, current_volume - 0.1)
        set_volume(new_volume)

    elif 'включи звук' in command:
        play_audio(random.choice(do))
        current_volume = get_volume()
        new_volume = 0.7
        set_volume(new_volume)

    elif 'выключи звук' in command:
        play_audio(random.choice(do))
        current_volume = get_volume()
        new_volume = 0
        set_volume(new_volume)

    elif 'пауза' in command:
        webbrowser.open("https://open.spotify.com")
        play_audio(random.choice(do))
        time.sleep(4)
        pg.press('space')

    elif 'следующий трек' in command:
        webbrowser.open("https://open.spotify.com")
        play_audio(random.choice(do))
        pg.hotkey('ctrl', 'right')

    elif 'предыдущий трек' in command:
        play_audio(random.choice(do))
        pg.hotkey('ctrl', 'left')
        pg.hotkey('ctrl', 'left')

    elif 'включи трек' in command:
        play_audio(random.choice(do))
        webbrowser.open("https://open.spotify.com")
        time.sleep(6)
        stroka = command
        words_to_remove = ["включи", "трек"]
        for word in words_to_remove:
            stroka = stroka.replace(word, "")
        print(stroka)
        ru_text = stroka
        type_russian_text(ru_text)
        pg.hotkey('ctrl', 'shift', 'l')
        time.sleep(2)
        pg.hotkey('ctrl', 'v')
        time.sleep(3)
        pg.click(453, 478)
        time.sleep(1)
        pg.click(1414, 472)

    elif 'нейросеть' in command:
        response = "Вы хотите, чтобы я спросила ChatGPT?"
        play_audio('audio/chat.wav')

        user_input = va_listen(timeout=10)  # Ожидание ответа пользователя в течение 10 секунд
        if 'да' in user_input.lower():
            play_audio('audio/slushau.wav')
            user_inp = va_listen(timeout=10)
            command_str = user_inp
            play_audio(random.choice(do))
            chatgpt_response = ask_chatgpt(command_str)
            print(chatgpt_response)
            va_speak(chatgpt_response)
        elif 'нет' in user_input.lower():
            play_audio('audio/good.wav')
        else:
            play_audio(random.choice(again))
    else:
        play_audio(random.choice(again))

# def test():

# 1414 472
# 453 478
