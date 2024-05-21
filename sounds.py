import soundfile as sf
import sounddevice as sd

def play_audio(file_path: str):
    audio_data, sample_rate = sf.read(file_path, dtype='int16')
    sd.play(audio_data, sample_rate)
    sd.wait()  # Ждем завершения воспроизведения
