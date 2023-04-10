"""
Building a Hack Assembler in Python

GitHub : https://github.com/VishalTheHuman
LinkedIn : https://www.linkedin.com/in/vishalthehuman/
"""
# Using Remove function from the Library "OS" to delete the intermediate file created "New.hack"
import os 

# Global Declaration :

# Predefined Values

# Jump : Binary Equivalent
jump = {
    "null":"000",
    "JGT":"001",
    "JEQ":"010",
    "JGE":"011",
    "JLT":"100",
    "JNE":"101",
    "JLE":"110",
    "JMP":"111"
}

# Destination : Binary Equivalent
destination={
    "null":"000",
    "M":"001",
    "D":"010",
    "MD":"011",
    "A":"100",
    "AM":"101",
    "AD":"110",
    "AMD":"111"
}

# Computation Binary values when "A" is present in the line
comp_a_0={
    "0":"101010",
    "1":"111111",
    "-1":"111010",
    "D":"001100",
    "A":"110000",
    "!D":"001101",
    "!A":"110001",
    "-D":"001111",
    "-A":"110011",
    "D+1":"011111",
    "A+1":"110111",
    "D-1":"001110",
    "A-1":"110010",
    "D+A":"000010",
    "A+D":"000010",
    "D-A":"010011",
    "A-D":"000111",
    "D&A":"000000",
    "D|A":"010101"
}

# Computation Binary values when "M" is present in the line
comp_a_1={
    "M":"110000",
    "!M":"110001",
    "-M":"110011",
    "M+1":"110111",
    "M-1":"110010",
    "D+M":"000010",
    "M+D":"000010",
    "D-M":"010011",
    "M-D":"000111",
    "D&M":"000000",
    "D|M":"010101"
}

# Dictonary to use in code to distinguish between variables and registers(Like R0,R1,R2...)
Allowed_Integers={
    "0":"0",
    "1":"1",
    "2":"2",
    "3":"3",
    "4":"4",
    "5":"5",
    "6":"6",
    "7":"7",
    "8":"8",
    "9":"9"
}

# Predefined Labels + Adding new Labels to the dictionary if the input code contains any other new Labels
label={
    "SCREEN":"16384",
    "KBD":"24576",
    "SP":"0",
    "LCL":"1",
    "ARG":"2",
    "THIS":"3",
    "THAT":"4"
}

# A place to store the variable name with the register number starting from the "Register 16"
variables={
    
}

# To remove the White Spaces
def RemoveWhiteSpace(string):
    # Replacing " " with an empty ""
    return string.replace(" ","")

# To remove R if the A-Instruction conatins R
def Remove_R(string):
    if string:
        #To remove only R in case of mentioning the register and Avoid Removing Variables names Starting with R
        if string[1]=="R" and Allowed_Integers.get(string[2])!=None: 
            # Replacing "R" with an empty ""
            string=string.replace("R","")
            return string
    return string

# To remove comments 
def RemoveComments(string):
    count=0
    flag=False
    for x in range(len(string)):
        if string[x]=="/":
            count+=1
            if(count==2):
                return string[:x-1]
        elif count == 1:
            flag=True
            if count == 1 or (count ==1 and flag==True):
                # To raise error if only one "/" is Present and the next "/" is not present
                raise Exception("Error in the Code : Only one '/' is present.")
    if count == 1:
                # To raise error if only one "/" is Present in the entire line
                raise Exception("Error in the Code : Only one '/' is present.")
    return string

#To Read and Convert the A-Instruction
def A_Instruction(string):
    string = string.replace("@","")
    string = string.replace("R","")
    return Decimal_to_Binary(int(string))

# Convert A-Instruction to 1 Operation Code + 15 Value 
def Decimal_to_Binary(decimal):
    decimal=int(decimal)
    if decimal<0:
        # To raise an error if the Decimal value is "Negative"
        raise Exception("The Decimal value entered is 'Negative'")
    # The output of bin(Decimal) will be like 0bXXXXXX to remove the "0b" we are slicing the string
    bin_str = bin(decimal)[2:] 
    # To extend the binary equilaent to 16-Bits
    if len(bin_str)<16:
        while 16-len(bin_str)!=0:
            bin_str="0"+bin_str
    return bin_str

# To convert a C-Instruction to it's Binary Equivalent 
def reading_C_Instruction(string):
    # Declaring Variables that we are going to use
    flag=0
    dest = False
    comp = False
    jmp=False
    equalindex=0
    jumpindex=0
    jumpstatement="Jump Statement"
    colonindex=0
    # Accessing each character in the line and categorizing destination,computation, and jump
    for x in string:
        if dest != True:
            if x=="=" and flag>0:
                destinationstr = string[:flag]
                equalsign=string[flag-1:flag]
                equalindex=flag
                dest = True
                if destination.get(destinationstr)==None:
                    raise Exception("Invalid Destination")
        if jmp !=True :
            if x == ";" and flag>0:
                colonindex=flag
                jumpstatement = string[colonindex+1:]
                if jump.get(jumpstatement)==None:
                    raise Exception("Invalid Syntax in JMP Statement")
                jumpindex=flag
                jmp = True
        flag+=1
    if jumpindex>0:
        if dest==True:
            comp = string[equalindex+1:colonindex]
        elif dest == False:
            comp = string[:colonindex]
    elif jumpindex==0:
        comp = string[equalindex+1:]
    # To raise an error if mistake is found in the computation by checking the corresponding value with the pre-defined dictionary
    if comp_a_0.get(comp)==None and comp_a_1.get(comp)==None:
        raise Exception("Error in the Computation Part")
    # When A=0
    elif comp_a_1.get(comp)==None:
        # Both Destination and Jump is present
        if jmp==True and dest==True:
            return "111"+"0"+comp_a_0.get(comp)+destination.get(destinationstr)+jump.get(jumpstatement)
        # Only Jump is present
        elif jmp==True and dest==False:
            return "111"+"0"+comp_a_0.get(comp)+destination.get("null")+jump.get(jumpstatement)
        # Only Destination is present
        elif jmp==False and dest == True:
            return "111"+"0"+comp_a_0.get(comp)+destination.get(destinationstr)+jump.get("null")
        # Raise an error if both are absent
        elif jmp==False and dest == False:
            raise Exception("Neither Jump nor Destination is Present")
    # When A=1
    elif comp_a_0.get(comp)==None:
        # Both Destination and Jump is present
        if jmp==True and dest==True:
            return "111"+"1"+comp_a_1.get(comp)+destination.get(destinationstr)+jump.get(jumpstatement)
        # Only Jump is present
        elif jmp==True and dest==False:
            return "111"+"1"+comp_a_1.get(comp)+destination.get("null")+jump.get(jumpstatement)
        # Only Destination is present
        elif jmp==False and dest == True:
            return "111"+"1"+comp_a_1.get(comp)+destination.get(destinationstr)+jump.get("null")
        # Raise an error if both are absent
        elif jmp==False and dest == False:
            raise Exception("Neither Jump nor Destination is Present")

# To Handle Labels and store the Label Values inside the "label" Dictionary
def handlelabels(input_file):
    with open(input_file, 'r') as input_file:
        index=0
        flag=0
        # Reading Each Line in the .asm file
        for line in input_file:
            stripped_line=RemoveComments(RemoveWhiteSpace(str(line)))
            stripped_line = stripped_line.strip()
            # Executes only if the stripped line is non-empty
            if stripped_line:
                if label.get(stripped_line[1:len(stripped_line)-1])==None:
                    # If "(" is found in the start and ")" found in the end
                    if stripped_line[0]=="(" and stripped_line!=None:
                        if stripped_line[len(stripped_line)-1]==")":
                            stripped_line=stripped_line[1:len(stripped_line)-1]
                            flag = index
                            # Adding to the "label" Dictionary
                            label.update({stripped_line:str(flag)}) 
                        else:
                            #If the Label is not closed Properly raise an Error
                            raise Exception("The Label is not Closed Properly")
                    else:
                        index+=1
    input_file.close()
    # Printing out all the labels found in the terminal
    print("Labels : ",end="")
    print(label)


def handlevariables(input_file):
    with open(input_file,"r") as input_file:
        variable = 16
        # Reading Each Line in the .asm file
        for line in input_file:
            stripped_line=RemoveComments(RemoveWhiteSpace(str(line)))
            stripped_line = stripped_line.strip()
            stripped_line = Remove_R(stripped_line)
            # Executes only if the stripped line is non-empty
            if stripped_line:
                # To Identify the labels
                if stripped_line[0]=="@":
                    if variables.get(stripped_line[1:])==None and Allowed_Integers.get(stripped_line[1])==None:
                        # To ensure we are not mistaking a label for a variable
                        if label.get(stripped_line[1:])==None:
                            stripped_line=stripped_line[1:]
                            # Adding to the "variable" Dictionary
                            variables.update({stripped_line:str(variable)})
                            variable+=1
        input_file.close()
    # Printing out all the variables found in the terminal
    print("Variables : ",end="")
    print(variables)


def fixloopsandvariables(input_file):
    # Then replacing the variables and labels with corresponding values
    # Creating and intermediate file "New.asm" to write the modified code
    with open(input_file, 'r') as input_file, open("New.asm","w") as output_file:
        # Reading Each Line in the .asm file
        for line in input_file:
            stripped_line=RemoveComments(RemoveWhiteSpace(str(line)))
            stripped_line = stripped_line.strip()
            # Executes only if the stripped line is non-empty
            if stripped_line:
                # Identify Label
                if stripped_line[0]=="@" and label.get(stripped_line[1:])!=None:
                    output_file.write("@"+label.get(stripped_line[1:]))
                    output_file.write("\n")
                # Identify Variable
                elif stripped_line[0]=="@" and variables.get(stripped_line[1:])!=None:
                    output_file.write("@"+variables.get(stripped_line[1:]))
                    output_file.write("\n")
                # Ignore Label Declaration
                elif stripped_line[0]=="(":
                    continue
                # Writing the line if no changes were made
                else:
                    output_file.write(stripped_line)
                    output_file.write("\n")
    input_file.close()
    output_file.close()


def main(main_file):
    # Identifying the Labels and Variables and Modifying the code accordingly before converting it
    handlelabels(main_file)
    handlevariables(main_file)
    fixloopsandvariables(main_file)
    # The modified file is stored in the name of "New.hack" which will be the input for conversion
    input_file='New.asm'
    with open(input_file, 'r') as input_file, open(main_file[:len(main_file)-3]+"hack", 'w') as output_file:
        # Reading Each Line in the .asm file
        for line in input_file:
            stripped_line = line.strip()
            stripped_line=RemoveComments(RemoveWhiteSpace(str(stripped_line)))
            # Executes only if the "stripped_line" is non-empty
            if stripped_line: 
                # If the first character of "the stripped line" is "@", it is an A-Instruction. Otherwise, it is a C-Instruction.
                if stripped_line[0]=="@":
                    #Executes A-Instruction Conversion
                    output_file.writelines(A_Instruction(stripped_line)) 
                    #Move to a new Line
                    output_file.writelines("\n") 
                else:
                    #Executes C-Instruction Conversion
                    output_file.writelines(reading_C_Instruction(stripped_line)) 
                    #Move to a new Line
                    output_file.writelines("\n") 
    # Closing the files
    input_file.close() 
    output_file.close()
    # Deleting the Intermediate File "New.asm"
    os.remove("New.asm")

# Calling the main function and passing the file name/location as a parameter 
main("D:\Code\Projects\Hack Assembler\/test\Max.asm")