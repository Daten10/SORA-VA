# TODO
# запросы в гугле DONE
# интерфейс

import random
import pvporcupine

from stt import va_listen
from pvrecorder import PvRecorder
from commands import process_command
from sounds import play_audio, greetings




# Настройки Porcupine
porcupine = pvporcupine.create(
    access_key='o3KmvBWPoF5Yv8XuqnzneJ3q8j2Xb2SCpvYTaclVJ6Rox1tT2+pC2A==',
    keyword_paths=['wake_word.ppn'],  # Замените на путь к вашему файлу ключевого слова
    model_path='porcupine_params_ru.pv'  # Замените на путь к русской модели Porcupine
)

recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)




def main():
    play_audio('audio/greeting.wav')
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
