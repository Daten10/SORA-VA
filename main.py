# TODO
# запросы в гугле DONE
# работа с текстовыми файлами
# прикрутить чатгпт
# запуск приложений
# интерфейс

import random
import pvporcupine
import concurrent.futures
from stt import va_listen
from pvrecorder import PvRecorder
from commands import process_command
from sounds import play_audio, greetings, privet


# Настройки Porcupine
porcupine = pvporcupine.create(
    access_key='o3KmvBWPoF5Yv8XuqnzneJ3q8j2Xb2SCpvYTaclVJ6Rox1tT2+pC2A==',
    keyword_paths=['wake_word.ppn'],  # Замените на путь к вашему файлу ключевого слова
    model_path='porcupine_params_ru.pv'  # Замените на путь к русской модели Porcupine
)

recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)


def main():
    play_audio(random.choice(privet))
    try:
        recorder.start()
        print('Listening for wake word...')

        with concurrent.futures.ThreadPoolExecutor() as executor:
            while True:
                pcm = recorder.read()
                keyword_index = porcupine.process(pcm)

                if keyword_index >= 0:
                    print('Wake word detected!')
                    play_audio(random.choice(greetings))

                    future = executor.submit(va_listen, timeout=10)
                    command = future.result()
                    if command:
                        process_command(command)

    except KeyboardInterrupt:
        print('Stopping...')
    finally:
        recorder.stop()
        porcupine.delete()


if __name__ == "__main__":
    main()
