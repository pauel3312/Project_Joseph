import webbrowser as web
import os
from functools import  partial

import pyaudio

import SaveAndLoadCommands as sl
try:
    import tkinter as tk
except ModuleNotFoundError:
    os.system("pip install tkinter")
    import tkinter as tk
try:
    from pyaudio import *
except ModuleNotFoundError:
    os.system("pip install " + os.path.dirname(__file__) + "\PyAudio-0.2.11-cp310-cp310-win32.whl")
    from pyaudio import *
try:
    from speech_recognition import Recognizer, Microphone
except ModuleNotFoundError:
    os.system("pip install Speechrecognition")
    from speech_recognition import Recognizer, Microphone
marge_x = 10
marge_y = 10
recognizer = Recognizer()
recognizer.dynamic_energy_threshold = True



def getAudio():
    global lb_status, joseph, lb_reponse, recognizer, record_audio
    lb_status["text"] = "vous pouvez parler..."
    joseph.update()
    record_audio()
#         recorded_audio = recognizer.record(source, 3) permet de modifier la durée de l'enregistrement
    lb_status["text"] = "enregistrement terminé"
    joseph.update()


def RecognizeAudio(recognizer, recorded_audio):
    print("IsRunning!")
    try:
        lb_status["text"] = "Reconnaissance du texte..."
        joseph.update()
        text = recognizer.recognize_google(recorded_audio, language="fr-FR")
        if len(text) <= 50:
            lb_reponse["text"] = text
        else:
            lb_reponse["text"] = text[:int(len(text)/2)] + '\n' + text[int(len(text)/2):]
        lb_status["text"] = ""
        joseph.update()
    except Exception as ex:
        print(ex)
    getCommands(text)


def getCommands(txt):
    global joseph
    for key in commands.keys():
        if commands[key][1] == 'ws':
            if key in txt:
                web.open(commands[key][0], new=0, autoraise=True)
        elif commands[key][1] == 'src':
            if key[0] in txt and key[1] in txt:
                a = txt.split(key[0])
                a = a[1].split(key[1])
                web.open(commands[key][0] + a[0], new=0, autoraise=True)
        elif commands[key][1] == 'app':
            if key in txt:
                os.system("START " + commands[key][0])
        elif commands[key][1] == 'innerFct':
            if commands[key][0] == 'Fermer':
                joseph.destroy()
                exit(0)


with Microphone() as microphone:
    recognizer.adjust_for_ambient_noise(microphone)
record_audio = recognizer.listen_in_background(Microphone(), RecognizeAudio)
joseph = tk.Tk()
commands = sl.load()
lb_status = tk.Label(joseph, bg="grey82", width=40)
lb_status.grid(row=6, column=2, padx=marge_x, pady=marge_y)
lb_reponse = tk.Label(joseph, bg="grey82", width=50)
lb_reponse.grid(row=7, column=0, padx=marge_x, pady=marge_y, rowspan=2)
bt_voc = tk.Button(joseph, text="Joseph", command=getAudio)
bt_voc.grid(row=5, column=0, padx=marge_x, pady=marge_y)
joseph.mainloop()
