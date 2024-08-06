import json
from typing import List, Tuple, Dict, Any
from threading import Thread


board: List[List[int]] = []
zet: Tuple[int, int] = (0, 0)
lijst_stukken: List[Tuple[str, int, int]] = []
relevante_stukken: List[Tuple[int, int]] = []

# Instelling voor de te detecteren kleur
TE_DETECTEREN_KLEUR:str = "Blauw"  # Verander dit naar "Rood" om rode zetten te beschouwen als mens

def recognize_move():
    zetten_mens=bepaal_relevante_zet()#vergeet de haakjes niet!!
    print("zetten_mens:",zetten_mens)#vorm: lijst van coordinaten(=[tuple(x,y),...])
    thread_controleer_vertraging=Thread(target=controleer_vertraging_data) #thread stoppen is moeilijk, daarom wordt die iedere keer opnieuw aangemaakt.
    thread_controleer_vertraging.start()
    for i in zetten_mens:
        try:
            int(i[0])
            int(i[1])

        except:
            raise Exception("De coordinaten moeten getallen zijn. Controleer de coordinaten in de beeldherkenning. (x,y)")
    try:
        if len(zetten_mens)==0:
            raise Exception("Er werd geen zet gedetecteerd.")

        elif len(zetten_mens)==1:
            print("1 zet, super")
            x,y=zetten_mens[0]
            antwoord=input("Klopt deze zet? (ja/nee) :",x,y)#todo: haal op termijn weg, wanneer de code betrouwbaar genoeg is.
            #=debugging
            if antwoord=="ja" or antwoord=="":
                pass
            else:
                raise Exception("")
            return x,y

        elif zetten_mens is None: #zou nooit mogen voorkomen
            raise Exception("Geen zetten, of variabele niet gedeclareerd")
        else:
            raise Exception("Meerdere zetten")

        
    except Exception as e:
        print("something went wrong with the recognition of the pieces:",e)
        return None



def initialiseer_spelbord_json_bestanden():
    import json
    relevante_stukken=[]
    pads=[r".\bord_gomoku\bord_na_zet.json",r".\bord_gomoku\bord_voor_zet.json"]

    for pad in pads:
        with open(pad, 'w') as json_file:
            json.dump({'stukken': relevante_stukken}, json_file)#zie lees_van_json

def controleer_vertraging_data():
    data=lees_van_json(r".\bord_gomoku\bord_na_zet.json")
    if data: #eerste keer zal dit nog geen waarde hebben
        from datetime import datetime
        huidige_timestamp=datetime.now().isoformat()

        huidige_tijd=huidige_timestamp.split("T")[1]
        huidige_datum=huidige_timestamp.split("T")[0]

        huidige_uren=int(huidige_tijd.split(":")[0])
        huidige_minuten=int(huidige_tijd.split(":")[1])
        huidige_seconden=float(huidige_tijd.split(":")[2])

        huidig_jaar=int(huidige_datum.split("-")[0])
        huidige_maand=int(huidige_datum.split("-")[1])
        huidige_dag=int(huidige_datum.split("-")[2])

        huidig_tijdstip=huidige_seconden+huidige_minuten*60+huidige_uren*3600

        print(data)
        tijd=data["timestamp"]
        datum=tijd.split("T")[0]
        tijd=tijd.split("T")[1]

        jaar=int(datum.split("-")[0])
        maand=int(datum.split("-")[1])
        dag=int(datum.split("-")[2])

        uren=int(tijd.split(":")[0])
        minuten=int(tijd.split(":")[1])
        seconden=float(tijd.split(":")[2])
        tijdstip=seconden+minuten*60+uren*3600

        max_vertraging=3
        datum_verschillend=(jaar!=huidig_jaar) or (maand!=huidige_maand) or (dag!=huidige_dag)
        tijd_verschillend= huidig_tijdstip>tijdstip+max_vertraging

        if datum_verschillend or tijd_verschillend:
            raise Exception("Herzie het programma, er zit te veel vertraging op." ,"Gebruik threads om vertraging op te lossen.")
        else:
            print("Deze data is minder dan 3 seconden oud.")
    
def lees_van_json(pad)-> List[Tuple[int, int]]:
    with open(pad, 'r') as json_file:
        data = json.load(json_file)
    return data["stukken"]#zie json.dump in schrijf_relevante_stukken_weg (dictionary naar lijst van tuples)

def bepaal_relevante_zet () -> List[Tuple[int, int]]:
    stukken_na_zet=lees_van_json(r".\bord_gomoku\bord_na_zet.json")
    stukken_voor_zet=lees_van_json(r".\bord_gomoku\bord_voor_zet.json")
    relevante_zetten=[]

    if stukken_voor_zet is None:
        stukken_voor_zet = []
    if stukken_na_zet is None:#mag niet voorkomen-daarom raise exception
        raise Exception("waarschijnlijk: fout in het gomoku programma, bekijk ook de functie schrijf_relevante_stukken_weg en programma met webcam")
        #stukken_na_zet = []
    for i in stukken_na_zet: #ik ga ervan uit dat er af en toe meerdere zetten gevonden kunnen worden, dit mag niet, maar een lijst is de gemakkelijkste manier om dit op te lossen.
        #als er meerdere stukken zijn, dan is er een fout/instabiliteitsprogramma in het programma dat de beeldherkenning doet.
        if i not in stukken_voor_zet:
            relevante_zetten.append(i)
    if relevante_zetten is None:
        raise Exception("Er geen zet gedaan. Controleer de beeldherkenning indien je fysiek wel een zet hebt uitgevoerd.")

    return relevante_zetten

def schrijf_relevante_stukken_weg(pad)->None:
    relevante_stukken = []
    data=lees_gedetecteerde_stukken()
    print("huidige_stukken:",data)
    
    if data:
        alle_stukken = set((stuk['color'], stuk['coordinates'][0], stuk['coordinates'][1]) for stuk in data['pieces'])#bevat alle unieke zetten
    
        for kleur, x, y in alle_stukken:
            if (kleur, x, y) not in lijst_stukken and kleur == TE_DETECTEREN_KLEUR:#enkel unieke stukken van relevante kleur toevoegen
                relevante_stukken.append((x, y))#als dit er meer dan 1 is, dan is er een fout in het vorige programma
        if len(relevante_stukken) > 0:
            print(f"Relevante stukken: {relevante_stukken}")
            with open(pad, 'w') as json_file:
                json.dump({'stukken': relevante_stukken}, json_file)#zie lees_van_json

        if relevante_stukken is None:
            print("Geen stukken van de relevante kleur gevonden, controleer beeldherkenning indien je fysiek wel een zet hebt uitgevoerd.")
    else:
        print("Geen stukken van de relevante kleur gevonden, controleer beeldherkenning indien je fysiek wel een zet hebt uitgevoerd.")

def schrijf_relevante_stukken_voor_zet_weg () :
    pad_relevante_stukken_voor_zet=r".\bord_gomoku\bord_voor_zet.json"
    schrijf_relevante_stukken_weg(pad_relevante_stukken_voor_zet)

def schrijf_relevante_stukken_na_zet_weg () :#kunnen er ook meer zijn (tot (15*15)/2 stukken)
    global board
    pad_relevante_stukken_na_zet=r".\bord_gomoku\bord_na_zet.json"
    schrijf_relevante_stukken_weg(pad_relevante_stukken_na_zet)


def lees_gedetecteerde_stukken() -> Dict[str, Any]:#retourneert alle stukken op het bord (leest json bestand)
    bestandspad = r'..\vijf_op_een_rij_beeldherkenning\detected_pieces.json'
    try:
        with open(bestandspad, 'r') as json_file:
            return json.load(json_file)
    except Exception as e:
        print(f"Fout bij het lezen van het JSON-bestand: {e}")
        return {}



