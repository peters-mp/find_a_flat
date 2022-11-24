import find_a_flat 
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from threading import Thread
import time
import webbrowser

such_status = False

class App(tk.Tk):    
    def __init__(self):
        super().__init__()
        self.title('Wohnungssuche')
        self.geometry('600x300')
               
class BtnFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.play_sound = tk.StringVar()
        self.abfrage_haeufigkeit = tk.IntVar()
        self.messagebox_var = tk.StringVar()
        #label
        self.header = ttk.Label(self, text = "Menü")
        self.header.pack()
        #button1
        self.btn1 = ttk.Button(self, text = "Suche starten")
        self.btn1['command'] = self.suche_starten
        self.btn1.pack(side = 'top', expand = False, fill = 'x')
        #checkbox if you want to play sound
        self.cb_play_sound = ttk.Checkbutton(self, text = 'Play sound', variable = self.play_sound)
        self.cb_play_sound.pack(side = 'top', expand = False, fill = 'x')
        #button2
        self.btn2 = ttk.Button(self, text = "Suche stoppen")
        self.btn2['command'] = self.suche_stoppen
        self.btn2.pack(side = 'top', expand = False, fill = 'x')
        #label for entry1
        self.L_entry1 = ttk.Label(self, text = "Abfragehäufigkeit [s]")
        self.L_entry1.pack(side = 'top', expand = False, fill = 'x')
        #entry1
        self.entry1 = ttk.Entry(self, textvariable = self.abfrage_haeufigkeit)
        self.abfrage_haeufigkeit.set(60) #default 60s
        self.entry1.pack(side = 'top', expand = False, fill = 'x')
        #button3
        self.btn3 = ttk.Button(self, text = "Suchekriterien anpassen")
        self.btn3['command'] = self.suchkriterien_anpassen
        self.btn3.pack(side = 'top', expand = False, fill = 'x')
        #messagebox
        self.messagebox = ttk.Label(self, textvariable = self.messagebox_var)
        self.messagebox.pack(side = 'top', expand = False, fill = 'x')
        # show the frame on the container
        self.pack(side = 'right', expand = True, fill = 'both')
    
    def suche_stoppen(self):
        global such_status
        such_status = False
    
    def suche_starten(self): 
        global such_status
        such_status = True
        t1 = Thread(target=suche) #in subprocess, damit die suche bis zum stopp ausgeführt wird
        t1.start()
        
    def suchkriterien_anpassen(self):
        self.suche_stoppen()
        webbrowser.open("websites.txt")
        

class ContentFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        #options = {'padx' : 5, 'pady' : 5}
        #inhalt
        self.textbox = ScrolledText(self, height = 200, width = 200)
        self.textbox.pack(side = 'top', expand = True, fill = 'both')
        # show the frame on the container
        self.pack(side = 'left', expand = True, fill = 'both')
    
def suche():
    while such_status == True:
        find_a_flat.ImmoWebsite.number_of_flats_found = 0
        #websites abfragen und Ergebnisse in Var ablegen:
        ergebnis_text = (find_a_flat.gewobag.abfrage()
                        + find_a_flat.sul.abfrage()
                        + find_a_flat.gwnk.abfrage()
                        + find_a_flat.degewo.abfrage()
                        + find_a_flat.ibw.abfrage()
                        + str("\n" + "aktualisiert: " + time.strftime("%H:%M:%S") + "\n" + "\n"))
        content_frame.textbox.insert('0.0', ergebnis_text)
        #print(ergebnis_text)
        #Gesamtanzahl an neuen(!) Treffern?
        if find_a_flat.ImmoWebsite.number_of_flats_found > 0 and btn_frame.play_sound.get() == "1":
            print("play sound")
            find_a_flat.Erfolgssong() #Alarm abspielen
        try:
            wait_time = btn_frame.abfrage_haeufigkeit.get()
        except ValueError:
            wait_time = 60
            btn_frame.messagebox_var.set('ValueError, take default 60s')
        time.sleep(wait_time)
        
        
if __name__ == '__main__':
    app = App() #erzeuge Instanz des windows
    btn_frame = BtnFrame(app) #erzeuge Instanz des MainFrame im Container "app"
    content_frame = ContentFrame(app) #erzeuge Instanz des ContentFrames
    app.mainloop()
    