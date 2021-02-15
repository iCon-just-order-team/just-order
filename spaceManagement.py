from pyswip import Prolog
from pyswip.prolog import PrologError

prolog = Prolog()
prolog.consult("kb.pl")

#Fa una query immessa dall'utente
def query(string):
    try:
        print(list(prolog.query(string)))
    except PrologError:
        print(string + ": Query non valida.")


#Mostra il menu attuale
def menu():
    #trova l'elenco delle ricette
    query_ricetta = "prop(X, subClassOf, ricetta), prop(Y, type, X)."
    ricettario = list(prolog.query(query_ricetta))
    print("Menu\n")

    # trova gli ingredienti per ogni ricetta
    for ricetta in ricettario:
        query_ingredienti = "prop(" + ricetta["Y"] + ", requirement, R)"
        ingredienti = list(prolog.query(query_ingredienti))
        print(ricetta["Y"], end=": ")
        i = 0
        for ingrediente in ingredienti:
            if len(ingredienti) - 1 == i:
                print(ingrediente["R"], end=".")
            else:
                print(ingrediente["R"], end=", ")
                i = i + 1
        print()


#Ottiene il cibo con quell'ingrediente
def cerca_ingrediente(ingredienti):
    #Creo la Query
    query = ""
    i = 0
    for ingrediente in ingredienti:
        query = query + "prop(" + ingrediente + ", is_contained, X)"
        if len(ingredienti) - 1 == i:
            query = query + "."
        else:
            query = query + ","
        i = i + 1

    #Stampo le varie ricetta
    ricettario = list(prolog.query(query))
    if ricettario:
        print("Le ricette che contengono ", end="")
        for ingrediente in ingredienti:
            print(ingrediente, end =" ")
        print("sono:")
        for ricetta in ricettario:
            print("- " + ricetta["X"])
    else:
        print("Non ci sono ricette disponibili che contengono", end=(" "))
        for ingrediente in ingredienti:
            print(ingrediente, end=" ")
    print()



#Dice se un piatto e disponibile in base agli ingredienti nel magazzino
def piatto_disponibile(piatto):
    piatto_presente(piatto)
    ingredienti_mancanti = list(prolog.query("prop(" + piatto + ", not_available_items, X)"))
    if not ingredienti_mancanti:
        print("Il piatto " + piatto + " e' disponibile")
    else:
        print("Il piatto " + piatto + " NON e' disponibile\nGli ingredienti mancanti sono: ")
        for ingrediente in ingredienti_mancanti:
            print("- " + ingrediente["X"])
        print( )


#visualizza i prodotti presenti nell'invetario
def mostra_inventario():
    #Ingredienti presenti nell'inventario
    ingredienti = list(prolog.query("prop(X, in_inventory, true)."))
    print("Gli ingredienti a disposizione sono: ")
    for ingrediente in ingredienti:
        availability = list(prolog.query("prop(" + ingrediente["X"] + ", availability, X)."))[0]['X']
        print("-" + ingrediente["X"] + ": " + str(availability) + " pz.")

    #Ingredienti mancanti nell'inventario
    ingredienti_mancanti = list(prolog.query("prop(X, in_inventory, false)."))
    if ingredienti_mancanti:
        print("Bisogna acquistare i seguenti ingredienti:", end=' ')
        for ingrediente in ingredienti_mancanti:
            print(ingrediente["X"], end=", ")
        print()


#Aggiunge nell'invetario la quantita  di quell'elemento acquistato
def ho_acquistato(ingrediente, qty=1):
    try:
        valore_precedente = list(prolog.query("prop(" + ingrediente + " , availability, X)"))[0]['X']
        prolog.retract("prop(" + ingrediente + " , availability," + str(valore_precedente) + ")")
        prolog.assertz("prop(" + ingrediente + " , availability," + str(valore_precedente + qty) + ")")
        print(str(qty) + " " + ingrediente + "(i) aggiunti nel magazzino")
    except IndexError:
        print("L'ingrediente non esiste!")


def cucina(piatto):
    piatto_disponibile(piatto)
    ingredienti_mancanti = list(prolog.query("prop(" + piatto + ", not_available_items, X)"))
    if not len(ingredienti_mancanti):
        ingredienti_usati = list(prolog.query("prop(" + piatto + ", requirement, X)."))
        for ingrediente in ingredienti_usati:
            valore_precedente = list(prolog.query("prop(" + ingrediente['X'] + " , availability, X)"))[0]['X']
            prolog.retract("prop(" + ingrediente['X'] + " , availability," + str(valore_precedente) + ")")
            prolog.assertz("prop(" + ingrediente['X'] + " , availability," + str(valore_precedente - 1) + ")")
        print("Inventario aggiornato.")


def caratteristica_piatto(caratteristica, piatto):
    piatto_presente(piatto)

    if not (caratteristica in ["lattosio", "vegetariano", "vegano", "celiaco"]):
        raise ValueError(repr(caratteristica) + ": Caratteristica non valida!")
    value = list(prolog.query("not(prop(" + piatto + ", is_not_for, " + caratteristica + "))."))
    if value:
        print("Questa pietanza è adatta per un " + caratteristica)
    else:
        if caratteristica == "lattosio":
            risposta = "Questa pietanza non è adatta per un intollerante al lattosio, perchè contiene: "
        else:
            risposta = "Questa pietanza non è adatta per un " + caratteristica + " perchè contiene: "
        ingredienti = list(prolog.query("prop(" + piatto + ", requirement, X )."))
        for ingrediente in ingredienti:
            value2 = len(list(prolog.query("prop(" + ingrediente['X'] + ", is_not_for, " + caratteristica + ").")))
            if value2:
                risposta = risposta + ingrediente['X'] + "; "
        print(risposta)

def piatto_per_chi(piatto):
    piatto_presente(piatto)

    caratteristiche = ["lattosio", "vegetariano", "vegano", "celiaco"]
    print("Nelle seguenti categorie: " + str(caratteristiche) + ", il piatto può essere mangiato da")
    value = list(prolog.query("prop(" + piatto + ", is_not_for, X)."))
    i = 0
    while(i < len(value)):
        j = 0
        while(j < len(caratteristiche)):
            if caratteristiche[j] == value[i]['X']:
                caratteristiche.remove(caratteristiche[j])
            else:
                j = j + 1
        i = i + 1

    if not caratteristiche:
        print("nessuno dei precedenti")
    else:
        print("chi ha le intolleranze/preferenze alimentari seguenti: " + str(caratteristiche))

#Dice se un piatto esiste nel menu - di controllo
def piatto_presente(piatto):
    ricettario = list(prolog.query("prop(X, subClassOf, ricetta), prop(Y, type, X)."))
    check = False
    for ricetta in ricettario:
        if ricetta['Y'] == piatto:
            check = True
            break
    if not check:
        raise ValueError(piatto + " non è nel ricettario.")