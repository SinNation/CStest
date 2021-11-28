##################################################################################################################
import os
import re
import time
import datetime
import pandas as pd
import pathlib
##################################################################################################################



##################################################################################################################
#Assumptions:
#CS tests makes some assumptions about the structure of the game code it is testing.
#1) It assumes that temporary variables are declared on an earlier row than they care called
#2) It assumes that no variable names use symbols that are commonly use in code (e.g. < !)
#3) It assumed that a variable with an _ is used in an array and is therefore handled differently
#4) Occurences of AND, OR, TRUE, FALSE are deemed to be part of the code and never variable names
##################################################################################################################



##################################################################################################################
#Set a time stamp to generate the folder with, to keep each run of the tests unique within a project
timestamp = datetime.datetime.now()
##################################################################################################################



##################################################################################################################
#Set all the path variables for the location of this code and the CS project
tests_path = os.getcwd() #Path of the folder containing CStest
cs_projects_path = os.path.dirname(os.getcwd()) #Parent path, should contain all CS project folders
##################################################################################################################



##################################################################################################################
print("=================================================================\
     \nWelcome to CStest. A python based testing engine for Choicescript.\
     \nThis script should be stored in a folder alongside your CS projects.\
     \nInput the name of the folder of the project you wish to test.\
     \n\
     \nA test outcome folder for the CS project will be generated.\
     \nThis folder is stored within the main CStest folder.\
     \nEvery test run will generate a timestamped folder for the project.\
     \n=================================================================\
     \n\
     \n")
##################################################################################################################



##################################################################################################################
#Have user input the folder name of their project and check it is valid
correct_folder = False #Keeps looping whilst the folder name that is input is not valid
while correct_folder == False:
    project_folder = input("What is the name of the folder your CS project is stored in?\
                           \n=================================================================\
                           \n")
    project_path = cs_projects_path + '\\' + project_folder #Set the project path using by appending the folder name
    if os.path.isdir(project_path) == False: #If that directory does not exist - it will loop back and ask for the input again
        print ("******************************************************************************************\
               \nThe project folder name " + project_folder + " that you input was not found in the directory: " + cs_projects_path + \
               ".\nEither the folder name was incorrect, or the folder does not exist in this directory. \
                .\nPlease ensure that the folder containing CStest is stored in the same location as all of your CS project folders.\
                \n****************************************************************************************\
                \n\
                \n")
        
    if os.path.isdir(project_path) == True:
        correct_folder = True #Sets the variable so the loop breaks and code continues
        print ("Project folder: " + project_folder + " has been found. CStest will begin.\
               \n")
        time.sleep(0.5)
##################################################################################################################



##################################################################################################################
#With the validated directory, generate a list of all .txt fields in the directory
list_of_files = [] #Empty list to append all the file names to
for file in os.listdir(project_path):
    if file.endswith('.txt'): #Loops through all the files with a .txt extension
       list_of_files.append(file)
number_of_files = len(list_of_files)
print (str(number_of_files) + ".txt files have been found in project folder: " + project_folder + "\n")
time.sleep(0.5)
##################################################################################################################



##################################################################################################################
#Set up the test folder to store all the test outcomes
try:
    if not os.path.exists(tests_path+'\\'+project_folder): #Checks if the directory already exists, so it won't try to recreate it
        os.makedirs(tests_path+'\\'+project_folder)
    os.makedirs(tests_path+'\\'+project_folder+'\\'+str(timestamp.strftime("%Y-%m%d-%H%M%S")))
except:
    print ("******************************************************************************************\
           \nCStest encountered an error when trying to create the test directory.\
           \nPlease report this as a bug with the following information:\
           \nAttempted to make this directory: " + tests_path+'\\'+project_folder+'\\'+str(timestamp.strftime("%Y-%m%d-%H%M%S")) + "\
           \n******************************************************************************************\
           \n\
           \n")
    input("Press ENTER to exit")
test_run_path = tests_path+'\\'+project_folder+'\\'+str(timestamp.strftime("%Y-%m%d-%H%M%S"))
print ("Outcome of tests will be stored in: " + test_run_path + "\n")
time.sleep(0.5)
##################################################################################################################



##################################################################################################################
#Parse all the files to ingest the complete code in the game. Remove line breaks and CS defined line and page breaks
#Then remove strings which are now wholly comprised of blank space. Then remove empty strings.                      
complete_code = {} #Dictionary to hold all the code in the game

for file in list_of_files: #Uses the list of files to allow us to cycle through all the files in the project
    file_path = project_path + '\\' + file #Constructs the file path for the specific file
    try:
        with open(file_path) as cs_file:
            code = cs_file.readlines() #Reads each line of the file in as a list of strings
    except:
        print ("******************************************************************************************\
              \nCStest encountered an error when trying to open file: " + file + " and read its contents.\
              \nPlease check the file is a valid CS txt file and if so, please report as a bug.\
              \nPlease provide this error message and the file that failed. \
              \nCStest will now exit as not reading in a .txt file could alter the outcome of the tests. \
              \n******************************************************************************************\
              \n\
              \n")
        input("Press ENTER to exit")

    try:
        error_location = "remove line breaks."
        remove_breaks = [line_of_code.replace('\n', '') for line_of_code in code] #Remove the generated line breaks in the code

        error_location = "uppercase strings."
        uppercase = [line_of_code.upper() for line_of_code in remove_breaks] #Uppercase all the strings

        error_location = "generate the numbered code."
        numbered_code = [] #Generate a list to store all the code strings alongside the row number
        for row_number, line_of_code in enumerate(uppercase): #Loop through all the lines of code in the file
            if str.isspace(line_of_code): #If the string contains only spaces then do nothing
                pass
            else:
                if not line_of_code: #Or if the string is completely empty then do nothing
                    pass
                else:
                    numbered_code.append([row_number +1, line_of_code]) #Otherwise append it to our list with the row number
    except:
        print ("******************************************************************************************\
              \nCStest encountered an error when trying to " + error_location + "\
              \nThe error occured with file: " + file + "\
              \nPlease report this bug along with the file that caused the error.\
              \n******************************************************************************************\
              \n\
              \n")
        input("Press ENTER to exit")
    
    complete_code[file] = numbered_code # Add the code for each file as a list of strings to the dictionary. The key is the file name
    
print ("Finished creating the code for all " + str(number_of_files) + ".txt files in the directory.\
       \n")
time.sleep(0.5)

##################################################################################################################

    

##################################################################################################################
# Parse the code to pull out all the cases where variables are defined and build a dictionary containing every variable in the game and the file it is defined in. 

list_of_variables = [] #List to contain all the created variables, to be populated into the dictionary
created_variables = {} #Dictionary to hold all the variables created in the game and the file in which they are created
list_of_duplicate_variables = [] #Variables that are created more than once in the startup file
duplicate_variables = {}


for original_string in complete_code['startup.txt']: #Take all the lines of code in the startup file. This gives us a list for each string (the row number and the code)
    string = original_string[1] #So take just the code and pass that in as our string
    if '*CREATE' in string: #If there is a *create command in our string, then it denotes the creation of a variable
        variable = string[string.find('*CREATE')+len('*CREATE'):].split()[0] #Split that string to just take the first word after the create command (chopping off the command and the initial value
        if variable in list_of_variables: #If the resulting variable already exists in our list, don't add it and instead identify it as a duplicate
            list_of_duplicate_variables.append ([original_string[0], variable])
        else:
            list_of_variables.append ([original_string[0], variable]) #Append to our list, taking the row number from the original string

    if '*TEMP' in string: #If there is a *temp command in our string, then it denotes the creation of a variable
        variable = string[string.find('*TEMP')+len('*TEMP'):].split()[0] #Split that string to just take the first word after the temp command (chopping off the command and the initial value
        if variable in list_of_variables: #If the resulting variable already exists in our list, don't add it and instead identify it as a duplicate
            list_of_duplicate_variables.append ([original_string[0], variable])
        else:
            list_of_variables.append ([original_string[0], variable]) #Append to our list, taking the row number from the original string

created_variables['startup.txt'] = list_of_variables #Add the list of variables as a value in the dictionary with the key being the startup.txt file name
duplicate_variables['startup.txt'] = list_of_duplicate_variables #Add the list of duplicate variables as a value in the dictionary with the key being the startup.txt file name


for file, code in complete_code.items(): #Now loop through all the files to look for temp variables in the remainder of the code. We want to bypass the startup file as we have already handled it
    if file != 'startup.txt': #Only process the file if it isn't the startup
        list_of_variables = [] #Reset the list of variables, so it is calculated fresh for each file
        list_of_duplicate_variables = [] #Reset the list of duplicate variables, so it is calculated fresh for each file
        for original_string in code: #Follow the same pattern as above
            string = original_string[1]
            if '*TEMP' in string:
                variable = string[string.find('*TEMP')+len('*TEMP'):].split()[0]
                if variable in list_of_variables:
                    list_of_duplicate_variables.append ([original_string[0], variable])
                #The difference here is that we want to append to the dictionary at the end of each file, so that we store the variables by file
                else:
                    list_of_variables.append ([original_string[0], variable]) # Create a list of all variable names in the file which follow the *temp command
        created_variables[file] = list_of_variables # Add the list of variables as a value in the dictionary with the key being the file name
        duplicate_variables[file] = list_of_duplicate_variables #Add the list of duplicate variables as a value in the dictionary with the key being the startup.txt file name

print ("Finished identifying all created and temp variable names in codebase\
       \n")
time.sleep(0.5)
##################################################################################################################           



#Parse the code to pull out all the variables referenced in the code and store a list, by file, of every single one.
##################################################################################################################          
# Define our function for pulling out variable names from command strings
def find_variables_in_command_strings (variables_in_file, string, bracket_variables_in_file, row_number):
    words_to_remove = [] #A list we are going to populate to hold all the strings that are not variables and need removing
    variables_to_add = [] #A list of words we need to add, from parsing certain variable names. We remove the original and add this version instead
    multi_word_string = 'false' #Control within a loop to identify strings containing multiple words
    bracket_variables_in_string = [] #A list to hold all the variables utilising [] in their names to be handled separately

    strings_to_remove_from_commands = ['ROUND(', 'MODULO', 'LENGTH(', '(', ')', '{', '}', '+', '=', '<', '>', '-', '&', '!', '%', '*IF', '*SET', '*ELSEIF', '*SELECTABLE_IF',\
                                   '*ELSE', '*INPUT_TEXT', '*INPUT_NUMBER', '*', '[B]', '[I]', '[/B]', '[/I]', '/', '$', '@', ':', '.', ',', ';', "'", '£'] #All valid characters that need to be cleaned out of strings
    for string_to_remove in strings_to_remove_from_commands:
        string = string.replace(string_to_remove,' ') #Remove the characters so that we are, as best as possible, just left with variable names.
        
    # Split the remaining string down into individual words. We need to evaluate each word independently now.
    variables_in_string = string.split() #This is a our baseline for all the variables in the string - we will remove/add as required

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
                
            if '[' in word: #'Bracket variables' are cases where a variable name is constructed by referring to another variable value. This identifies these.
                error_location = "Removing [] words" 
                bracket_variables_in_string.append(word) #We document the full variable as one to be handled separatelt
                words_to_remove.append(word) #So we remove it from our list as we will handle it separately                
                word = (word.split('[')[1]) #We can process the variable name in the brackets though, so split off everything after it
                word = word.replace(']','') #Replace the closing bracket
                if '#' in word: #If that variable also has a # in it to denote a character number, then split that off also
                    word = word.split('#')[0]
                variables_to_add.append(word) #Finally we have a clean word to record
    except:
        print ("******************************************************************************************\
              \nCStest encountered an error when trying to parse each word in the string.\
              \nFailing word: " + word + " \
              \nFailing string: " + string + " \
              \nError location: " + error_location + " \
              \n******************************************************************************************\
              \n")

    #De-duplicates all of our lists  
    words_to_remove = list(dict.fromkeys(words_to_remove)) 
    variables_to_add = list(dict.fromkeys(variables_to_add))
    variables_in_string = list(dict.fromkeys(variables_in_string))
    bracket_variables_in_string = list(dict.fromkeys(bracket_variables_in_string))

    #Remove the words from our list of variables
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

    #Append all the identified variables to a list containing the variables in the file
    for variable in variables_in_string:
        if any (variable == file_variable[1] for file_variable in variables_in_file):
            pass
        else:
            variables_in_file.append([row_number, variable])

    #Append all identified variables to add (from the brackets) to a list containing all the variables in the file
    for variable in variables_to_add:
        if any (variable == file_variable[1] for file_variable in variables_in_file):
            pass
        else:
            variables_in_file.append([row_number, variable])

    #Append all the bracket variables to a list containing all the bracket variables in the file
    for variable in bracket_variables_in_string:
        if any (variable == file_variable[1] for file_variable in bracket_variables_in_file):
            pass
        else:
            bracket_variables_in_file.append([row_number, variable])

    #End function by returning the two file level lists which were passed in initially, now updated for the current string.
    return variables_in_file, bracket_variables_in_file
##################################################################################################################



##################################################################################################################
#Define our function to pull out variables from prose strings
def find_variables_in_prose_strings (variables_in_file, string, bracket_variables_in_file, row_number):
    strings_to_remove_from_prose = ['ROUND(', 'MODULO', 'LENGTH(', '(', ')', '+', '=', '<', '>', '-', '&', '!', '%', '*IF', '*', '[B]', '[I]', '[/B]', '[/I]',\
                                    '/', '$', '@', ':', '.', ',', ';', '£', '"', '*page_break', '*line_break'] #Slightly different characters to strip from the string
    for string_to_remove in strings_to_remove_from_prose:
                string = string.replace(string_to_remove,' ') #Loop through the characters and replace them.
    if '{' in string: #In prose, variables are called with {} - this identifies that the string contains a variable
        words_in_string = string.split() #Split the string into its component words
        for word in words_in_string: #Loop through each word
            if '{' in word: #The word is a variable call
                word = word.split('}')[0] #Split out anything before or after the {} (including the {} )
                word = word.split('{')[1]
                if '[' in word: #If the variable contains a [ then handle it in the same way as a command variable
                    if any (word == file_variable[1] for file_variable in bracket_variables_in_file): #Don't do anything if the variable is already added for that file
                        pass
                    else:
                        bracket_variables_in_file.append([row_number, word]) #Store it as a bracket variable for handling separately
                    word = (word.split('[')[1]) #Strip off the square brackets
                    word = word.replace(']','')
                    if '#' in word:
                        word = word.split('#')[0] #Strip off the # if there is one
                    if any (word == file_variable[1] for file_variable in variables_in_file): #Leaving us with the variable called in the brackets - first check if we have already added it for the file
                        pass
                    else:
                        variables_in_file.append([row_number, word]) #Then add it              
                else:
                    if any (word == file_variable[1] for file_variable in variables_in_file): #Or it had no [] and is just a variable call. Check it isn't alreay added for the file
                        pass
                    else:
                        variables_in_file.append([row_number, word]) #Then add it
                                
    return variables_in_file, bracket_variables_in_file #Return the two lists of variables in the file
##################################################################################################################



##################################################################################################################
#Code which calls our two functions to identify all the variables in each file which have been called

#Dictionaries to store the variables in each file
called_variables = {}
called_bracket_variables = {}

#In the complete code we have the file name, under which is a list. This list contains a number of sub lists.
#Those sub lists each contain a row number and the line of code found on that row number.
#We want to take each line of code and parse it for the variables it calls.

for file, code in complete_code.items(): #Gives us the entire list of lists containing all the code in each file
    print ("Finding variables in: " + file)
    time.sleep(0.5)
    
    variables_in_file = [] #Creates our master list to store all the variables called in the file. We will pass this in and out of the functions
    bracket_variables_in_file = [] #Creates our master list to store all the bracket variables called in the file. We will pass this in and out of the functions

    #The code contains a number of lists in it, each list is a line of code and a row number. Loop through each of these
    for original_string in code:

        string = original_string[1] #Redefine our string as just the line of code, ignoring the row number

        #Remove AND, OR, TRUE and FALSE as there are frequently found in the code but are not variable names
        string = re.sub(r'\bAND\b'  , '', string) #Remove 'and' where it is a standalone word and not part of a longer word
        string = re.sub(r'\bOR\b'   , '', string) #Remove 'or' where it is a standalone word and not part of a longer word
        string = re.sub(r'\bTRUE\b' , '', string) #Remove 'true' where it is a standalone word and not part of a longer word
        string = re.sub(r'\bFALSE\b', '', string) #Remove 'false' where it is a standalone word and not part of a longer word
        
        #Strip all the white space at the start of the string, allows us to correctly evaluate the first character of the string
        string = string.lstrip()

        #Identify if the a command string and if so, pass to the command function
        if (string.startswith('*IF') or string.startswith('*SET') or string.startswith('*ELSEIF') or string.startswith('*ELSE') or string.startswith('*INPUT_TEXT') or string.startswith('*INPUT_NUMBER')):
            variables_in_file, bracket_variables_in_file = find_variables_in_command_strings (variables_in_file, string, bracket_variables_in_file, original_string[0]) #Pass in the cleansed string and the original row number

        #If the command is a '*selectable_if' string, then split the string and pass the command half and prose half to the functions respectively
        elif string.startswith ('*SELECTABLE_IF'):
            command_string = string.split('#')[0] #Split out before the #, giving us just the code
            prose_string = string.replace(command_string,'') #Then the remainder is the prose - cut off the command string
            prose_string = prose_string[1:]

            variables_in_file, bracket_variables_in_file = find_variables_in_command_strings (variables_in_file, command_string, bracket_variables_in_file, original_string[0])
            variables_in_file, bracket_variables_in_file = find_variables_in_prose_strings (variables_in_file, prose_string, bracket_variables_in_file, original_string[0])

        #Otherwise it must be a prose string, so pass it to the prose function
        else:
            variables_in_file, bracket_variables_in_file = find_variables_in_prose_strings (variables_in_file, string, bracket_variables_in_file, original_string[0])

    if variables_in_file: #After finishing all the code in the file
        #Add the list of variables to the dictionary with the filename as the key
        called_variables [file] = variables_in_file
        
    if bracket_variables_in_file: #Do the same for the bracket variables
        called_bracket_variables [file] = bracket_variables_in_file

print ("Finished finding variables in all files.")
time.sleep(0.5)
##################################################################################################################



##################################################################################################################
#Check for whether there are any created variables that are not called in the code.
variables_not_called = []

for created_file, created_variable_row in created_variables.items(): #Loop through all the files
    for created_variable in created_variable_row: #Loop through all the variables created in the file
        variable_found = False #Set the variable as 'not found' to begin with.
        
        for called_file, called_variable_row in called_variables.items(): #Loop through all the files to find if the variable is called in it
            if created_file == 'startup.txt' or called_file == created_file: #Only compare variables defined in the startup (which can be called anywhere), or variables defined in the SAME file we're checking (for temp variables)         
                for called_variable in called_variable_row: #Loop through all the called variables in the file
                    if variable_found == False: #If we haven't already found it
                        if created_variable[1] == called_variable[1]: #And the variable we are currently comparing matches the one we are searching for. Here we take the second element of the list, as the first element is the row number
                            variable_found = True #Then set it to 'found'

        for called_bracket_file, called_bracket_variable_row in bracket_variables.items(): #Repeat for the bracket variables
            if created_file == 'startup.txt' or called_bracket_file == created_file:
                for called_bracket_variable in called_bracket_variable_row:
                    if created_variable[1].split('_')[0] == called_bracket_variable[1].split('[')[0]: #Difference here is we split the variables before the _ and brackets and simply match on the stub
                        variable_found == True

        if variable_found == False: #After looking for the variable in every file and not finding it, add it as a non-called variable             
            variables_not_called.append([created_file, created_variable[1], created_variable[0]])  
       
##################################################################################################################



##################################################################################################################
#Check for any called variables which are not defined in the startup or are not defined in the same file (temp)
#Also, where it is a temp variable, it also checks if it was defined on a later row number than the one it was called on
variables_not_defined = []
variables_defined_in_startup = []
variables_called_before_defined = []

for called_file, called_variable_row in called_variables.items(): #Loop through our files
    for called_variable in called_variable_row: #Loop through each called variable in the file
        if called_variable[1] not in variables_defined_in_startup: #If the variable name is in our list (generated in these loops), then we already know it has been defined and can be skipped
            variable_defined = False #Set variable as not defined, until we see that it is
            
            for created_file, created_variable_row in created_variables.items(): #Loop through each file
     
                if created_file == 'startup.txt' or called_file == created_file: #If the file is startup or the same file we are checking, then proceed (we don't want to check temp variables in other files)
                    for created_variable in created_variable_row: #Loop through each created variable in that file
                        if variable_defined == False: #If we haven't se the variable to defined yet
                            if called_variable[1] == created_variable[1]: #Then check if the variable we are checking matches the one we are searching for
                                variable_defined = True #And if so, set it to 'defined'
                                row_defined_on = created_variable[0] #Record the row number to now check which row it was defined on
                                if created_file == 'startup.txt':
                                    variables_defined_in_startup.append(called_variable[1]) #We query this list so that if we encounter the same variable in a different file, we already know it has been defined
      
            if variable_defined == False: #If we get through all the files and we never find the variable, add it as a non-defined variable
                variables_not_defined.append([called_file, called_variable[1], called_variable[0]])
            else:
                if called_variable[0] <= row_defined_on: #Otherwise check what row it was called on and if it was defined on an earlier row, add it to the list
                    variables_called_before_defined.append ([called_file, called_variable[1], called_variable[0], row_defined_on])
                

#DO WE ADD MORE FUNCTIONALITY BELOW

#Repeat for the bracket variables. The main difference here is we just match on the stub. So we don't record whether it was called before defined and so on, because
# we are not matching exactly on the variable names
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
required_indent = False

for file, code in complete_code.items():

    file_invalid_indents = []
    file_potentially_invalid_indents = []
    expected_indent = 0
    
    for original_string in code:

        string = original_string[1]

        allowed_indents = [0]

        if ((len(string) - len(string.lstrip(' '))) % 4 == 0) or (len(string) - len(string.lstrip(' ')) == 0):           
            
            indent_calculator = expected_indent
            while indent_calculator > 0:
                allowed_indents.append (indent_calculator)
                indent_calculator -= 4

            if len(string) - len(string.lstrip(' ')) not in allowed_indents:
                file_potentially_invalid_indents.append([original_string[0], string])

            else:
                if required_indent == True:
                    required_indent = False
                    if len(string) - len(string.lstrip(' ')) != expected_indent:
                        file_invalid_indents.append([original_string[0], string])   

        else:
            file_invalid_indents.append([original_string[0], string])

        if len(string) - len(string.lstrip(' ')) in allowed_indents and expected_indent != 0:
            expected_indent = len(string) - len(string.lstrip(' '))

        no_space_string = string.lstrip(' ')
        if (no_space_string.startswith('*IF') or no_space_string.startswith('*ELSEIF') or no_space_string.startswith('*ELSE') or no_space_string.startswith('*SELECTABLE_IF') or no_space_string.startswith('*CHOICE') or \
            no_space_string.startswith('*FAKE_CHOICE') or no_space_string.startswith('#')):

            required_indent = True
            expected_indent += 4

    invalid_indents[file] = file_invalid_indents
    potentially_invalid_indents[file] = file_potentially_invalid_indents


print (invalid_indents)
print ("\n")
print (potentially_invalid_indents)
print ("\n")
print (variables_called_before_defined)
print ("\n")
print (variables_not_defined)
print ("\n")
print (variables_not_called)

duplicate_variables


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
