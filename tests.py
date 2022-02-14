import webbrowser as web
import os
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

joseph = tk.Tk()

commands = sl.load()


def voiceReckon():
    recognizer = Recognizer()

    with Microphone() as source:
        print("réglage du bruit ambiant...patientez...")
        recognizer.adjust_for_ambient_noise(source)
        print("vous pouvez parler...")
        recorded_audio = recognizer.listen(source)
        print("enregistrement terminé")
    try:
        print("Reconnaissance du texte...")
        text = recognizer.recognize_google(
            recorded_audio,
            language="fr-FR"
        )
        print("vous avez dit : {}".format(text))

    except Exception as ex:
        print(ex)
    getCommands(text)


def getCommands(txt):
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


bt_voc = tk.Button(joseph, text="Joseph", command=voiceReckon())
bt_voc.grid(row=0, column=0)
joseph.mainloop()
