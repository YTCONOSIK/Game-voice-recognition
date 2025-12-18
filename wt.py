import vosk
import sounddevice as sd
import queue
import json
import pyttsx3

import keyboard
import time
import threading
import random
from jokes import jokes

# from mss import mss
# from PIL import Image
# from pytesseract import pytesseract


vosk_model = vosk.Model('vosk-model-small-ru-0.22')
samplerate = 16000
device = 8
q = queue.Queue()
rec = vosk.KaldiRecognizer(vosk_model, samplerate)
spd = False
thr = 0


def q_callback(indata, *_):
    q.put(bytes(indata))


def listen():
    try:
        with sd.RawInputStream(samplerate=samplerate, blocksize=1000, device=device, dtype='int16', channels=1,
                               callback=q_callback):
            print('Слушаю..')
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    text = json.loads(rec.Result())['text']
                    break

        return text
    except:
        pass


# def get_info():
#     global spd, thr
#     while True:
#         with mss() as sct:
#             sct.shot()
#         img = Image.open('monitor-1.png')
#         thr_img = img.crop((250, 40, 400, 70))
#         spd_img = img.crop((250, 70, 400, 100))
#         pytesseract.tesseract_cmd = 'tesseract/tesseract.exe'
#
#         try:
#             thr = int(pytesseract.image_to_string(thr_img).lower().split()[0])
#         except:
#             thr = None
#
#         try:
#             spd = int(pytesseract.image_to_string(spd_img).lower().split()[0])
#         except:
#             spd = None
#
#         time.sleep(2)
#
#
# threading.Thread(target=get_info).start()

key_map = {
    'выстрел': 'k',
    'огонь': 'k',
    'дрон': 'alt+0',
    'дым': 'g',
    'прицел': 'shift',
    'ковш': 'ctrl+t',
    'дистанция': 'x',
    'завеса': 'h',
    'первый': '1',
    'второй': '2',
    'третий': '3',
    'полный вперёд': 'e*3',
    'полный назад': 'q*3',
    'вперёд': 'e',
    'назад': 'd',

    'ловушки': 'alt+e',
    'ловушке': 'alt+e',
    'шасси': 'g',
    'закрылки': 'f',
    'тормоз': 'h',
    'сброс': 'space',
    'захват': 'alt+x',
    'ракета': '4',
    'пуск': 'alt+p'
}


def say(text, in_thread=False):
    if not in_thread:
        threading.Thread(target=say, args=(text, True)).start()
    else:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

        if engine._inLoop:
            engine.endLoop()


def main():

    text = listen()
    print(f'Распознано: {text}')

    for key in key_map:
        if key not in text:
            continue

        n = 1
        if '*' in key_map[key]:
            key, n = key_map[key].split('*')
        else:
            key = key_map[key]

        for _ in range(int(n)):
            keyboard.press(key)
            time.sleep(.1)
            keyboard.release(key)
            time.sleep(.1)

    if 'стоп' in text:
        keyboard.press('w')
        time.sleep(.1)
        keyboard.release('w')
        keyboard.release('s')

    if 'катапультирование' in text or 'катапультирования' in text or 'покинуть машину' in text:
        keyboard.press('j')
        time.sleep(3)
        keyboard.release('j')

    if 'полная тяга' in text or 'форсаж' in text:
        keyboard.release('ctrl')
        keyboard.press('shift')

        start = time.time()
        while thr != 110:
            if time.time() - start > 3:
                keyboard.release('shift')
                return

        keyboard.release('shift')

    if 'минимальная тяга' in text:
        keyboard.press('ctrl')
        time.sleep(2)
        keyboard.release('ctrl')

    if 'взлёт' in text:
        say('Выполняю автоматический взлёт')
        keyboard.press('shift')
        time.sleep(1)
        keyboard.release('shift')

        start = time.time()
        while not spd or spd < 400:
            print(spd, thr)
            if time.time() - start > 100:
                say('Произошла ошибка')
                return

        keyboard.press('s')
        time.sleep(.8)
        keyboard.release('s')

        say('Автоматический взлёт успешно выполнен')

    # if 'отчёт' in text:
    #     img = Image.open('monitor-1.png')
    #     thr_img = img.crop((250, 40, 400, 70))
    #     spd_img = img.crop((250, 70, 400, 100))
    #
    #     thr_img.save('thr.png')
    #     spd_img.save('spd.png')
    #
    #     engine = pyttsx3.init()
    #
    #     if spd:
    #         engine.say(f'Скорость: {spd} километров в час')
    #     else:
    #         engine.say(f'Нет данных о скорости')
    #
    #     if thr:
    #         engine.say(f'Тяга: {thr} процентов')
    #     else:
    #         engine.say(f'Нет данных о тяге')
    #
    #     engine.runAndWait()

    if 'остановка' in text:
        keyboard.release('shift')
        keyboard.press('ctrl')

    if 'анекдот' in text:
        say(random.choice(jokes))


if __name__ == '__main__':
    while True:
        main()
