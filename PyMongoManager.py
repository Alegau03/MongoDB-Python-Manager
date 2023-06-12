import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import time
from colorama import Fore


# POSSO SCEGLIERE A CHE DATABASE CONNETTERMI
def connection():
    print("\n")
    print(Fore.BLUE+"\n                                 BENVENUTO NEL GESTORE PYTHON MONGODB!")
    print("\n")
    time.sleep(0.5)
    cl=input(Fore.WHITE+" INSERISCI L'INDIRIZZO DEL DATABASE, SE è QUELLO STANDARD SCRIVERE STANDARD -> ")
    time.sleep(0.5)
    if cl=="standard" or cl=="STANDARD" or cl=="Standard":
        cl = "mongodb://localhost:27017"
    database=input(Fore.LIGHTWHITE_EX+"\n INSERIRE IL NOME DEL DATABASE -> ")
    
    time.sleep(0.5)

    uC=input("\n INSERIRE LA COLLECTION -> ")
    
    time.sleep(0.5)

    print(Fore.LIGHTMAGENTA_EX+"\n MI COLLEGO AL DATABASE ALL' INDIRIZZO: ",cl," CON NOME: ",database," ALLA COLLECTION DI NOME: ",uC)
    time.sleep(1.3)
    return cl,database,uC

#CONNESSIONE AL DATABASE
cl,database,uC=connection()

client = MongoClient(cl)

db= client.get_database(database)

usersCollection = db.get_collection(uC)


#OPERAZIONI DI RICERCA
def ricerca():
    print("\n")
    

    print("\n                                 PUOI CERCARE PER: NOME,COGNOME, ETA, COMUNE DI RESIDENZA ")

    time.sleep(0.5)
    ric=input(" DIGITA PER COSA VUOI CERCARE (nome,cognome,età,comune) -> ").lower()
    time.sleep(0.5)
    print("\n")
    
    print("\n VUOI CERCARE PER: "+ ric.upper())
    if ric=="nome":
        time.sleep(0.5)
        nome_da_cercare=input("\n INSERISCI IL NOME DA CERCARE CON MAIUSCOLE E MINUSCOLE CORRETTE -> ")
        time.sleep(0.5)
        query={"nome":{"$regex": nome_da_cercare}}
        
        
    if ric=="cognome":
        time.sleep(0.5)
        cognome_da_cercare=input("\n INSERISCI IL COGNOME DA CERCARE CON MAIUSCOLE E MINUSCOLE CORRETTE -> ")
        time.sleep(0.5)
        query={"cognome":{"$regex": cognome_da_cercare}}

    if ric=="età" or ric=="eta":
        time.sleep(0.5)
        gtorlt=input("\n CERCARE PER ETA' MAGGIORE DI O MINORE DI (INSERIRE gt o lt) -> ")
        if gtorlt=="gt":
            time.sleep(0.5)
            eta_da_cercare=input("\n INSERISCI L'ETA' DA CERCARE IN NUMERO -> ")
            time.sleep(0.5)
            query={"età":{"$gt":int(eta_da_cercare)}}

        if gtorlt=="lt":
            time.sleep(0.5)
            eta_da_cercare=input("\n INSERISCI L'ETA' DA CERCARE IN NUMERO -> ")
            time.sleep(0.5)
            query={"età":{"$lt":int(eta_da_cercare)}}

    if ric=="comune":
        time.sleep(0.5)
        comune_da_cercare=input("\n INSERISCI IL COMUNE DA CERCARE CON MAIUSCOLE E MINUSCOLE CORRETTE -> ")
        time.sleep(0.5)
        query={"Comune Residenza":{"$regex": comune_da_cercare}}
    
    result=usersCollection.find(query)
    file = open('result.txt','w',encoding="UTF8")
    for user in result:
            print(user)
            print(user, file=file, sep="\n")
    print("\n")
    print("\n                                 LAVORO ULTIMATO!\n")
    continuare=input("\n VUOI CERCARE ALTRO? S/N -> ")
    if continuare=="s" or continuare=="S":
        time.sleep(0.5)
        ricerca()
    if continuare=="N" or continuare=="n":
        time.sleep(0.5)
        main()
    
########################### AGGIUNTA IN DB DA FILE ##########################à
def estrapolaUsers(file):
    
    
    with open(file, "r") as f:
            lines = []
            for line in f:
                lines.append(line.strip())
    lista_di_nomi = []

    for line in lines:
        if line!="":
                if line not in lista_di_nomi:
                    lista_di_nomi.append(line)

    users=[]

    lista_di_nomi.pop(0)
    for user in lista_di_nomi:
        dict={}
        ls=user.split()
        dict["nome"]=ls[0]
        dict["cognome"]=ls[1]
        dict["età"]=int(ls[2])
        dict["Comune Residenza"]=ls[3]
        dict["Data Di Nascita"]=ls[4]
        users.append(dict)

    return users

def aggiornamento():
    print("\n")
    

    print("\n                                 PUOI MODIFICARE SOLO INSERENDO L'ID DELL'UTENTE, LE MODIFICHE POSSONO ESSERE FATTE PER: NOME,COGNOME, ETA, COMUNE DI RESIDENZA ")
    time.sleep(0.5)

    id_modificare=input("\n INSERIRE L'ID DELL'UTENTE DA MODIFICARE -> ").lower()
    time.sleep(0.5)
    print("\n UTENTE DA MODIFICARE CON ID: ",id_modificare)
    time.sleep(0.5)
    modifica=input("\n INSERIRE LA MODIFICA DA EFFETTUARE: NOME,COGNOME,ETA', COMUNE DI RESIDENZA(comune) -> ").lower()
    time.sleep(0.5)
    dato_modificato=input("\n INSERIRE ORA IL CAMBIAMENTO ATTENZIONE A MAIUSCOLE/MINOSCOLE (vecchio->Nuovo) -> ")
    time.sleep(0.5)
    query = {"_id": ObjectId(id_modificare)}

    if modifica=="nome":
        value = {"$set": {"nome":dato_modificato}}
    if modifica=="cognome":
        value = {"$set": {"cognome":dato_modificato}}
    if modifica=="comune":
        value = {"$set": {"comune":dato_modificato}}
    if modifica=="età" or modifica=="eta":
        value = {"$set": {"età":dato_modificato}}
    result = usersCollection.update_one(query, value)
    print("\n                                 MODIFICA AVVENUTA CON SUCCESSO")
    time.sleep(0.5)
    cont=input("\n CONTINUARE A MODIFICARE? S/N -> ").lower()
    if cont=="si":
        aggiornamento()
    if cont=="no":
        main()

###################### ELIMINAZIONE DATI#########################
def eliminazione():
    print("\n")
    

    print("\n                                 PUOI ELIMINARE PER: ID,NOME,COGNOME, ETA, COMUNE DI RESIDENZA,TOTALE ")

    time.sleep(0.5)
    ric=input(" DIGITA PER COSA VUOI ELIMINARE (id,nome,cognome,età,comune,TOTALE) -> ").lower()
    time.sleep(0.5)
    print("\n")
    
    print("\n VUOI ELIMINARE PER: "+ ric.upper())
    if ric=="id":
        time.sleep(0.5)
        print("\n L'ELIMINAZIONE PER ID PUO' ESSERE FATTA UN ID ALLA VOLTA")
        time.sleep(0.5)
        id_da_eliminare=input("\n INSERISCI L' ID DA ELIMINARE -> ")
        time.sleep(0.5)
        query = {"_id": ObjectId(id_da_eliminare)}
    if ric=="id":
         result=usersCollection.delete_one(query)
         time.sleep(0.5)
         print("\n")
         print("\n                                 LAVORO ULTIMATO!\n")
         time.sleep(0.5)
         continuare=input("\n VUOI ELIMINARE ALTRO? S/N -> ")
         if continuare=="s" or continuare=="S":
             time.sleep(0.5)
             eliminazione()
         if continuare=="N" or continuare=="n":
            time.sleep(1)
            main()
    if ric=="nome":
        time.sleep(0.5)
        print("\n\n ATTENZIONE L'ELIMINAZIONE PER NOME ELIMINA TUTTI GLI USER CON LO STESSO NOME")
        time.sleep(0.5)
        nome_da_eliminare=input("\n INSERISCI IL NOME DA ELIMINARE CON MAIUSCOLE E MINUSCOLE CORRETTE -> ")
        time.sleep(0.5)
        query={"nome":{"$regex": nome_da_eliminare}}

    if ric=="cognome":
        time.sleep(0.5)
        print("\n\n ATTENZIONE L'ELIMINAZIONE PER COGNOME ELIMINA TUTTI GLI USER CON LO STESSO COGNOME")
        time.sleep(0.5)
        cognome_da_eliminare=input("\n INSERISCI IL COGNOME DA ELIMINARE CON MAIUSCOLE E MINUSCOLE CORRETTE -> ")
        time.sleep(0.5)
        query={"cognome":{"$regex": cognome_da_eliminare}}

    if ric=="comune":
        time.sleep(0.5)
        print("\n\n ATTENZIONE L'ELIMINAZIONE PER COMUNE ELIMINA TUTTI GLI USER CON LO STESSO COMUNE")
        time.sleep(0.5)
        comune_da_eliminare=input("\n INSERISCI IL COMUNE DELL'USER DA ELIMINARE CON MAIUSCOLE E MINUSCOLE CORRETTE -> ")
        time.sleep(0.5)
        query={"comune":{"$regex": comune_da_eliminare}}

    if ric=="età" or ric=="eta":
        time.sleep(0.5)
        print("\n\n ATTENZIONE L'ELIMINAZIONE PER ETA' ELIMINA TUTTI GLI USER CON LA STESSA ETA'(MINORE O MAGGIORE DI UN NUMERO)")
        gtorlt=input("\n ELIMINARE PER ETA' MAGGIORE DI O MINORE DI (INSERIRE gt o lt) -> ")
        if gtorlt=="gt":
            time.sleep(0.5)
            eta_da_eliminare=input("\n INSERISCI L'ETA' DA ELIMINARE IN NUMERO -> ")
            time.sleep(0.5)
            query={"età":{"$gt":int(eta_da_eliminare)}}

        if gtorlt=="lt":
            time.sleep(0.5)
            eta_da_eliminare=input("\n INSERISCI L'ETA' DA ELIMINARE IN NUMERO -> ")
            time.sleep(0.5)
            query={"età":{"$lt":int(eta_da_eliminare)}}
    if ric=="TOTALE" or ric=="totale":
        time.sleep(0.5)
        print("\n ATTENZIONE L'ELIMINAZIONE TOTALE COMPORTA LA PERDITA DI TUTTI I DATI\n\n E' UN OPERAZIONE IRREVERSIBILE\n\n")
        procedere=input("PROCEDERE? S/N -> ").lower()
        if procedere=="n":
            eliminazione()
        if procedere=="s":
            query={}

    result=usersCollection.delete_many(query)
    time.sleep(0.5)
    print("\n")
    print("\n                                 LAVORO ULTIMATO!\n")
    time.sleep(0.5)
    continuare=input("\n VUOI ELIMINARE ALTRO? S/N -> ").lower()
    if continuare=="s" or continuare=="S":
        time.sleep(0.5)
        eliminazione()
    if continuare=="N" or continuare=="n":
        time.sleep(1)
        main()
############### FUNZIONE PRINCIPALE################################

def main():
    print("\n")
    print("\n")
    print("\n")
    print(Fore.YELLOW+"********************************************************************************************************************")
    print("********************************************************************************************************************")
    print("\n")
    print(Fore.GREEN+"\n SEI COLLEGATO AL DATABASE ALL'INDIRIZZO: ",cl," CON NOME: ",database," ALLA COLLECTION DI NOME: ",uC)
    print("\n")
    decision=input(Fore.WHITE+"\n                                 LE OPERAZIONI DISPONIBILI SONO: \n\n-AGGIUNTA \n\n-RICERCA \n\n-AGGIORNAMENTO \n\n-ELIMINAZIONE \n\n-USCITA (esc) \n\n COSA VUOI FARE -> ").lower()

    
    if decision=="aggiunta":
        time.sleep(0.5)
        print("\n\n PER AGGIUNGERE NUOVI DATI DEVI AGGIUNGERLI NEL FILE 'user.txt'                         \n ATTENZIONE VERIFICARE CHE NON VI SIANO DATI PRECEDENTI SENNO' SARANNO REINSERITI")
        time.sleep(0.5)
        avanti=input("\n SE HAI INSERITO TUTTI I DATI IN 'user.txt' DIGITA 'si' DIGITANDO 'no' IL PROGRAMMA SI INTERROMPERA' E POTRAI INSERIRLI -> ").lower()
        if avanti=="si":
            users = estrapolaUsers("user.txt")
            result= usersCollection.insert_many(users)
            time.sleep(0.5)
            print("\n                                NUOVI DATI AGGIUNTI CON SUCCESSO ")
            time.sleep(1.2)
            print("\n                                RITORNO AL MENU' PRINCIPALE ")
            time.sleep(1)
        
        main()
    if decision=="eliminazione":
        eliminazione()
         
    if decision=="ricerca":
        ricerca()
    if decision=="esc":
        time.sleep(1)
        print("\n")
        print("\n")
        print(Fore.RED+"\n                                 ARRIVEDERCI")
        print("\n")
        print(Fore.YELLOW+"********************************************************************************************************************")
        print("********************************************************************************************************************"+Fore.WHITE)
    if decision=="aggiornamento":
        aggiornamento()
main()