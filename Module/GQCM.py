#!/usr/bin/env python
import sys
import Gestion
import DB
import Parser
import QCM

#TODO LIST

#uniformiser les messages adressés à l'utilisateur
#-> texte français ou anglais ?
#-> commande "entrer" ou 'quit' pour quitter ?

#commande "tag" : trouver une implémentation ergonomique, plus rapide que d'utiliser "search" puis l'option 'tag'

#commande "import":
#-> proposer à l'utilisateur de taguer les questions immédiatement après l'import ?
#-> nettoyer le code : je pense qu'il ya beaucoup de code en double

#implémenter commande "untag" : enlève les tags "tag1 tag1 tag3" d'une selection de questions si elles ont ces tags
#-> nouvelle commande, ou bien seulement une option à la fin de search ?

#implémenter commande "rename" : change le nom d'une unique question (GQCM rename ancienNom nouveauNom)
#-> si plusieurs question avec même nom, les affiche et demande d'entrer l'id de la question à changer



if(len(sys.argv) == 1):
    print("Error no command entered")
    print("Voici la liste des commmandes disponibles :")
    print("    -import")
    print("    -export")
    print("    -show (affiche toutes les questions contenues dans la base de donnée)")
    print("    -tag")
    print("    -search")
    sys.exit()

# La suite de if elif else est très peu élégante -> faire un match case, ou bien passer par un dictionnaire comme dans CL.py ?



if sys.argv[1] == "import":#import commande
    Gestion.init()
    if len(sys.argv) == 3: #import rapide, tous les arguments sur la même ligne
        
        try: 
            Gestion.parse_file(sys.argv[2])
        

            for string in Gestion.get_all_short_buffer_str():
            	print(string)
            
            line = input("Input names of questions to save, or press enter to select all >>> ")
            args = line.split()
            #print(len(args))
            
            
            if len(args) == 0 :
            	Gestion.save_buffer()
            	print("buffer saved")
            else :
            	for name in args:
            		Gestion.select_buffer_name(name)
            	Gestion.save_sel_buffer()
            
            
            Gestion.persist_db()
            print("Base de donnée sauvegardée")
            sys.exit()
            
        except FileNotFoundError:
            print("Error file " + sys.argv[2] + " not found")
    
        Gestion.save_buffer()
        Gestion.persist_db()
        sys.exit()
        
    elif(len(sys.argv) == 2):#import détaillé
        entry = input("Enter the path of the file to import (relative path from the Module folder or absolute path)>>> ").strip()
        while(entry == ""):
            entry = input("Enter the path of the file to import (relative path from the Module folder or absolute path)>>> ").strip()
        try:
            Gestion.parse_file(entry)
            for string in Gestion.get_all_short_buffer_str():
            	print(string)
            
            line = input("Input names of questions to save, or press enter to select all >>> ")
            args = line.split()
            #print(len(args))
            
            
            if len(args) == 0 :
            	Gestion.save_buffer()
            	print("buffer saved")
            else :
            	for name in args:
            		Gestion.select_buffer_name(name)
            	Gestion.save_sel_buffer()
            
            
            Gestion.persist_db()
            print("Base de donnée sauvegardée")
            sys.exit()
            
       
        except FileNotFoundError:
            print("Error file " + sys.argv[2] + " not found")
                
    elif len(sys.argv) >= 4:
        #implémenter l'importation de plusieurs fichiers à la fois ?
        print("Error number of argument invalid")
        sys.exit()
        
    
    

        
         
elif sys.argv[1] == "export":
    Gestion.init()
    print("EXPORTING")
    #On demande un critère d'import puis on entre la commande correspondante
    entry = input("Select how to choose what you want to export : 'tag';'name';'id';    enter finish to finalize export >>> ")
    while(entry != "finish"):
        
        
        if(entry == "tag"):
            entryTag = input("Enter a tag or enter quit to go back to selection type >>> ")
            while(entryTag != "quit"):
                if(entryTag != "quit" and entryTag != ""):
                    entryTag = entryTag.split()
                    Gestion.select_tags(entryTag)
                entryTag = input("Enter a tag or enter quit to go back to selection type >>> ")
                
                
            
        elif(entry == "name"):
            entryName = input("Enter a name or enter quit to go back to selection type >>> ")
            while(entryName != "quit"):
                if(entryName != "quit" and entryName != ""):
                    Gestion.select_name(entryName)
              
                entryName= input("Enter a name or enter quit to go back to selection type >>> ")
                
            
        elif(entry == "id"):
            entryId = input("Enter an id or enter quit to go back to selection back >>>")
            while(entryId != "quit"):
                if(entryId != "quit" and entryId != ""):
                    Gestion.select_id(entryId)
                entryId = input("Enter an id or enter quit to go back to selection back >>>")
             
        print("\nQuestions currently selected for export :\n")
        for string in Gestion.get_all_short_sel_str():
            print(string)

                

        entry = input("Select how to choose what you want to export : 'tag';'name';'id' :\n Or enter finish to finalize export >>>")
    #export
    nomFichier = input("Entrez un nom de fichier :").strip()
    while(nomFichier == ""):
        nomFichier = input("Entrez un nom de fichier :").strip()
    Gestion.export_sel_latex("../Exports/"+nomFichier + ".tex")
    print("Fichier " + nomFichier + ".tex exporté dans le dossier Exports")
    sys.exit()


elif sys.argv[1] == "show":#On montre toutes les questions contenues dans la base de données
    Gestion.init()
    Gestion.select_all()
    for string in Gestion.get_all_short_sel_str():
        print(string)
    sys.exit()

elif sys.argv[1] == "tag":
    Gestion.init()
    
    #On demande un critère de sélection 
    entry = input("Select how to choose what you want to tag : 'tag';'name';'id';    enter finish to finalize tag >>> ")
    while(entry != "finish"):
        
        
        if(entry == "tag"):
            entryTag = input("Enter a tag or enter quit to go back to selection type >>> ")
            while(entryTag != "quit"):
                if(entryTag != "quit" and entryTag != ""):
                    entryTag = entryTag.split()
                    Gestion.select_tags(entryTag)
                entryTag = input("Enter a tag or enter quit to go back to selection type >>> ")
                
                
            
        elif(entry == "name"):
            entryName = input("Enter a name or enter quit to go back to selection type >>> ")
            while(entryName != "quit"):
                if(entryName != "quit" and entryName != ""):
                    Gestion.select_name(entryName)
              
                entryName= input("Enter a name or enter quit to go back to selection type >>> ")
                
            
        elif(entry == "id"):
            entryId = input("Enter an id or enter quit to go back to selection back >>>")
            while(entryId != "quit"):
                if(entryId != "quit" and entryId != ""):
                    Gestion.select_id(entryId)
                entryId = input("Enter an id or enter quit to go back to selection back >>>")
             
        print("\nQuestions currently selected to tag :\n")
        for string in Gestion.get_all_short_sel_str():
            print(string)

                

        entry = input("Select how to choose what you want to tag : 'tag';'name';'id' :\n Or enter finish to finalize tag >>>")
    
    #Tagging        
    nomTag = input("Entrez un tag :").strip()
    while(nomTag == ""):
        nomTag = input("Entrez un tag:").strip()
    Gestion.apply_tag_all(nomTag)
    print("Tag "+nomTag+" appliqué aux question sélectionnées.")
    Gestion.persist_db()
    print("Base de donnée sauvegardée")
    sys.exit()


elif sys.argv[1] == "search":#Commande search pour chercher une certaine question
    Gestion.init()
    if len(sys.argv) == 2:#recherche détaillée
        searchtype = input("Select searching method ('tag', 'name' or 'id') or press enter to abort >>> ").strip()
        while(searchtype not in ["tag", "name", "id", ""]):
            searchtype = input("Select searching method ('tag', 'name' or 'id') or press enter to abort >>> ").strip()
        if(searchtype == ""):
            sys.exit()


    if len(sys.argv) < 4:#recherche rapide
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
        sys.exit()
    for string in Gestion.get_all_short_sel_str():
        print(string)

    entry = input("Select what to do with the selection ('tag', 'export') or press enter to quit >>> ").strip()

    if (entry == ""):
        sys.exit()
    elif (entry == 'tag'):
        tags = input("Input the tags to apply to the selection >>> ").split()
        for tag in tags:
            Gestion.apply_tag_all(tag)
            Gestion.persist_db()
    elif (entry == 'export'):
        nomFichier = input("Input a file name : ").strip()
        while(nomFichier == ""):
            nomFichier = input("Input a valid file name : ").strip()
        Gestion.export_sel_latex(nomFichier + ".tex")
    


    sys.exit()

   
else:
    sys.exit()

            
            