#!/usr/bin/python2

import argparse
import sys
import fileinput
import shlex

# Function definitions

# Function to read the input data
def read_funct():
    temp = []
    for Line in fileinput.input(args.inFile, ''):
        shlex.split(Line)
        Line = Line[:len(Line)-1]
        temp.append(Line)
    fileinput.close()
    return temp

# Function to add a line
def add_funct(AddLine):
    FField = ""                                 # Variables to store field parameters
    DField = ""
    PField = ""
    QField = ""
    AddLine = AddLine[6:len(AddLine)-3]         # Clip the ends of the 'add "{' & '}"'
    SplitLines = AddLine.rsplit(", ")           # Split the line into its fields
    
    for Subfields in SplitLines:
        if(Subfields[1:10] == "Footprint"):
            FField = Subfields.rsplit("'")[3]
        if(Subfields[1:12] == "Description"):
            DField = Subfields.rsplit("'")[3]
        if(Subfields[1:7] == "PartID"):
            PField = Subfields.rsplit("'")[3]
        if(Subfields[1:9] == "Quantity"):
            print Subfields
            QField = Subfields[12:len(Subfields)]
    # Concatonate the new string to be added & add
    NewLine = PField.rjust(6) + "  " + DField + " ".rjust(32-len(DField)) + FField + " ".rjust(12-len(FField)) + QField
    Data.append(NewLine)
    print "add command run with no errors"
 
# Function to remove a line with a certain PartID
def remove_funct(RemoveField, Data):
    RemoveField = RemoveField[7:]                       # Clip the leading 'remove'
    RemoveFieldF = RemoveField.rsplit("=")[0]           # Extract the field portion
    RemoveFieldV = RemoveField.rsplit("=")[1]           # Extract the value portion
    RemoveFieldV = RemoveFieldV[:len(RemoveFieldV)-1]   # Remove the newline
    indexList = []                                      # List of indices with lines to remove
    i = 0                                               # index to add to the above list
    
    for Line in Data[1:]:                               # Skip the header line
        if(RemoveFieldF == "PartID"):
            if(cmp(Line[0:6].lstrip(), RemoveFieldV) == 0): 
                indexList.append(i)
        elif(RemoveFieldF == "Description"):
            if(cmp(Line[8:39].rstrip(), RemoveFieldV) == 0): 
                indexList.append(i)
        elif(RemoveFieldF == "Footprint"):
            if(cmp(Line[40:51].rstrip(), RemoveFieldV) == 0): 
                indexList.append(i)
        elif(RemoveFieldF == "Quantity"):
            if(cmp(Line[52:60].rstrip(), RemoveFieldV) == 0): 
                indexList.append(i)
        else:
            apple = 1   # Throw an apple
        i = i + 1
    for j in reversed(indexList):       # Remove indices in reverse order
        Data.pop(j+1)                   # Include the +1 for the header line
    print "remove command run with no errors"

# Function to list entries in inventory
def list_funct(ListLine, Data):
    ListLine = ListLine[:len(ListLine)-1]           # Remove the newline
    ListLine = ListLine.rsplit(' ')
    if(len(ListLine) == 2):
        for Line in Data:
            print Line
    else:
        if(ListLine[2] == "with"):
            WithField = ListLine[3]
            print "listng with field",WithField
            WithF = WithField.rsplit('=')[0]
            WithV = WithField.rsplit('=')[1]
            print Data[0]                           # Print header
            for Line in Data[1:]:
                if( (WithF != "PartID") and (WithF != "Description") and (WithF != "Footprint") and (WithF != "Quantity") ):
                    print "Error: Field not found"
                if( (WithF == "PartID") and (cmp(WithV, Line[0:6].lstrip()) == 0) ):
                    print Line
                elif( (WithF == "Description") and (cmp(WithV, Line[8:39].rstrip()) == 0) ):
                    print Line
                elif( (WithF == "Footprint") and (cmp(WithV, Line[40:51].rstrip()) == 0) ):
                    print Line
                elif( (WithF == "Quantity") and (cmp(WithV, Line[52:60].rstrip()) == 0) ):
                    print Line
        elif(ListLine[2] == "sort"):
            print Data[0]                           # Print header
            SortBy = ListLine[3]
            SortedData = []
            for Line in Data:
                if(SortBy == "Description"):
                    Line = Line[8:39] + Line
                if(SortBy == "Footprint"):
                    Line = Line[40:51] + Line
                if(SortBy == "Quantity"):
                    Line = Line[52:].rstrip() + Line
                SortedData.append(Line)
            SortedData = SortedData[1:]
            SortedData.sort()
            for Line in SortedData:
                if(SortBy == "PartID"):
                    print Line
                if(SortBy == "Description"):
                    print Line[31:]
                if(SortBy == "Footprint"):
                    print Line[11:]
                if(SortBy == "Quantity"):
                    print Line[len(Line[52:].lstrip().rstrip()):]
            print
        else:
            a = 1       # throw

# Main program start
parser = argparse.ArgumentParser(description='Inventory management.')
parser.add_argument('-f', '--data-file', dest="inFile", help="Path to the data file to be read on startup")
args = parser.parse_args()

#try:
Data = read_funct()         # Call data reading

for Line in fileinput.input("actions", ''):
    if(Line[0:3] == "add"):
        add_funct(Line)
    elif(Line[0:6] == "remove"):
        remove_funct(Line, Data)
    elif(Line[0:4] == "list"):
        list_funct(Line, Data)

# Write the updated file to output
fout = open(args.inFile, 'w')
for Line in Data:
    fout.write(Line+'\n')
fout.close()

sys.exit(0)

