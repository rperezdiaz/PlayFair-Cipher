""" 
playfair.py 
Author: Rey F. Pérez Díaz
"""

import string

#generates a PlayFair Matrix
def generate_matrix(keyword: string) -> list:
    #format user input
    keyword = keyword.upper()
    keyword = keyword.replace("J","I") #replace j's with i's 

    alphabet = "abcdefghiklmnopqrstuvwxyz".upper()
    keystring = ""

    #get all non-duplicate alphabetic symbols in user input
    for char in keyword:
        if char.isalpha() and char not in keystring:
            keystring += char

    #add the rest of missing alphabet to keystring
    for letter in alphabet:
        if letter not in keystring:
            keystring += letter

    #trasnform keystring to playfair matrix
    cols, rows = 5 , 5
    matrix = [ [0]*cols for i in range(rows)]
    ctr = 0
    for i in range(rows):
        for j in range(cols):
            matrix[i][j] = keystring[ctr]
            ctr+=1

    return matrix

#prints the matrix
def print_matrix(matrix: list):
    print("\nThis is the key matrix: \033[96m")
    for row in matrix:
        print(row)
    print("\033[0m")


def get_usr_input(option: int):
    if option == 1:
        msg = input("\nEnter the plain text message: ")
    else:
        msg = input("\nEnter the encrypted message: ")
    kw = input("Enter key word: ")
    return kw, msg

#shows terminal based menu
def show_menu():
    ans = ""
    while ans != 0:
        print("\nWhat do you want to do?")
        print("1. ENCRYPT a message\n2. DECIPHER a message\n0. EXIT")
        ans = int(input("Enter option number: "))
        if ans == 1:
            kw, msg = get_usr_input(ans)
            encrypt(kw, msg)
            break
        elif ans == 2:
            kw, msg = get_usr_input(ans)
            decipher(kw, msg)
            break
        elif ans != 0:
            print("\n\033[93m"+ str(ans), "is not a valid input\033[0m")
            print("\nWhat do you want to do?")
            print("1. ENCRYPT a message\n2. DECIPHER a message\n0. EXIT")
            ans = int(input("Enter option number: "))

def process_message_string(message:string):
    #remove non-alphabetic characters from message
    message = message.upper()
    for char in message:
        if char not in string.ascii_uppercase:
            message = message.replace(char, "")

    #check pairs, add X between digraphs
    i = 0
    while i < len(message)-1:
        if message[i] == message[i+1]:
            message = message[:i+1] + 'X' + message[i+1:]
        i+=2
    
    #form pair for single letter
    if len(message) %2 != 0:
        message = message + 'Z' 

    return message

#returns a string containing the encrypted message
def encrypt(keyword:string, message:string):
    pf_matrix = generate_matrix(keyword)
    print_matrix(pf_matrix)

    message = process_message_string(message)

    i = 0
    encrypted_message=""
    while i < len(message)-1:
        #get letter locations in matrix
        loc1 = get_location(message[i],pf_matrix) 
        loc2 = get_location(message[i+1],pf_matrix)

        #check letter position and substitute
        if loc1[0] == loc2[0]: #letters in same row 
            r1,c1 = loc1[0],loc1[1]+1
            r2,c2, = loc2[0],loc2[1]+1
            #adjust column indeces; 4 is the highest index in a 5x5 matrix
            if c1 > 4: 
                c1=0
            if c2 > 4:
                c2= 0
            encrypted_message += pf_matrix[r1][c1] + pf_matrix[r2][c2] #concat pair substitution
        elif loc1[1] == loc2[1]: #letters in same column
            r1,c1 = loc1[0]+1,loc1[1]
            r2,c2, = loc2[0]+1,loc2[1]
            #adjust row indices 
            if r1 > 4: 
                r1=0
            if r2 > 4:
                r2= 0
            encrypted_message += pf_matrix[r1][c1] + pf_matrix[r2][c2]
        else: #rectangle formed
            r1,c1 = loc1[0],loc1[1]
            r2,c2, = loc2[0],loc2[1]
            encrypted_message += pf_matrix[r1][c2] + pf_matrix[r2][c1]
        
        i+=2 #next two letters
    print("This is the encrypted message:\033[96m")
    print_pairs(encrypted_message)
    print("\033[0m")

def print_pairs(str:string):
    i=0
    paired = ""
    for letter in str:
        if i >= 2:
            paired += " "
            i=0
        paired += letter
        i+=1
    print(paired)

#returns tuple of letter coordinates 
def get_location(letter:string, matrix:list):
    row = 0
    for r in matrix:
        col = 0
        for c in matrix[row]:
            if matrix[row][col] == letter:
                return row,col
            col += 1
        row += 1
    
    return row,col

#returns a string containing the plain text message
def decipher(keyword:string, message:string):
    pf_matrix = generate_matrix(keyword)
    print_matrix(pf_matrix)

    message = message.replace(" ", "") #remove whitespace

    i = 0
    deciphered_message=""
    while i < len(message)-1:
        #get letter locations in matrix
        loc1 = get_location(message[i],pf_matrix) 
        loc2 = get_location(message[i+1],pf_matrix)

        #check letter position and substitute
        if loc1[0] == loc2[0]: #letters in same row 
            r1,c1 = loc1[0],loc1[1]-1
            r2,c2, = loc2[0],loc2[1]-1
            #adjust column indeces; 4 is the highest index in a 5x5 matrix
            if c1 < 0: 
                c1 = 4
            if c2 < 0:
                c2 = 4
            deciphered_message += pf_matrix[r1][c1] + pf_matrix[r2][c2] #concat substitution
        elif loc1[1] == loc2[1]: #letters in same column
            r1,c1 = loc1[0]-1,loc1[1]
            r2,c2, = loc2[0]-1,loc2[1]
            #adjust row indices 
            if r1 < 0: 
                r1 = 4
            if r2 < 0:
                r2 = 4
            deciphered_message += pf_matrix[r1][c1] + pf_matrix[r2][c2]
        else: #rectangle formed
            r1,c1 = loc1[0],loc1[1]
            r2,c2, = loc2[0],loc2[1]
            deciphered_message += pf_matrix[r1][c2] + pf_matrix[r2][c1]
        
        i+=2 # evaluate next two letters

    deciphered_message = remove_filler(deciphered_message)

    print("This is the deciphered message message:\033[96m")
    print(deciphered_message)
    print("\033[0m")

def remove_filler(message:string):
    #remove Z from adjusted single letter
    idx = len(message)-1
    if len(message) % 2 == 0 and message[idx] == "Z":
        message = message[0:idx]

    #remove X between digraphs
    i=0
    while i < len(message)-2:
        if message[i] == "X" and message[i-1] == message[i+1]:
            message = message[:i] + message[i+1:]
        i+=1

    return message

def main():
    show_menu()

#Starts execution of program
if __name__ == "__main__":
    main()