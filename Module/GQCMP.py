#!/usr/bin/env python
import sys
import Gestion
import DB
import Parser
import QCM


if(len(sys.argv) == 1):
    print("Error no command entered")
    sys.exit()


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
    
else:
    sys.exit()

            
            