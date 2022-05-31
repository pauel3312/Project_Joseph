# --coding: utf-8 --
import webbrowser as web
import os
import SaveAndLoadCommands as Sl
from functools import partial
from time import sleep
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
    except Exception as ex:
        print(ex)
    try:
        if len(text) <= 50:
            lb_reponse["text"] = text
        else:
            lb_reponse["text"] = text[:int(len(text)/2)] + '\n' + text[int(len(text)/2):]
        lb_status["text"] = ""
        joseph.update()

        getCommands(text)
    except UnboundLocalError:
        lb_reponse["text"] = 'Vous n\'avez rien dit'


def rec_new_commands():
    global commands, Creer_commandes, lb_newCommand_status, lb_newCommand_reponse
    recognizer = Recognizer()
    with Microphone() as source:
        lb_newCommand_status["text"] = "réglage du bruit ambiant...patientez..."
        Creer_commandes.update()
        recognizer.adjust_for_ambient_noise(source)
        lb_newCommand_status["text"] = "vous avez 3 secondes"
        Creer_commandes.update()
        recorded_audio = recognizer.record(source, 3)
        lb_newCommand_status["text"] = "enregistrement terminé"
        Creer_commandes.update()
    try:
        lb_newCommand_status["text"] = "Reconnaissance du texte..."
        Creer_commandes.update()
        text = recognizer.recognize_google(
            recorded_audio,
            language="fr-FR"
        )
    except Exception as ex:
        print(ex)
    try:
        lb_newCommand_reponse["text"] = "vous avez dit : " + text
        lb_newCommand_status["text"] = ""
        Creer_commandes.update()
    except UnboundLocalError:
        lb_newCommand_reponse["text"] = 'Vous n\'avez rien dit'
        lb_newCommand_status["text"] = ""
        Creer_commandes.update()


def getCommands(txt):
    for command in commands:
        if type(command[0]) == list:
            if command[0][0] and command[0][1] in txt:
                if command[2] == 'src':
                    a = txt.split(command[0][0])
                    a = a[1].split(command[0][1])
                    web.open(command[1] + a[0], new=0, autoraise=True)
                    break
        elif type(command[0]) == str:
            if command[0] in txt:
                if command[2] == 'ws':
                    web.open(command[1], new=0, autoraise=True)
                    break
                elif command[2] == 'app':
                    os.system('START ' + command[1])
                    os.system("taskkill /im cmd.exe /f")
                    break
                elif command[2] == 'InnerFct':
                    eval(command[1])()
                    break
                elif command[2] == 'cmd':
                    os.system(command[1])
                    os.system("taskkill /im cmd.exe /f")
                    break
                elif command[2] == 'lst':
                    for c in command[1]:
                        if c[-4:] == '.exe':
                            os.system('START ' + c)
                            os.system("taskkill /im cmd.exe /f")
                        else:
                            web.open(c, new=0, autoraise=True)
                            break
                    break

def GUI():
    global joseph, marge_x, marge_y, lb_status, lb_reponse, lb_newCommand_status, lb_newCommand_reponse, Creer_commandes\
        , commands, en_newCommand_commande, cb_newCommand_type, afficher_commandes
    lb_status = tk.Label(joseph, bg="grey82", width=40)
    lb_reponse = tk.Label(joseph, bg="grey82", width=50)
    bt_voc = tk.Button(joseph, text="Joseph", command=voiceReckon)
    lb_indic_rec = tk.Label(Creer_commandes, text="enregistrer les mots-clés :")
    lb_indic_commande = tk.Label(Creer_commandes, text="Commande :")
    lb_indic_type = tk.Label(Creer_commandes, text="Type de commande :")
    lb_newCommand_status = tk.Label(Creer_commandes, text="", bg="grey82")
    lb_newCommand_reponse = tk.Label(Creer_commandes, text="", bg="grey82")
#    bt_newcommand_plus = tk.Button(Creer_commandes, text="+", command=addEntry)
    bt_newCommand_rec = tk.Button(Creer_commandes, text="Enregistrer", command=rec_new_commands)
    en_newCommand_commande = tk.Entry(Creer_commandes, width=30)
    cb_newCommand_type = ttk.Combobox(Creer_commandes, values=["Site Web (ws)",
                                                               "démarrer une application (app)",
                                                               "fonction interne au code (InnerFct)",
                                                               "commande MS-DOS (cmd)"],
                                      state="readonly",
                                      width=30)
    bt_save = tk.Button(Creer_commandes, text="Sauvegarder", command=SaveCommands)


    display_commands()

    bt_voc.grid(row=5, column=0, padx=marge_x, pady=marge_y)
    lb_reponse.grid(row=7, column=0, padx=marge_x, pady=marge_y, rowspan=2)
    lb_status.grid(row=6, column=2, padx=marge_x, pady=marge_y)
    bt_save.grid(row=5, column=2, padx=marge_x, pady=marge_y)
    lb_indic_rec.grid(row=0, column=0, padx=marge_x, pady=marge_y)
    lb_indic_commande.grid(row=1, column=0, padx=marge_x, pady=marge_y)
    en_newCommand_commande.grid(row=1, column=2, padx=marge_x, pady=marge_y)
    lb_indic_type.grid(row=2, column=0, padx=marge_x, pady=marge_y)
    bt_newCommand_rec.grid(row=0, column=2, padx=marge_x, pady=marge_y)
    lb_newCommand_status.grid(row=1, column=3, padx=marge_x, pady=marge_y)
    cb_newCommand_type.grid(row=2, column=2, padx=marge_x, pady=marge_y)
    lb_newCommand_reponse.grid(row=2, column=3, padx=marge_x, pady=marge_y)


def display_commands():
    global commands, afficher_commandes
    for widget in afficher_commandes.winfo_children():
        widget.destroy()
    bold = True
    bt_actualiser = tk.Button(afficher_commandes, text="Actualiser", command=display_commands)
    bt_actualiser.grid(row=0, column=4, padx=marge_x, pady=marge_y)
    for command in commands:
        lb_display_command_voc = tk.Label(afficher_commandes, text=command[0])
        if command[2] != "lst":
            lb_display_command_link = tk.Label(afficher_commandes, text=command[1])
        else:
            lb_display_command_link = ttk.Combobox(afficher_commandes, values=command[1], state="readonly", width=30)
            lb_display_command_link.set(command[1][0])
        lb_display_command_type = tk.Label(afficher_commandes, text=command[2])
        bt_delete_command = tk.Button(afficher_commandes, text="Supprimer", command=partial(delete_commands, command))
        if bold:
            lb_display_command_voc["font"] = ("Helvetica", "12", "bold")
            lb_display_command_link["font"] = ("Helvetica", "12", "bold")
            lb_display_command_type["font"] = ("Helvetica", "12", "bold")
        lb_display_command_voc.grid(row=commands.index(command), column=0)
        lb_display_command_link.grid(row=commands.index(command), column=1)
        lb_display_command_type.grid(row=commands.index(command), column=2)
        if not bold and command[2] != 'src':
            bt_delete_command.grid(row=commands.index(command), column=3)
        bold = False


def SaveCommands():
    global commands, en_newCommand_commande, cb_newCommand_type, lb_newCommand_reponse
    if en_newCommand_commande.get() != '' and (cb_newCommand_type.get() != '' and "vous avez dit :" in lb_newCommand_reponse.cget("text")
                                               and [lb_newCommand_reponse.cget("text").split(": ")[1],
                                                    en_newCommand_commande.get(),
                                                    cb_newCommand_type.get().split('(')[1].split(')')[0]] not in commands):
        commands.append([lb_newCommand_reponse.cget("text").split(": ")[1], en_newCommand_commande.get(),
                         cb_newCommand_type.get().split('(')[1].split(')')[0]])
        Sl.save(commands)
        lb_newCommand_reponse.config(text="commande enregistrée")
        en_newCommand_commande.delete(0, 'end')
        cb_newCommand_type.set('')
        Creer_commandes.update()
        sleep(1)
        lb_newCommand_reponse["text"] = ""
    else:
        lb_newCommand_reponse["text"] = "il manque quelque chose"
        Creer_commandes.update()
        sleep(1)
        lb_newCommand_reponse["text"] = ""


def delete_commands(command):
    global commands
    commands.remove(command)
    Sl.save(commands)
    display_commands()


Assistant_vocal = tk.Tk()
NoteBook = ttk.Notebook(Assistant_vocal)
joseph = ttk.Frame(NoteBook, width=400, height=280)
Creer_commandes = ttk.Frame(NoteBook, width=400, height=280)
afficher_commandes = ttk.Frame(NoteBook, width=400, height=280)
NoteBook.add(joseph, text="Commander à votre esclave")
NoteBook.add(Creer_commandes, text="créer un ordre pour votre esclave")
NoteBook.add(afficher_commandes, text="afficher les ordres de votre esclave")
NoteBook.grid()

commands = Sl.load()

GUI()
Assistant_vocal.title("Assistant vocal")
Assistant_vocal.mainloop()
