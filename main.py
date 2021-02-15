import spaceManagement as sm
import soldOutPrediciton as sop


def help():
    print("=== [ PREDIZIONE ] ===\n"
          "$ previsione_affluenza - prevede l'affluenza nel locale\n"
          "=== [ GESTIONE INVENTARIO ] ===\n"
          "$ inventario - comunica gli ingredienti presenti nell'inventario\n"
          "$ ho_acquistato INGREDIENTE QTY - aggiorna l'invetario con il prodotto nella quantitÃ  selezionata (default 1)\n"
          "$ cucina PIATTO - cucina il piatto inserito, modificando l'inventario\n"
          "=== [ PRODOTTI ] ====\n"
          "$ menu - mostra il menÃ¹ a disposizione\n"
          "$ cerca_ingrediente INGREDIENTE - mostra tutti i piatti con quell'ingrediente\n"
          "$ piatto_disponibile PIATTO - dice se, in base agli ingredienti, Ã¨ possibile eseguire il piatto\n"
          "$ caratteristica_piatto CARATTERISTICA PIATTO - considerando quella caratteristica (lattosio, vegetariano, vegano, celiaco) dice se puoi mangiare quel piatto\n"
          "$ piatto_per_chi PIATTO - dato un piatto, comunica chi può mangiare quel piatto"
          "=== [ QUERY MANUALE ] ===\n"
          "$ query QUERY - permette di effettuare una query al kb [es. query prop(pasta_tonno, requirement, X)]\n"
          "=== [ ESCI ] ===\n"
          "$ exit - esce dal programma\n")

#Comandi command Line
def elaborate_string(input):
    try:
        commands = input.split(" ")
        if commands[0] == 'help':
            help()
        elif commands[0] == 'query':
            sm.query(input[5:])
        elif commands[0] == 'menu':
            sm.menu()
        elif commands[0] == 'cerca_ingrediente':
            sm.cerca_ingrediente(commands[1:])
        elif commands[0] == 'piatto_disponibile':
            sm.piatto_disponibile(commands[1])
        elif commands[0] == 'inventario':
            sm.mostra_inventario()
        elif commands[0] == 'ho_acquistato':
            if len(commands) == 2:
                sm.ho_acquistato(commands[1])
            else:
                sm.ho_acquistato(commands[1], int(commands[2]))
        elif commands[0] == 'cucina':
            sm.cucina(commands[1])
        elif commands[0] == 'previsione_affluenza':
            sop.prediction()
        elif commands[0] == 'caratteristica_piatto':
            sm.caratteristica_piatto(commands[1], commands[2])
        elif commands[0] == 'piatto_per_chi':
            sm.piatto_per_chi(commands[1])
        elif commands[0] == 'exit':
            return
        else:
            print("Comando non valido")
    except ValueError as err:
        print("Attenzione!", err)
    except IndexError:
        print("Rispettare gli argomenti!")

if __name__ == '__main__':
    input_string = None
    while input_string != 'exit':
        input_string = input("$ ")
        elaborate_string(input_string)



