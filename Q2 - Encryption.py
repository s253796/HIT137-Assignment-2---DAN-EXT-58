# HIT137 Assignment 2 - Question 1 Encryption/Decryption
# Group Name: DAN/EXT 58
# PRADIKSHYA DHAKAL - s396200
# SHEREENA FERNANDO FERNANDO - s387227
# MEL HA - s253796
with open("raw_text.txt", "r") as file:
    text= file.read ()
# User input for variables is obtained.
shift1 = int(input("Enter shift1 value: "))
shift2 = int(input("Enter shift2 value: "))
encrypted_text =  ""
encryption_flags = []
# Flags are used because while encryption will work smoothly, decryption may have overlapping possible values making it inaccurate.

# Text is encrypted based on which characters are used; whichever encryption method was used is recorded (flagged) at each character position (index).
# Wrap around calculations are used for when characters go past z or before a.
for ch in text:
    ordvalue = ord(ch)
    if ch >= 'a' and ch <= 'm': 
        ciphervalue = ordvalue + shift1*shift2
        if ciphervalue > ord('z'):
            x = ciphervalue - ord('z') - 1
            ciphervalue = ord('a') + (x % 26)
        encryption_flags.append('a-m')       
    elif ch >= 'n' and ch <= 'z':
        ciphervalue = ordvalue - (shift1+shift2)
        if ciphervalue < ord('a'):
            y = ord('a') - (ciphervalue + 1)
            ciphervalue = ord('z') - (y % 26)
        encryption_flags.append('n-z')
    elif ch >= 'A' and ch <= 'M': 
        ciphervalue = ordvalue - shift1
        if ciphervalue < ord('A'):
            y = ord('A') - (ciphervalue + 1)
            ciphervalue = ord('Z') - (y % 26)
        encryption_flags.append('A-M')
    elif ch >= 'N' and ch <= 'Z':
        ciphervalue = ordvalue + shift2**2
        if ciphervalue > ord('Z'):
            x = ciphervalue - ord('Z') - 1
            ciphervalue = ord('A') + (x % 26)
        encryption_flags.append('N-Z')

    else:
        ciphervalue = ordvalue
        encryption_flags.append ('other')
    encrypted_text = encrypted_text + chr(ciphervalue)

with open("encrypted_text.txt", "w") as file:
    file.write(encrypted_text)

with open("encrypted_text.txt", "r") as file:
    text= file.read ()

decrypted_text =  ""
# Enumerate used to identify the index and determine what encryption flag was used for each character.
for i, ch in enumerate (text):
    ordvalue = ord(ch)
    flag = encryption_flags [i]
    # Text decrypted using stored flags to reverse encryption shifts.
    if flag == 'a-m':
        ciphervalue = ordvalue - shift1*shift2
        if ciphervalue < ord('a'):
            x = ord('a') - (ciphervalue + 1)
            ciphervalue = ord('z') - (x % 26)
    elif flag == 'n-z':
        ciphervalue = ordvalue + (shift1+shift2)
        if ciphervalue > ord('z'):
            y = ciphervalue - ord('z') - 1
            ciphervalue = ord('a') + (y % 26)
    elif flag == 'A-M':
        ciphervalue = ordvalue + shift1
        if ciphervalue > ord('Z'):
            y = ciphervalue - ord('Z') - 1
            ciphervalue = ord('A') + (y % 26)
    elif flag == 'N-Z':
        ciphervalue = ordvalue - shift2**2
        if ciphervalue < ord('A'):
            x = ord('A') - (ciphervalue + 1)
            ciphervalue = ord('Z') - (x % 26)

    elif flag == 'other':
            ciphervalue = ordvalue
    decrypted_text = decrypted_text + chr(ciphervalue)

with open("decrypted_text.txt", "w") as file:
    file.write(decrypted_text)
# Raw text compared directly to decrypted text to verify encryption to decryption was successful.
with open("raw_text.txt", "r") as raw:
    raw_text = raw.read ()
with open("decrypted_text.txt", "r") as decrypted:
    decrypted_text = decrypted.read ()

if raw_text == decrypted_text:
    print ("Decryption successful.")
else:
    print ("Decryption failed.")
