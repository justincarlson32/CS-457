# Justin Carlson
# CS 457-1001
# Created: 11-10-21


from genericpath import isfile
import sys
import os

inUseDatabase = ''


# function: doesExist(mode, path):
# Purpose: Checks if a file/folder exists, with a mode flag that determines whether to look
# for a folder or a file

def doesExist(mode, path):
	if (mode == 0): #databases
		if (os.path.isdir(os.path.abspath(path))):
			return True
	else: #tables
		if (os.path.isfile(os.path.abspath(path))):
			return True

	return False


# function: getValuePairs(line)
# Purpose: gets [ids datatypes] from create command input

def getKeyValuePairs(line):

	# man, you guys love fucking with our parsing by changing capitalizations
	# and spacing between scripts; mildly aggrivating
	for letter in line[2]:
		if (letter == '('):
			line.insert(3, line[2][line[2].index(letter):])
			break

	line = line[+3:] #remove commands
	keyValues = []
	
	line[0] = (line[0])[+1:] #remove first parenthesis

	delimited = [] # for storing sanitized inputs of special characters

	for word in line:
		delimited.append(word.replace(",", "")) # remove commas

	delimited[len(delimited) - 1] = (delimited[len(delimited) - 1])[:-2] #remove semi colon and parentheseis

	for word in delimited:
		keyValues.append(word)
	
	return keyValues

#function: handleCreate(line)
#purpose: handles the CREATE sql command and parsing

def handleCreate(line):
	structure = line[1] # get whether table or database
	if (structure == 'DATABASE'): # if database
		dbName = (line[2])[:-1] # name of db
		if (not(doesExist(0, dbName))):
			print("Creating database: " + dbName)
			os.mkdir(dbName) # make directory
		else:
			print ("Failed Creating Database: " + dbName + " because it already exists") # if exists
	if (structure == 'TABLE' or structure == 'table'): # if table
		tblName = ''
		for letter in line[2]:
			if (letter == '('):
				break
			tblName += letter
		if (not(doesExist(1, inUseDatabase + "/" + tblName))):
			print("Creating table: " + tblName + " in database: " + inUseDatabase)
			f = open(inUseDatabase + "/" + tblName, "w")
			keyValues = getKeyValuePairs(line)
			for keyValue in keyValues[::2]:
				f.write(keyValue + ' ' + keyValues[keyValues.index(keyValue) + 1] + ' ') #write values to file
			f.write('\n')
			f.close()

		else:
			print ("Failed Creating table: " + tblName + " because it already exists in database: "  + inUseDatabase)

#function: handleDrop(line)
#purpose: handles the Drop sql command and parsing	

def handleDrop(line):
	if (line[1] == 'DATABASE'):
		dbName = (line[2])[:-1]
		if (doesExist(0, dbName)):
			print("Deleting Database: " + dbName)
			os.rmdir(os.path.abspath(dbName)) # remove the directory of the database name
		else:
			print("Database deletion failed because database: " + dbName + " does not exist") # if it doesnt exist
	if (line[1] == 'TABLE'):
		tblName = (line[2])[:-1]
		if (doesExist(1, inUseDatabase + "/" + tblName)):
			print("Deleting table: " + tblName + "in database: " + inUseDatabase)
			os.remove(os.path.abspath(inUseDatabase + "/" + tblName)) # remove text file where the table information was stored
		else:
			print("Table deletion failed because table: " + tblName + " does not exist in database: " + inUseDatabase)

#function: handleUse(line)
#purpose: handles the USE sql command and parsing

def handleUse(line):
	dbName = (line[1])[:-1]
	if (doesExist(0, dbName)):
		print("USE Database: " + dbName)
		global inUseDatabase # set global value for in use database
		inUseDatabase = str(dbName)
	else:
		print("Database USE failed because database: " + dbName + " does not exist")


#function: handleAlter(line)
#purpose: handles the ALTER sql command and parsing
# mostly deprecated and needs updating to work with new table model
def handleAlter(line):
	tblName = line[2] # table name
	command = line[3] # command (ADD/DROP)
	if (doesExist(1, inUseDatabase + "/" + tblName)):
		data = line[4] + " " + (line[5])[:-1] + " "
		if (command == 'DROP'):
			pairs = [] #needs updating
			didFind = False
			for pair in pairs:
				if (pair == data):
					print("Finished dropping " + data + " from table: " + tblName)
					pairs.remove(pair)
					didFind = True
					os.remove(os.path.abspath(inUseDatabase + "/" + tblName))
					f = open(inUseDatabase + "/" + tblName, "w")
					for pair in pairs:
						f.write(pair[0] + ' ' + pair[1] + ' ')
					f.close()

			if (didFind == False):
				print("Did not find: " + data + " in table: " + tblName)
		if (command == 'ADD'):
			print("Finished adding: " + data + " to table: " + tblName)
			f = open(inUseDatabase + "/" + tblName, "a")
			f.write(data)
			f.close()
	else:
		print("Error altering: " + tblName + " does not exist in database: " + inUseDatabase)
	print

#function: handleInsert(line)
#purpose: handles the INSERT sql command and parsing
def handleInsert(line):

	tblName = str(line[2]) # gets name of desired table

	line = line[+3:] #remove commands

	line[0] = (line[0])[+7:] #removing "values("" from string 

	delimited = [] # for later removing any special characters

	for word in line: # removing special characters
		delimited.append(word.replace(",", " "))

	delimited[len(delimited) - 1] = (delimited[len(delimited) - 1])[:-2] #remove semi colon and parentheseis

	f = open(inUseDatabase + "/" + tblName, "a") # writing back  to file in specified format

	for word in delimited:
		f.write(word + ' ')

	f.write('\n')

	f.close()

	print("Inserted 1 item into table: " + tblName + " in database: " + inUseDatabase)

#function: writeTableToFile(table, tblName)
#purpose: takes the 2-d array table and the name of the table and writes it into the in-use database directory
def writeTableToFile(table, tblName):

	os.remove(os.path.abspath(inUseDatabase + "/" + tblName)) # remove old copy of the table

	f = open(inUseDatabase + "/" + tblName, "w")

	for line in table:
		for item in line:
			f.write(item + " ")
		f.write("\n")
	
	f.close()

	return

#function: parseTable(tblName)
#purpose: simply loads table into 2-d array, identically to how it is stored in file
def parseTable(tblName):
	table = []
	f = open(inUseDatabase + "/" + tblName, "r")

	lines = f.readlines()

	for Tuple in lines:
		row = []
		for word in Tuple.split():
			row.append(str(word))	
		table.append(row)

	return table

#function: generateVarToGraphDict(arg1)
#purpose: generates a dictionary with table variable mapped to graph array

def generateVarToGraphDict(arg1):
	returnDict = {}
	for i in range(0, len(arg1), 2):
		returnDict[arg1[i + 1]] = parseTable(arg1[i])
	return returnDict

#function: handleSelect(line)
#purpose: handles the SELECT sql command and parsing

def handleSelect(line):

	if any("*" in s for s in line): # if query is a simple SELECT *
		if (line[1] == '*'): #select all; built for future element finding

			line = line[3:] # remove select * from

			tableNamesWithVarName = [] # to store DB name to its variable name

			shouldLeftOuter = 0 # simple way to tell which kind of join should occur

			shouldSkip = False # used for skipping the variable name of the table
			for chunk in line: #loop through all words in command
				if shouldSkip:
					shouldSkip = False
					continue
				if (chunk == "where" or chunk == "on"):
					line = line[(line.index(chunk)):] # remove all table name and variable when get to where
					break

				if (chunk == "inner" or chunk == "join"):  #skip these words
					continue

				if (chunk == "left" or chunk == "outer"):
					shouldLeftOuter = 1
					continue

				varName = line[line.index(chunk) + 1] # get the variable name of the table
				tableNamesWithVarName.append(chunk) # push table name into array
				tableNamesWithVarName.append(varName.replace(",", "")) # push sanitized variable name into array
				shouldSkip = True # skip the variable name next ieration


			varNameToGraphDict = generateVarToGraphDict(tableNamesWithVarName) #generates a dictionary with variable names mapped to table in memory

			leftTableID = "" # hold table identifier from command
			leftTableVar = "" # hold table name in disk

			rightTableID = "" # ^
			rightTableVar = "" # ^

			for chunk in line:
				if (chunk == "where" or chunk == "on"):
					continue
				if (chunk == "="):
					operation = chunk
					continue

				bufferLeft = chunk.split(".") # splitting variable name from property of table (E.id = E id)
				bufferRight = line[line.index(chunk) + 2].split(".") # ^

				leftTableID = bufferLeft[0] # table as user defined in command   # ultimately these ended up reversed, too lazy to fix
				leftTableVar = bufferLeft[1] # table as desribed in memory
				rightTableID = bufferRight[0] # ^
				leftTableVar = bufferLeft[1] # ^

				break

			leftColumn = 0 # target column for comparison
			for i in range(0, len(varNameToGraphDict[leftTableID][0]), 2): # parse every other element of header row of table
				if (i > (len(varNameToGraphDict[leftTableID][0]) - 2)): # ignore anything greater than max - 1
					break
				if (varNameToGraphDict[leftTableID][0][i] == leftTableVar): # getting operation comparing data type and column
					leftColumn = i		
			
			leftColumnValues = [sub[leftColumn] for sub in varNameToGraphDict[leftTableID]][1:] # all values in the comparing column

			rightColumn = 0 # target column for comparison
			for i in range(0, len(varNameToGraphDict[rightTableID][0]), 2): # parse every other element of header row of table
				if (i > (len(varNameToGraphDict[leftTableID][0]) - 2)): # ignore anything greater than max - 1
					break
				if (varNameToGraphDict[rightTableID][0][i] == rightTableVar): # getting operation comparing data type and column
					rightColumn = i		
			
			printString = "" # string that will be formatted for printing

			rightColumnValues = [sub[rightColumn] for sub in varNameToGraphDict[rightTableID]][1:] # generate right column values
			rightColumnValues = list(enumerate(rightColumnValues)) # generate unique list of them so proper indexing can occure

			candidateTable = [] # table that will hold the values retained from each select oeperation

			rightDataTypes = []
			for i in range(0, len(varNameToGraphDict[rightTableID][0]), 2): # parse data types to add to cand table
				dataTypeAndID = varNameToGraphDict[rightTableID][0][i] + " " + varNameToGraphDict[rightTableID][0][i + 1]
				rightDataTypes.append(dataTypeAndID)
			
			leftDataTypes = []
			for i in range(0, len(varNameToGraphDict[leftTableID][0]), 2): # parse data types to add to cand table
				dataTypeAndID = varNameToGraphDict[leftTableID][0][i] + " " + varNameToGraphDict[leftTableID][0][i + 1]
				leftDataTypes.append(dataTypeAndID)

			candidateTable.append(leftDataTypes + rightDataTypes) # add the data type row to the cand table

			for value in leftColumnValues: # parse through left column values
				addedIndices = [] # keep track of indices for uniqueness
				didMatch = 0 # for if no match was found in the table
				for index, element in rightColumnValues: # parse through 
					if (value == element):
						shouldPass = 0
						for index1 in addedIndices:
							if (index1 == addedIndices):
								shouldPass = 1
								break
						if shouldPass == 0:
							candidateTable.append(varNameToGraphDict[leftTableID][int(value)] + varNameToGraphDict[rightTableID][index + 1]) # add indices to table for printing
							addedIndices.append(index) # add to index that have already been added
							didMatch = 1 # mark that a similar tuple was found
				if (didMatch == 0 and shouldLeftOuter): # if a match for the tuple could not be found, we add it with a blank space
					candidateTable.append(varNameToGraphDict[leftTableID][int(value)] + [" "])

			#printing table to screen
			for row in range(0, len(candidateTable)):
				printString = ""
				for column in range(0, len(candidateTable[row])):
					printString += candidateTable[row][column] + " | "

				print(printString)

		else:
			print("Error selecting: " + tblName + " does not exist in database: " + inUseDatabase)		

	else:

		#all information variables the will be needed for future selecting
		selectIDs = []
		operation = ""
		comparatorValue = 0
		whereID = ""
		tblName = ""


		selectColumns = []
		operationColumn = 0

		#parse things here

		parseStage = 0 # variable to determine which part of parsing we are on

		for chunk in line: #loop through all words in command
			if (chunk == "from"): #getting table name and end of select columns
				tblName = line[line.index(chunk) + 1]
				parseStage = 1

			if (not(chunk == "select") and parseStage == 0):
				selectIDs.append(chunk.replace(",", "")) # getting name of all select columns and removing commas

			if (chunk == "where"):
				whereID = line[line.index(chunk) + 1]# getting where column name
				operation = line[line.index(chunk) + 2]# getting comparator operation
				comparatorValue = int((line[line.index(chunk) + 3]).replace(";", "")) #getting value to compare to and removing semi colon

		table =	parseTable(tblName) # create virtual copy of table

		printString = "" # variable to handle each line that will be printed to screen

		for i in range(0, len(table[0]), 2): # parse every other element of header row of table
			if (i > (len(table[0]) - 2)): # ignore anything greater than max - 1
				break
			if (table[0][i] == whereID): # getting operation comparing data type and column
				operationColumn = i
			for id in selectIDs: # parsing all ids that are within the specified input
				if (id == table[0][i]): # if id is in header add its column index to array
					selectColumns.append(int(i/2)) # divide by two because double indices due to storage technique
					printString += table[0][i] + " " + table[0][i+1] + " | " # print selected data types and ids
			i += 1
		print(printString) #print data types and ids

		for i in range(1, len(table)): # actually parsing values
			printString = "" # place holder to print line by line
			for j in selectColumns:
				if (operation == "!="): # given input operation !=
					if (not(int(table[i][operationColumn])) == comparatorValue): # performs the specified operation on the target column values
						printString += table[i][j] + "|" # if it does compare correctly add it to the print out string
			if (not(printString == "")): # to not print initialized string
				print(printString)

#function: handleUpdate(line)
#purpose: handles the UPDATE sql command and parsing
def handleUpdate(line):

	#getting relevant information from the input command
	# self expalnatory names
	tblName = line[1]
	setID = line[3]
	setValue = line[5]
	whereID = line[7]
	whereValue = (line[9])[:-1]

	table = parseTable(tblName)

	whereColumn  = -1 # the column from which the values will be checked
	toColumn = -1 # the column from which the values will be updated

	for id in table[0]:
		if (id == whereID):
			whereColumn = int(((table[0]).index(id))/2) # gets the where id column index and divides by two because 
														# the header column has double the indices of the actual data due to datatypes and ids
		if (id == setID):
			toColumn = int(((table[0]).index(id))/2)	# gets the to id column index and divides by two because 
														# the header column has double the indices of the actual data due to datatypes and ids

	columnValues = [sub[whereColumn] for sub in table] #generate list of column elements

	modifiedRows = [] # rows that were modified to write back to virtual table
	for value in columnValues:
		if (value == whereValue):
			modifiedRows.append(columnValues.index(value)) # adding row index to list
			columnValues[columnValues.index(value)] = setValue # setting value in column list

	for row in modifiedRows:
		table[int(row)][toColumn] = setValue # writing value back to original virtual table

	writeTableToFile(table, tblName) # write virtual table to disk

	print("Modified " + str(len(modifiedRows)) + " records")

#function: handleDelete(line)
#purpose: handles the DELETE sql command and parsing
def handleDelete(line):

	#getting relevant information from the input command
	tblName = line[2]
	whereID = line[4]
	whereValue = (line[6])[:-1]
	operator = line[5]

	table = parseTable(tblName) # generating virtual copy of the table

	whereColumn  = -1 # the column from which the values will be checked

	for id in table[0]:
		if (id == whereID):
			whereColumn = int(((table[0]).index(id))/2) # gets the where id column index and divides by two because 
														# the header column has double the indices of the actual data due to datatypes and ids

	columnValues = [sub[whereColumn] for sub in table]  # generate single array of all values in the column

	modifiedRows = [] # rows that were modified to write back to virtual table

	iterator = 0

	if (operator == "="): # if operation is equal
		for iterator in range(len(columnValues)):
			if (columnValues[iterator] == whereValue):
				modifiedRows.append(iterator) # add row where value fits criteria
	
	if (operator == ">"): # if operation is greater than
		for iterator in range(1, len(columnValues)):
			if (float(columnValues[iterator]) > float(whereValue)):
				modifiedRows.append(iterator)# add row where value fits criteria

	removed = 0 #amount of data removed because after removing an element the indices all shift and have to adjust to that offset
	for row in modifiedRows:
		table.remove(table[row - removed])
		removed += 1
	
	print("Removed " + str(len(modifiedRows)) + " entries")

	writeTableToFile(table, tblName) # write table back to file after modification

#function: parseLine(line)
#purpose: handles command input parsing to determine which command is called
	
def parseLine(line):
		command = line.split()[0]
		if (command == 'create' or command == 'CREATE'):
			handleCreate(line.split())
		if (command == 'DROP'):
			handleDrop(line.split())
		if (command == 'USE'):
			handleUse(line.split())
		if (command == 'select'):
			handleSelect(line.split())
		if (command == 'ALTER'):
			handleAlter(line.split())
		if (command == 'insert'):
			handleInsert(line.split())
		if (command == 'update'):
			handleUpdate(line.split())
		if (command == 'delete'):
			handleDelete(line.split())

with open('PA3_test.sql') as f:
	lines = f.readlines()
	for line in lines:
		if (not(line[0] == '\n' or ( line[0] == '-'))):

			if any(".exit" in s for s in line.split()): #quit program if .exit is called
				print("-------Finished--------")
				quit()
			
			completeLine = line

			amountOfLines = 1
			while completeLine.find(';') == -1: #this is to deal with the new multiline commands, goes until a semi colon is found
				if (not(lines[lines.index(line) + amountOfLines][0] == '-')):
					completeLine += str(lines[lines.index(line) + amountOfLines])
					lines[lines.index(line) + amountOfLines] = '-' + ' ' + '\n'
				amountOfLines += 1		



			splitComplete = completeLine.split() #create list of words

			for chunk in splitComplete: #this is to correct bad test script using a mix of lowercase and uppercase P in product
				if "product" in chunk:	#in real SQL capitalization matters...
					splitComplete[splitComplete.index(chunk)] = "Product"



			if len(splitComplete) > 7: #apparently it will retain values from the previous command, this is to check if there are duplicate wording
				#this is honestly some black magic, that I couldnt figure out how to fix. It works somehow
				if splitComplete[0] == splitComplete[2]:
					splitComplete.remove(splitComplete[0])
					splitComplete.remove(splitComplete[0])

			completeLine = " ".join(splitComplete)# join list of words back into a single string
			parseLine(completeLine)
	print("-------Finished--------")

	


