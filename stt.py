import vosk
import sys
import sounddevice as sd
import queue
import json

model = vosk.Model("model_small")
samplerate = 16000
device = 1
vosk.SetLogLevel(0)
q = queue.Queue()


def q_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def va_listen(timeout=10):
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                           channels=1, callback=q_callback):
        print('LISTENING...')
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = rec.Result()
                text = json.loads(result).get('text', '')

                if text:
                    print(f"Recognized: {text}")
                    return text
            # else:
            #     partial_result = rec.PartialResult()
            #     print(partial_result)
