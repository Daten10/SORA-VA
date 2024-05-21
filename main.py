# TODO
# запросы в гугле
# интерфейс

import random
import torch
import sounddevice as sd
import time
from stt import va_listen
import datetime
import webbrowser
from num2words import num2words
from pvrecorder import PvRecorder
import pvporcupine
from sounds import play_audio

# audio_folder = "D:/pyProjects/Makima/audio"
greetings = ['audio/r1.wav', 'audio/r2.wav', 'audio/r3.wav']
do = ['audio/commands/budetsdelano.wav', 'audio/commands/secundochku.wav', 'audio/commands/secundu.wav',
      'audio/commands/vipolnyau.wav']
again = ['audio/commands/esheraz.wav', 'audio/commands/neponyala.wav', 'audio/commands/takoinet.wav',]

language = 'ru'
model_id = 'v4_ru'
sample_rate = 48000
speaker = 'baya'
put_accent = True
put_yoo = True
device = torch.device('cpu')
text = 'Приветствую Данил! Сегодня я буду вашим голосовым помощником'

model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                     model='silero_tts',
                                     language=language,
                                     speaker=model_id)
model.to(device)  # gpu or cpu



# Настройки Porcupine
porcupine = pvporcupine.create(
    access_key='o3KmvBWPoF5Yv8XuqnzneJ3q8j2Xb2SCpvYTaclVJ6Rox1tT2+pC2A==',
    keyword_paths=['wake_word.ppn'],  # Замените на путь к вашему файлу ключевого слова
    model_path='porcupine_params_ru.pv'  # Замените на путь к русской модели Porcupine
)

recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)


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

        # response = "Открываю браузер"
        # va_speak(response)

    elif 'экзамен' in command:
        play_audio('D:/pyProjects/Makima/audio/commands/pizdec.wav')
        # webbrowser.open("http://www.google.com")
        # response = "Открываю браузер"
        # va_speak(response)

    elif 'музыку' in command:
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

    else:
        play_audio(random.choice(again))
        # response = "Извините, я не понимаю эту команду"
        # va_speak(response)


def main():
    try:
        recorder.start()
        print('Listening for wake word...')

        while True:
            pcm = recorder.read()
            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print('Wake word detected!')

                play_audio(random.choice(greetings))
                # va_speak("Как я могу помочь?")
                command = va_listen(timeout=10)  # Ожидание команды в течение 10 секунд
                if command:
                    process_command(command)

    except KeyboardInterrupt:
        print('Stopping...')
    finally:
        recorder.stop()
        porcupine.delete()


if __name__ == "__main__":
    main()
