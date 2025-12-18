import json, pyaudio, webbrowser,keyboard,time
from  vosk import Model, KaldiRecognizer

model=Model('Small_model')
rec=KaldiRecognizer(model,16000)
p= pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,channels=1,rate=16000,input=True, frames_per_buffer=8000)
stream.start_stream()

def listen():
    while(True):
        data = stream.read(4000,exception_on_overflow=False)
        if(rec.AcceptWaveform(data))and (len(data) > 0):
            answer= json.loads(rec.Result())
            if answer['text']:
                yield answer['text']
for text in listen():
    print(text)
    if 'бананы' in text:
        webbrowser.open('https://cdn.wallpaperjam.com/532c2ccccebc81ece939618290fbc5f59e1fb199/fruits-food-bananas-white-background.jpg')
    elif 'дым' in text:
        keyboard.press('g')
        time.sleep(0.2)
        keyboard.release('g')
    elif 'тепловизор' in text:
        keyboard.press('x')
        time.sleep(0.2)
        keyboard.release('x')
    elif 'покинуть машину'in text:
        keyboard.press('j')
        time.sleep(3.2)
        keyboard.release('j')
    elif 'стоп машина'in text:
        keyboard.release('w')
        keyboard.release('s')
        keyboard.press('k')
        time.sleep(0.2)
        keyboard.release('k')
    elif 'вперёд'in text:
        keyboard.press('w')