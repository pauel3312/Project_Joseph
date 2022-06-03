# --coding: utf-8 --
############################# import des librairies ###############################
import webbrowser as web
import os
import SaveAndLoadCommands as Sl
from functools import partial
from time import sleep

NInputFields = 1
list_InputWidgets = []

############################# vérification de la présence des librairies sur la machine ###############################

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

############################# fonction principale d'enregistrement ###############################

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
            lb_reponse["text"] = text[:int(len(text) / 2)] + '\n' + text[int(len(text) / 2):]
        lb_status["text"] = ""
        joseph.update()

        getCommands(text)
    except UnboundLocalError:
        lb_reponse["text"] = 'Vous n\'avez rien dit'

############################# fonction d'enregistrement d'une nouvelle comande ###############################

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

############################# fonction d'exécution de la commande ###############################

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
                elif command[2] == 'file':
                    os.startfile(command[1])
                    os.system("taskkill /im cmd.exe /f")
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
                        if c[1] == 'cmd':
                            os.system(c[0])
                        elif c[1] == 'file':
                            os.startfile(c[0])
                        elif c[1] == 'ws':
                            web.open(c[0], new=0, autoraise=True)
                        elif c[1] == 'app':
                            os.system('START ' + c[0])
                    break

############################# fonction GUI ###############################

def GUI():
    global joseph, marge_x, marge_y, lb_status, lb_reponse, lb_newCommand_status, lb_newCommand_reponse, \
        Creer_commandes, commands, afficher_commandes
    lb_status = tk.Label(joseph, bg="grey82", width=40)
    lb_reponse = tk.Label(joseph, bg="grey82", width=50)
    bt_voc = tk.Button(joseph, text="Joseph", command=voiceReckon)
    updateInputWidgets()

    display_commands()

    bt_voc.grid(row=5, column=0, padx=marge_x, pady=marge_y)
    lb_reponse.grid(row=7, column=0, padx=marge_x, pady=marge_y, rowspan=2)
    lb_status.grid(row=6, column=2, padx=marge_x, pady=marge_y)

############################# fonction ajout de commandes ###############################

def updateInputWidgets():
    global list_InputWidgets, lb_newCommand_status, lb_newCommand_reponse, Creer_commandes
    for widget in Creer_commandes.winfo_children():
        widget.destroy()
    list_InputWidgets = []
    bt_save = tk.Button(Creer_commandes, text="Sauvegarder", command=SaveCommands)
    lb_indic_rec = tk.Label(Creer_commandes, text="enregistrer les mots-clés :")
    bt_newcommand_plus = tk.Button(Creer_commandes, text="+", command=partial(UpdateEntries, 1))
    bt_newcommand_moins = tk.Button(Creer_commandes, text="-", command=partial(UpdateEntries, -1))
    bt_newCommand_rec = tk.Button(Creer_commandes, text="Enregistrer", command=rec_new_commands)
    lb_newCommand_status = tk.Label(Creer_commandes, text="", bg="grey82")
    lb_newCommand_reponse = tk.Label(Creer_commandes, text="", bg="grey82")
    lb_newCommand_status.grid(row=1, column=3, padx=marge_x, pady=marge_y)
    lb_newCommand_reponse.grid(row=2, column=3, padx=marge_x, pady=marge_y)
    bt_newcommand_plus.grid(row=2 + 2 * NInputFields, column=1, padx=marge_x, pady=marge_y)
    bt_newcommand_moins.grid(row=1, column=1, padx=marge_x, pady=marge_y)
    bt_newCommand_rec.grid(row=0, column=2, padx=marge_x, pady=marge_y)
    lb_indic_rec.grid(row=0, column=0, padx=marge_x, pady=marge_y)
    bt_save.grid(row=5 + 2 * NInputFields, column=2, padx=marge_x, pady=marge_y)
    for i in range(NInputFields):
        lb_indic_commande = tk.Label(Creer_commandes, text="Commande {} :".format(i + 1))
        lb_indic_type = tk.Label(Creer_commandes, text="Type de la commande {} :".format(i + 1))
        en_newCommand_commande = tk.Entry(Creer_commandes, width=30)
        if NInputFields == 1:
            cb_newCommand_type = ttk.Combobox(Creer_commandes, values=["Site Web (ws)",
                                                                       "démarrer une application (app)",
                                                                       "fonction interne au code (InnerFct)",
                                                                       "commande MS-DOS (cmd)",
                                                                       "fichier avec chemin d'accès (file)"],
                                              state="readonly",
                                              width=30)
        else:
            cb_newCommand_type = ttk.Combobox(Creer_commandes, values=["Site Web (ws)",
                                                                       "démarrer une application (app)",
                                                                       "commande MS-DOS (cmd)",
                                                                       "fichier avec chemin d'accès (file)"],
                                              state="readonly",
                                              width=30)
        list_InputWidgets.append([en_newCommand_commande, cb_newCommand_type])
        en_newCommand_commande.grid(row=1 + 2 * i, column=2, padx=marge_x, pady=marge_y)
        cb_newCommand_type.grid(row=2 + 2 * i, column=2, padx=marge_x, pady=marge_y)
        lb_indic_commande.grid(row=1 + 2 * i, column=0, padx=marge_x, pady=marge_y)
        lb_indic_type.grid(row=2 + 2 * i, column=0, padx=marge_x, pady=marge_y)


def UpdateEntries(N):
    global NInputFields, list_InputWidgets
    if NInputFields + N in range(1, 15):
        NInputFields += N
        updateInputWidgets()

############################# fonction affichage des commandes ###############################

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

############################# fonction enregistrement des commandes ###############################

def SaveCommands():
    global commands, lb_newCommand_reponse, list_InputWidgets, lb_NewCommand_status
    if len(list_InputWidgets) == 1:
        en_newCommand_commande = list_InputWidgets[0][0]
        cb_newCommand_type = list_InputWidgets[0][1]
        if en_newCommand_commande.get() != '' and (cb_newCommand_type.get() != '' and
                                                   "vous avez dit :" in lb_newCommand_reponse.cget("text")
                                                   and [lb_newCommand_reponse.cget("text").split(": ")[1],
                                                        en_newCommand_commande.get(),
                                                        cb_newCommand_type.get().split('(')[1].split(')')[0]]
                                                   not in commands):
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
    else:
        add = True
        ListOfCommands = []
        for InputWidgets in list_InputWidgets:
            en_newCommand_commande = InputWidgets[0]
            cb_newCommand_type = InputWidgets[1]
            if InputWidgets[0].get() != '' \
                    and cb_newCommand_type.get() != '' \
                    and "vous avez dit :" in lb_newCommand_reponse.cget("text"):
                ListOfCommands.append((en_newCommand_commande.get(),
                                       cb_newCommand_type.get().split('(')[1].split(')')[0]))
            else:
                lb_newCommand_reponse["text"] = "il manque quelque chose"
                Creer_commandes.update()
                sleep(1)
                lb_newCommand_reponse["text"] = ""
                add = False
        if add:
            commands.append([lb_newCommand_reponse.cget("text").split(": ")[1], ListOfCommands, "lst"])
            Sl.save(commands)
            lb_newCommand_reponse.config(text="commande enregistrée")
            for InputWidgets in list_InputWidgets:
                InputWidgets[0].delete(0, 'end')
                InputWidgets[1].set('')
            Creer_commandes.update()
            sleep(1)
            lb_newCommand_reponse["text"] = ""


def delete_commands(command):
    global commands
    commands.remove(command)
    Sl.save(commands)
    display_commands()

############################# MAIN (appel des fonctions) ###############################

Assistant_vocal = tk.Tk()

NoteBook = ttk.Notebook(Assistant_vocal)
joseph = ttk.Frame(NoteBook, width=400, height=280)
Creer_commandes = ttk.Frame(NoteBook, width=400, height=280)
afficher_commandes = ttk.Frame(NoteBook, width=400, height=280)

NoteBook.add(joseph, text="exécuter une commande")
NoteBook.add(Creer_commandes, text="créer une nouvelle commande")
NoteBook.add(afficher_commandes, text="gérer la liste des commandes")
NoteBook.grid()

commands = Sl.load()

GUI()
Assistant_vocal.title("Assistant vocal")
Assistant_vocal.mainloop()


############################# FIN ###############################
