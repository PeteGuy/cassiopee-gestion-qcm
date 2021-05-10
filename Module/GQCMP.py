#!/usr/bin/env python
import sys
import Gestion
import DB
import Parser
import QCM


if(len(sys.argv) == 1):
    print("Error no command entered")
    sys.exit()

# La suite de if elif else est très peu élégante -> faire un match case, ou bien passer par un dictionnaire comme dans CL.py 



if sys.argv[1] == "import":
    if len(sys.argv) == 3:
        #import rapide 
        print("tesst")
        Gestion.init()
        Gestion.parse_file(sys.argv[2])
    
        Gestion.save_buffer()
        Gestion.persist_db()
        
    elif len(sys.argv) == 4:
        #import avec détails on fait une boucle while pour avoir les détails
        print("4")
        
    
    
    else:
        print("Error number of argument invalid")
        sys.exit()
         
         
elif sys.argv[1] == "export":
    Gestion.init()
    print("EXPORTING")
    entry = input("Select how to choose what you want to export : 'tag';'name';'id';    enter finsh to finalize export >>>")
    while(entry != "finish"):
        
        
        if(entry == "tag"):
            entryTag = input("Enter a tag or enter quit to go back to selection type >>>")
            while(entryTag != "quit"):
                if(entryTag != "quit" and entryTag != ""):
                    entryTag = entryTag.split()
                    Gestion.select_tags(entryTag)
                entryTag = input("Enter a tag or enter quit to go back to selection type >>>")
                
                
            
        elif(entry == "name"):
            entryName = input("Enter a name or enter quit to go back to selection type >>>")
            while(entryName != "quit"):
                if(entryName != "quit" and entryName != ""):
                    Gestion.select_name(entryName)
              
                entryName= input("Enter a name or enter quit to go back to selection type >>>")
                
            
        elif(entry == "id"):
            entryId = input("Enter an id or enter quit to go back to selection back >>>")
            while(entryId != "quit"):
                if(entryId != "quit" and entryId != ""):
                    Gestion.select_id(entryId)
                entryId = input("Enter an id or enter quit to go back to selection back >>>")
                

                

        entry = input("Select how to choose what you want to export : 'tag';'name';'id';    enter finsh to finalize export >>>")
            
    nomFichier=input("Entrez un nom de fichier :")
    while(nomFichier == ""):
        nomFichier=input("Entrez un nom de fichier :")
    Gestion.export_sel_latex(nomFichier+".tex")
    sys.exit()


elif sys.argv[1] == "show":
    Gestion.init()
    Gestion.select_all()
    for string in Gestion.get_all_short_sel_str():
        print(string)
    sys.exit()


elif sys.argv[1] == "search":
    Gestion.init()
    if len(sys.argv) == 2:
        entry = input("Select searching method ('tag', 'name' or 'id') or press enter to abort >>> ")
        while(entry not in ["tag", "name", "id", ""]):
            entry = input("Select searching method ('tag', 'name' or 'id') or press enter to abort >>> ")
        if(entry == ""):
            sys.exit()
        else:
            searchtype = entry


    if len(sys.argv) < 4:
        if len(sys.argv) == 3:
            searchtype = sys.argv[2]
        message = "Input the " + searchtype + "s of the questions you're searching for, or press enter to abort >>> "
        args = input(message).split()
        if(len(args) == 0):
            sys.exit()
    else:
        searchtype = sys.argv[2]
        args = sys.argv[3:]


    if (searchtype == 'tag'):
        for tag in args:
            Gestion.select_tags(tag)
    elif (searchtype == 'name'):
        for name in args:
            Gestion.select_name(name)
    elif (searchtype == 'id'):
        for id in args:
            Gestion.select_id(id)   
    else:
        print("Incorrect searching method selected : only 'tag', 'name' and 'id' are accepted")
        sys.exit()


    if Gestion.sel == []:
        print("No corresponding question found")
    else:
        for string in Gestion.get_all_short_sel_str():
            print(string)
    sys.exit()

   
else:
    sys.exit()

            
            