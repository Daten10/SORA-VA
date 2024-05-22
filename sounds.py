import soundfile as sf
import sounddevice as sd

greetings = ['audio/r1.wav', 'audio/r2.wav', 'audio/r3.wav']
do = ['audio/commands/budetsdelano.wav', 'audio/commands/secundochku.wav', 'audio/commands/secundu.wav',
      'audio/commands/vipolnyau.wav']
again = ['audio/commands/esheraz.wav', 'audio/commands/neponyala.wav', 'audio/commands/takoinet.wav',]

privet = ['audio/privet.wav', 'audio/greeting.wav', 'audio/zdr.wav']

def play_audio(file_path: str):
    audio_data, sample_rate = sf.read(file_path, dtype='int16')
    sd.play(audio_data, sample_rate)
    sd.wait()  # Ждем завершения воспроизведения
