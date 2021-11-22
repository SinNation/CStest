import os
import re
import time
import datetime
import pandas as pd
import pathlib
import re


#### Assumptions
# That your code is in order, checking of temp declarations is based on order of strings
# That no variable names contain symbols commonly used in code (e.g. <)
# Attributes with an _ are assumed to be used in arrays and therefore can't be found in the code consistently
# as python doesn't know what the suffix should be at any point. So it just searches for everything before the
# _ and considers a match on this basis to be a 'hit'




# Set a time stamp to generate the folder with, to keep each run of the tests unique within a project
timestamp = datetime.datetime.now()


##################################################################################################################
# Set all the path variables for the location of this code and the CS project
tests_path = os.getcwd() #Path of the folder containing CStest
cs_projects_path = os.path.dirname(os.getcwd()) #Parent path, should contain all CS project folders
##################################################################################################################


print("=================================================================\
     \nWelcome to CStest. A python based testing engine for Choicescript.\
     \nThe tool is easy to use. Ensure that the folder containing this\
     \nscript is stored alongside all of your CS project folders. You\
     \nthen simply need to input the name of the folder for the project\
     \nyou wish to test.\
     \n\
     \nThe tests will then begin and will generate file inputs that you\
     \ncan view. When you run the tests for a project, it will generate\
     \na folder within the CStest folder for that project. Then within\
     \nthat folder, it will generate a folder for each time you run the\
     \ntests - the name of this foler will be a date/time stamp, so that\
     \nthe test runs are kept in order.\
     \n=================================================================\
     \n")


##################################################################################################################
# Have user input the folder name of their project and check it is valid
correct_folder = False # Keeps looping whilst the folder name that is input is not valid
while correct_folder == False:
    project_folder = input("What is the name of the folder your CS project is stored in?\
                           \n=================================================================\
                           \n")
    project_path = cs_projects_path + '\\' + project_folder #Set the project path using by appending the folder name
    if os.path.isdir(project_path) == False:
        print ("******************************************************************************************\
               \nThe project folder name " + project_folder + " that you input was not found in the directory: " + cs_projects_path + \
               ".\nEither the folder name was incorrect, or the folder does not exist in this directory. \
                .\nPlease ensure that the folder containing CStest is stored in the same location as all of your CS project folders.\
                \n****************************************************************************************\
                \n\
                \n")
        
        retry = input("====================================================================\
                      \nWould you like to try re-entering the folder name? Enter 'N' to exit or enter anything else to retry.\
                      \n====================================================================\
                      \n\
                      \n")
        if retry.upper() == 'N':
            exit()
    if os.path.isdir(project_path) == True:
        correct_folder = True
        print ("Project folder: " + project_folder + " has been found. CStest will begin\
               \n")
        time.sleep(1)
##################################################################################################################



##################################################################################################################
# With the validated directory, generate a list of all .txt fields in the directory
list_of_files = []
for file in os.listdir(project_path):
    if file.endswith('.txt'):
       list_of_files.append(file)
number_of_files = len(list_of_files)
print (str(number_of_files) + ".txt files have been found in project folder: " + project_folder + "\n")
##################################################################################################################



##################################################################################################################
#Set up the test folder to store all the test outcomes
if not os.path.exists(tests_path+'\\'+project_folder):
    os.makedirs(tests_path+'\\'+project_folder)
os.makedirs(tests_path+'\\'+project_folder+'\\'+str(timestamp.strftime("%Y%m%d-%H%M%S")))
test_run_path = tests_path+'\\'+project_folder+'\\'+str(timestamp.strftime("%Y%m%d-%H%M%S"))
print ("Outcome of tests will be stored in: " + test_run_path + "\n")
##################################################################################################################



##################################################################################################################
# Parse all the files to ingest the complete code in the game. Remove line breaks and CS defined line and page breaks
# Then remove strings which are now wholly comprised of blank space. Then remove empty strings
                           
complete_code = {} # Dictionary to hold all the code in the game

for file in list_of_files:
    file_path = project_path + '\\' + file
    try:
        with open(file_path) as f:
            code = f.readlines()
    except:
        print ("******************************************************************************************\
               CStest encountered an error when trying to open file: " + file + " and read its contents.\
              \nPlease check the file is a valid CS txt file and if so, please report as a bug.\
              \nPlease provide this error message and the file that failed. \
              \nCStest will now exit as not reading in a .txt file could alter the outcome of the tests. \
               ******************************************************************************************\
              \n\
              \n")
        input("Press ENTER to exit")

    remove_breaks = [item.replace('\n', '').replace('*page_break', '').replace('*line_break', '') for item in code] #Remove CS commands which just add new lines and page breaks

    uppercase = [string.upper() for string in remove_breaks]
  
    for item in uppercase:
        if str.isspace(item):
            uppercase.remove(item) #Remove any strings which wholly consist of white space (but leaves white space within strings)
        else:
            pass
    
    remove_empty = list(filter(None, uppercase)) # Remove any completely empty strings
    
    complete_code[file] = remove_empty # Add the code for each file as a list of strings to the dictionary. The key is the file name
print ("Finished parsing " + str(number_of_files) + ".txt files in the directory. All code has been read into CStest\
       \n")
time.sleep(1)
##################################################################################################################



##################################################################################################################
# Parse the code to pull out all the cases where variables are defined and build a dictionary containing every variable in the game and the file it is defined in. 

list_of_variables = [] # List to contain all the created variables, to be populated into the dictionary
created_variables = {} # All the variables created in the game and the file in which they are created
duplicate_variables = [] # Variables that are created more than once in the startup file
row_number = 0

for string in complete_code['startup.txt']:
    row_number += 1
    if '*CREATE' in string:
        variable = string[string.find('*CREATE')+len('*CREATE'):].split()[0]
        if variable in list_of_variables:
            duplicate_variables.append (variable) #To match with the temp variables, we insert a dummy value of 0 to represent the row number
        else:
            list_of_variables.append ([row_number, variable]) # Create a list of all variable names that follow the *create command in startup

created_variables['startup.txt'] = list_of_variables # Add the list of variables as a value in the dictionary with the key being the startup.txt file name


for file, code in complete_code.items():
    list_of_variables = []
    row_number = 0
    for string in code:
        row_number += 1
        if '*TEMP' in string:
            variable = string[string.find('*TEMP')+len('*TEMP'):].split()[0]
            list_of_variables.append ([row_number, variable]) # Create a list of all variable names in the file which follow the *temp command
            created_variables[file] = list_of_variables # Add the list of variables as a value in the dictionary with the key being the file name

print ("Finished identifying all created and temp variable names in codebase\
       \n")
time.sleep(1)
##################################################################################################################           



##################################################################################################################          
#Parse the code to pull out all the variables referenced in the code and store a list, by file, of every single one.

# Define our functions for pulling out variable names from command strings and prose strings
def find_variables_in_command_strings (variables_in_file, string, bracket_variables_in_file, row_number):
    words_to_remove = [] # A list we are going to populate to hold all the strings that are not variables and need removing
    variables_to_add = [] # A lit of words we need to add, from parsing certain variable names. We remove the original and add this version
    multi_word_string = 'false' # Control within a loop to identify strings containing multiple words
    bracket_variables_in_string = []

    strings_to_remove_from_commands = ['ROUND(', 'MODULO', 'LENGTH(', '(', ')', '{', '}', '+', '=', '<', '>', '-', '&', '!', '%', '*IF', '*SET', '*ELSEIF', '*SELECTABLE_IF',\
                                   '*ELSE', '*INPUT_TEXT', '*INPUT_NUMBER', '*', '[B]', '[I]', '[/B]', '[/I]', '/', '$', '@', ':', '.', ',', ';', "'", '£']
    for string_to_remove in strings_to_remove_from_commands:
        string = string.replace(string_to_remove,' ')
    # Split the remaining string down into individual words. We need to evaluate each word independently now
    variables_in_string = string.split()

    try:
        for word in variables_in_string: # Loop through each word and check if it meets any criteria which denotes it as not being a variable
            error_location = ''
            if multi_word_string == 'true': # If a previous word was identified as the start of a multi-word string, then this kicks in and keeps flagging the words until it finds the end of the string
                error_location = "Looking for end of multi-word string"
                if (word.endswith("'") or word.endswith('"')): # If the word is the end of the string
                    multi_word_string = 'false' # Then switch this off
                words_to_remove.append(word)
            
            if word.isnumeric(): # If the word is a number
                error_location = "Checking numbers"
                words_to_remove.append(word)
                
            if word.startswith("'") and word.endswith("'") or word.startswith('"') and word.endswith('"'): #If the word is contained in quotes, i.e. is a value and not an attribute name
                error_location = "Checking actual strings"
                words_to_remove.append(word)
                
            if (word.startswith("'") or word.startswith('"')): # If the word is the start of a string of words (so it has opening quotes) - triggers the loop above
                error_location = "Checking start of multi-word strings"
                multi_word_string = 'true'
                words_to_remove.append(word)
                
            if '#' in word and '[' not in word: #In some cases, # is used to pull out the numbered character from a string, this chops off the # and number, just leaving the variable name                    
                error_location = "Removing # words"
                variables_to_add.append(word.split('#')[0])
                words_to_remove.append (word)
                
            if '[' in word:
                error_location = "Removing [] words"
                bracket_variables_in_string.append(word)
                words_to_remove.append(word)                    
                word = (word.split('[')[1])
                word = word.replace(']','')
                if '#' in word:
                    word = word.split('#')[0]
                variables_to_add.append(word)
    except:
        print ("******************************************************************************************\
              \nCStest encountered an error when trying to parse each word in the string.\
              \nFailing word: " + word + " \
              \nFailing string: " + string + " \
              \nError location: " + error_location + " \
              \n******************************************************************************************\
              \n")
         
    words_to_remove = list(dict.fromkeys(words_to_remove))
    variables_to_add = list(dict.fromkeys(variables_to_add))
    variables_in_string = list(dict.fromkeys(variables_in_string))
    bracket_variables_in_string = list(dict.fromkeys(bracket_variables_in_string))
    
    try:
        for word in words_to_remove:
            variables_in_string.remove(word)

    except:
        print ("******************************************************************************************\
              \nCStest encountered an error when trying to remove non-variable words from the list of variables.\
              \nThe word is likely not present in the list of variable names.\
              \nFailing word: " + word + " \
              \nFailing string: " + print(variables_in_string) + " \
              \n******************************************************************************************\
              \n")


    for variable in variables_in_string:
        if any (variable == file_variable[1] for file_variable in variables_in_file):
            pass
        else:
            variables_in_file.append([row_number, variable])

    for variable in variables_to_add:
        if any (variable == file_variable[1] for file_variable in variables_in_file):
            pass
        else:
            variables_in_file.append([row_number, variable])

    for variable in bracket_variables_in_string:
        if any (variable == file_variable[1] for file_variable in bracket_variables_in_file):
            pass
        else:
            bracket_variables_in_file.append([row_number, variable])
    
    return variables_in_file, bracket_variables_in_file


def find_variables_in_prose_strings (variables_in_file, string, bracket_variables_in_file, row_number):
    strings_to_remove_from_prose = ['ROUND(', 'MODULO', 'LENGTH(', '(', ')', '+', '=', '<', '>', '-', '&', '!', '%', '*IF', '*', '[B]', '[I]', '[/B]', '[/I]',\
                                    '/', '$', '@', ':', '.', ',', ';', '£', '"']
    for string_to_remove in strings_to_remove_from_prose:
                string = string.replace(string_to_remove,' ')
    if '{' in string:
        words_in_string = string.split()
        for word in words_in_string:
            if '{' in word:
                word = word.split('}')[0]
                word = word.split('{')[1]
                if '[' in word:
                    if any (word == file_variable[1] for file_variable in bracket_variables_in_file):
                        pass
                    else:
                        bracket_variables_in_file.append([row_number, word])
                    word = (word.split('[')[1])
                    word = word.replace(']','')
                    if '#' in word:
                        word = word.split('#')[0]
                    if any (word == file_variable[1] for file_variable in variables_in_file):
                        pass
                    else:
                        variables_in_file.append([row_number, word])                   
                else:
                    if any (word == file_variable[1] for file_variable in variables_in_file):
                        pass
                    else:
                        variables_in_file.append([row_number, word])
                                
    return variables_in_file, bracket_variables_in_file


# lists and dictionaries to store the lists of variables
called_variables = {}
bracket_variables = {}

# Loop through the code in each file. Identifying the variables in each file
for file, code in complete_code.items():
    print ("Finding variables in: " + file)
    
    variables_in_file = []
    bracket_variables_in_file = []
    row_number = 0

    # Loop through each string the code code of each file
    for string in code:
        
        row_number += 1

        string = re.sub(r'\bAND\b'  , '', string) #Remove 'and' where it is a standalone word and not part of a longer word
        string = re.sub(r'\bOR\b'   , '', string) #Remove 'or' where it is a standalone word and not part of a longer word
        string = re.sub(r'\bTRUE\b' , '', string) #Remove 'true' where it is a standalone word and not part of a longer word
        string = re.sub(r'\bFALSE\b', '', string) #Remove 'false' where it is a standalone word and not part of a longer word
        # Strip all the white space at the start of the string, allows us to correctly evaluate the first character of the string
        string = string.lstrip()

        # If the string is a command string, pass to the command function
        if (string.startswith('*IF') or string.startswith('*SET') or string.startswith('*ELSEIF') or string.startswith('*ELSE') or string.startswith('*INPUT_TEXT') or string.startswith('*INPUT_NUMBER')):
            variables_in_file, bracket_variables_in_file = find_variables_in_command_strings (variables_in_file, string, bracket_variables_in_file, row_number)

        # If it is a '*selectable_if' string, then split the string and pass the command half and prose half to the functions respectively
        elif string.startswith ('*SELECTABLE_IF'):
            command_string = string.split('#')[0]
            prose_string = string.replace(command_string,'')
            prose_string = prose_string[1:]

            variables_in_file, bracket_variables_in_file = find_variables_in_command_strings (variables_in_file, command_string, bracket_variables_in_file, row_number)
            variables_in_file, bracket_variables_in_file = find_variables_in_prose_strings (variables_in_file, prose_string, bracket_variables_in_file, row_number)

        #Otherwise it must be a prose string, so pass it to the prose function
        else:
            variables_in_file, bracket_variables_in_file = find_variables_in_prose_strings (variables_in_file, string, bracket_variables_in_file, row_number)

    if variables_in_file:
        #Add the list of variables to the dictionary with the filename as the key
        called_variables [file] = variables_in_file
        
    if bracket_variables_in_file:
        bracket_variables [file] = bracket_variables_in_file
    
##################################################################################################################


##################################################################################################################
#Check for whether there are any created variables that are not called in the code
variables_not_called = []

for created_file, created_variable_row in created_variables.items():
    for created_variable in created_variable_row:
        variable_found = False
        
        for called_file, called_variable_row in called_variables.items():
            if created_file == 'startup.txt' or called_file == created_file:           
                for called_variable in called_variable_row:
                    if variable_found == False:
                        if created_variable[1] == called_variable[1]:
                            variable_found = True

        for called_bracket_file, called_bracket_variable_row in bracket_variables.items():
            if created_file == 'startup.txt' or called_bracket_file == created_file:
                for called_bracket_variable in called_bracket_variable_row:
                    if created_variable[1].split('_')[0] == called_bracket_variable[1].split('[')[0]:
                        variable_found == True

        if variable_found == False:                
            variables_not_called.append([created_file, created_variable[1], created_variable[0]])  
       
##################################################################################################################


##################################################################################################################
#Check for any called variables which are not defined in startup, their file, or are defined on a later row number
#in their file than they are called
variables_not_defined = []
variables_defined_in_startup = []
variables_called_before_defined = []

for called_file, called_variable_row in called_variables.items():
    for called_variable in called_variable_row:
        if called_variable[1] not in variables_defined_in_startup: #If the variable name is in our list (generated in these loops), then we already know it has been defined and can be skipped
            variable_defined = False
            
            for created_file, created_variable_row in created_variables.items():
     
                if created_file == 'startup.txt' or called_file == created_file:
                    for created_variable in created_variable_row:
                        if variable_defined == False:
                            if called_variable[1] == created_variable[1]:
                                variable_defined = True
                                row_defined_on = created_variable[0]
                                if created_file == 'startup.txt':
                                    variables_defined_in_startup.append(called_variable[1]) #We query this list so that if we encounter the same variable in a different file, we already know it has been defined
      
            if variable_defined == False:
                variables_not_defined.append([called_file, called_variable[1], called_variable[0]])
            else:
                if called_variable[0] == row_defined_on:
                    variables_called_before_defined = [called_file, called_variable[1], called_variable[0], row_defined_on]
                

for called_bracket_file, called_bracket_variable_row in bracket_variables.items():
    for called_bracket_variable in called_bracket_variable_row:            
        for created_file, created_variable_row in created_variables.items():
            if created_file == 'startup.txt' or called_file == created_file:
                for created_variable in created_variable_row:
                    if variable_defined == False:
                        if called_bracket_variable[1].split('[')[0] == created_variable[1].split('_')[0]:
                            variable_defined = True
                            
        if variable_defined == False:
            variables_not_defined.append([called__bracket_file, called_bracket_variable[1], called_bracket_variable[0]])


##################################################################################################################


##################################################################################################################

# Parse the complete code to measure the indents on each line to spot cases where potentially the indent is incorrect

invalid_indents = {}
potentially_invalid_indents = {}
expected_indent = 0

for file, code in complete_code.items():

    file_invalid_indents = []
    file_potentially_invalid_indents = []
    expected_indent = 0
    
    for string in code:

        allowed_indents = [0]

        if ((len(string) - len(string.lstrip(' '))) % 4 == 0) or (len(string) - len(string.lstrip(' ')) == 0):
            indent_calculator = expected_indent
            while indent_calculator > 0:
                allowed_indents.append (indent_calculator)
                indent_calculator -= 4

            if len(string) - len(string.lstrip(' ')) not in allowed_indents:
                file_potentially_invalid_indents.append([string])

        else:
            file_invalid_indents.append([string])

        if len(string) - len(string.lstrip(' ')) in allowed_indents and expected_indent != 0:
            expected_indent = len(string) - len(string.lstrip(' '))

        no_space_string = string.lstrip(' ')
        if (no_space_string.startswith('*IF') or no_space_string.startswith('*ELSEIF') or no_space_string.startswith('*ELSE') or no_space_string.startswith('*SELECTABLE_IF') or no_space_string.startswith('*CHOICE') or \
            no_space_string.startswith('*FAKE_CHOICE') or no_space_string.startswith('#')):

            expected_indent += 4

    invalid_indents[file] = file_invalid_indents
    potentially_invalid_indents[file] = file_potentially_invalid_indents
     

print (potentially_invalid_indents)

# Put row number on the string

# *page_break will reset
# *goto will reset
# *gosub will reset







## Future functionality
# Spaces after a # when it denotes a choice - needs to catch
# Missing * on a command
# Misspelt command
# Output as complete errors as possible, the command that failed and the stats at that time



"""
To parse the schema:

Go through code and find each identifier for a decision in the code (if, selectable_if, choice)
Give each of them a unique ID (might need to store it in the actual code)

Then go through each item and find the ID of the items it links to. Store that in a dictionary format
ID : Conditions : link

Then parse the code to take each ID in turn and spawn the runs and follow the code

"""



     



#if duplicate_variables:
    #duplicate_variables = pd.DataFrame(duplicate_variables, columns = ['duplicate_variable_name'])
    
    #duplicate_variables.to_csv(pathlib.Path(test_run_path, 'duplicate_variables' + '.csv'))

# number_of_files

#variables not called
