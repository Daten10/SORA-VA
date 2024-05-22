import time

import soundfile as sf
import sounddevice as sd

from selenium import webdriver
import json
greetings = ['audio/r1.wav', 'audio/r2.wav', 'audio/r3.wav']
do = ['audio/commands/budetsdelano.wav', 'audio/commands/secundochku.wav', 'audio/commands/secundu.wav',
      'audio/commands/vipolnyau.wav']
again = ['audio/commands/esheraz.wav', 'audio/commands/neponyala.wav', 'audio/commands/takoinet.wav',]

privet = ['audio/privet.wav', 'audio/greeting.wav', 'audio/zdr.wav']

def play_audio(file_path: str):
    audio_data, sample_rate = sf.read(file_path, dtype='int16')
    sd.play(audio_data, sample_rate)
    sd.wait()  # Ждем завершения воспроизведения

# def save_cookies(driver, filename):
#     # Получение всех cookie с текущей страницы
#     cookies = driver.get_cookies()
#
#     # Сохранение cookie в файл в формате JSON
#     with open(filename, 'w') as file:
#         json.dump(cookies, file)

# # Пример использования:
# driver = webdriver.Chrome()
# driver.get("https://open.spotify.com")
# time.sleep(20)
# save_cookies(driver, "spotify_cookies.txt")
#
# # Закрыть драйвер
# driver.quit()