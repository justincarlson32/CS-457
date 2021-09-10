from genericpath import isfile
import sys
import os

inUseDatabase = ''

def doesExist(mode, path):
	if (mode == 0): #databases
		if (os.path.isdir(os.path.abspath(path))):
			return True
	else: #tables
		if (os.path.isfile(os.path.abspath(path))):
			return True

	return False

def getKeyValuePairsFromFile(tblName):
	pairs = []
	f = open(inUseDatabase + "/" + tblName, "r")
	lines = f.readlines()
	printString = ''
	for line in lines:
		pairs.append(line.rstrip())
	f.close()	
	return pairs	

def getKeyValuePairs(line):
	keyValues = []

	#hardcoded
	keyValues.append([(line[0])[+1:], (line[1])[:-1]])
	keyValues.append([(line[2]), (line[3])[:-2]])
	
	return keyValues

def handleCreate(line):
	structure = line[1]
	if (structure == 'DATABASE'):
		dbName = (line[2])[:-1]
		if (not(doesExist(0, dbName))):
			print("Creating database: " + dbName)
			os.mkdir(dbName)
		else:
			print ("Failed Creating Database: " + dbName + " because it already exists")
	if (structure == 'TABLE'):
		tblName = (line[2])
		if (not(doesExist(1, inUseDatabase + "/" + tblName))):
			print("Creating table: " + tblName + " in database: " + inUseDatabase)
			f = open(inUseDatabase + "/" + tblName, "w")
			for keyValue in getKeyValuePairs(line[+3:]):
				f.write(keyValue[0] + ' ' + keyValue[1] + '\n')
			f.close()
		else:
			print ("Failed Creating table: " + tblName + " because it already exists in database: "  + inUseDatabase)
			

def handleDrop(line):
	if (line[1] == 'DATABASE'):
		dbName = (line[2])[:-1]
		if (doesExist(0, dbName)):
			print("Deleting Database: " + dbName)
			os.rmdir(os.path.abspath(dbName))
		else:
			print("Database deletion failed because database: " + dbName + " does not exist")
	if (line[1] == 'TABLE'):
		tblName = (line[2])[:-1]
		if (doesExist(1, inUseDatabase + "/" + tblName)):
			print("Deleting table: " + tblName + "in database: " + inUseDatabase)
			os.remove(os.path.abspath(inUseDatabase + "/" + tblName))
		else:
			print("Table deletion failed because table: " + tblName + " does not exist in database: " + inUseDatabase)

def handleUse(line):
	dbName = (line[1])[:-1]
	if (doesExist(0, dbName)):
		print("USE Database: " + dbName)
		global inUseDatabase
		inUseDatabase = str(dbName)
	else:
		print("Database USE failed because database: " + dbName + " does not exist")

def handleSelect(line):
	tblName = (line[3])[:-1]
	if (doesExist(1, inUseDatabase + "/" + tblName)):
		if (line[1] == '*'): #select all; built for future element finding
			f = open(inUseDatabase + "/" + tblName, "r")
			lines = f.readlines()
			printString = ''
			for line in lines:
				if (lines.index(line) == (lines.__len__() - 1)):
					printString += line.rstrip()
				else:
					printString += line.rstrip() + " | "
			f.close()		
			print(printString)
	else:
		print("Error selecting: " + tblName + " does not exist in database: " + inUseDatabase)

#ALTER TABLE tbl_1 ADD a3 float;

def handleAlter(line):
	tblName = line[2]
	command = line[3]
	if (doesExist(1, inUseDatabase + "/" + tblName)):
		data = line[4] + " " +(line[5])[:-1]
		if (command == 'DROP'):
			pairs = getKeyValuePairsFromFile(tblName)
			didFind = False
			for pair in pairs:
				if (pair == data):
					print("Finished dropping " + data + " from table: " + tblName)
					pairs.remove(pair)
					didFind = True
					os.remove(os.path.abspath(inUseDatabase + "/" + tblName))
					f = open(inUseDatabase + "/" + tblName, "w")
					for pair in pairs:
						f.write(pair[0] + ' ' + pair[1] + '\n')
					f.close()

			if (didFind == False):
				print("Did not find: " + data + " in table: " + tblName)
		if (command == 'ADD'):
			print("Finished adding: " + data + "to table: " + tblName)
			f = open(inUseDatabase + "/" + tblName, "a")
			f.write(data + '\n')
			f.close()
	else:
		print("Error altering: " + tblName + " does not exist in database: " + inUseDatabase)
	print

def parseLine(line):
		command = line.split()[0]
		if (command == 'CREATE'):
			handleCreate(line.split())
		if (command == 'DROP'):
			handleDrop(line.split())
		if (command == 'USE'):
			handleUse(line.split())
		if (command == 'SELECT'):
			handleSelect(line.split())
		if (command == 'ALTER'):
			handleAlter(line.split())


with open('PA1_test.sql') as f:
	lines = f.readlines()
	for line in lines:
		if (not(line[0] == '\n' or ( line[0] == '-'))):
			if (line == '.EXIT'):
				break
			parseLine(line)
	print("-------Finished--------")

	


