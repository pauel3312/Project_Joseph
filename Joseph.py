import webbrowser as web
import os
import SaveAndLoadCommands as sl
lb_reponse = None
lb_status = None


try:
    import tkinter as tk
    from tkinter import ttk
except ModuleNotFoundError:
    os.system("pip install tkinter")
    import tkinter as tk
    from tkinter import ttk
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


def voiceReckon():
    global joseph, lb_status, lb_reponse
    recognizer = Recognizer()
    with Microphone() as source:
        lb_status["text"] = "réglage du bruit ambiant...patientez..."
        joseph.update()
        recognizer.adjust_for_ambient_noise(source)
        lb_status["text"] = "vous pouvez parler..."
        joseph.update()
        recorded_audio = recognizer.listen(source)
#        recorded_audio = recognizer.record(source, 3) permet de modifier la durée de l'enregistrement
        lb_status["text"] = "enregistrement terminé"
        joseph.update()
    try:
        lb_status["text"] = "Reconnaissance du texte..."
        joseph.update()
        text = recognizer.recognize_google(
            recorded_audio,
            language="fr-FR"
        )
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
    for command in commands:
        if type(command[0]) == list:
            if command[2] == 'src':
                if command[0][0] and command[0][1] in txt:
                    a = txt.split(command[0][0])
                    a = a[1].split(command[0][1])
                    web.open(command[1] + a[0], new=0, autoraise=True)


def GUI():
    global joseph, marge_x, marge_y, lb_status, lb_reponse
    lb_status = tk.Label(joseph, bg="grey82", width=40)
    lb_reponse = tk.Label(joseph, bg="grey82", width=50)
    bt_voc = tk.Button(joseph, text="Joseph", command=voiceReckon)

    bt_voc.grid(row=5, column=0, padx=marge_x, pady=marge_y)
    lb_reponse.grid(row=7, column=0, padx=marge_x, pady=marge_y, rowspan=2)
    lb_status.grid(row=6, column=2, padx=marge_x, pady=marge_y)


Assistant_vocal = tk.Tk()
NoteBook = ttk.Notebook(Assistant_vocal)
joseph = ttk.Frame(NoteBook, width=400, height=280)
Creer_commandes = ttk.Frame(NoteBook, width=400, height=280)
NoteBook.add(joseph, text="Commander à votre esclave")
NoteBook.add(Creer_commandes, text="créer un ordre pour votre esclave")
NoteBook.grid()

commands = sl.load()

GUI()
Assistant_vocal.mainloop()
