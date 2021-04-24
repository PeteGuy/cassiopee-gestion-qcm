#!/usr/bin/env python
import sys
import Gestion

Gestion.init()
Gestion.parse_file(sys.argv[1])

for string in Gestion.get_all_short_buffer_str():
	print(string)

line = input("Input names of questions to save, or press enter to select all >> ")
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