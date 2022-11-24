import pathlib
import requests
from bs4 import BeautifulSoup
import webbrowser

class ImmoWebsite:
    #read dicts from txt-file
    url_dict = {}
    neg_dict = {}
    if pathlib.Path("websites.txt").exists():
        with open("websites.txt", "r", encoding="utf-8") as file:
            for line in file:
                if " : " in line:
                    company, url = line.strip().split(" : ")
                    url_dict[company] = url
                elif " = " in line:
                    company_a, neg_ausdruck = line.strip().split(" = ")
                    neg_dict[company_a] = neg_ausdruck
    else:
        print("Error - file 'websites.txt' does not exist")
    
    number_of_flats_found = 0

    def __init__(self, company, already_seen=""):
        self.company = company
        self.url = ImmoWebsite.url_dict[company]
        self.neg_text = ImmoWebsite.neg_dict[company]
        self.already_seen = already_seen
        
    def abfrage(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, "html.parser")
        text_to_search_in = soup.get_text()
        #prüfen ob sinnvoller Text gefunden wurde (noch implementieren)
        #for entry in ImmoWebsite.neg_texts:
        if self.neg_text in text_to_search_in: #website text enthält Absage
            return str(self.company + ": Kein neues Angebot" + "\n")
        elif self.already_seen == text_to_search_in:
            return str(self.company + ": Angebot bereits angesehen. Kein neues Angebot." + "\n")
        else:
            self.already_seen = text_to_search_in
            ImmoWebsite.number_of_flats_found += 1 
            return str(self.company + ": Erfolg auf " + self.url + "\n")
            
    
#Instanzen verschiedener Wohnungsbaugesellschaften
gewobag = ImmoWebsite("gewobag")
sul = ImmoWebsite("sul")
gwnk = ImmoWebsite("gwnk")
degewo = ImmoWebsite("degewo")
ibw = ImmoWebsite("ibw")
    
def Erfolgssong():
    path_song = pathlib.Path('alarm.mp3')
    if path_song.exists():
        webbrowser.open('alarm.mp3')
    else:
        print("file 'alarm.mp3' not found")

