import re
from datetime import date 
import getpass

def get_valid_password():
    while True: 
        password = getpass.getpass()
        if (len(password)<6 or len(password)>20):
            print("Password must be between 7 to 20 characters")
            continue
        elif re.search("[\W]",password):
            print("Password must be composed of lowercase, uppercase, number or underscore")
            continue
        else:
            return password


def get_valid_username():
    while True: 
        username = input("Input username: ")
        if (len(username)<6 or len(username)>20):
            print("Username must be between 7 to 20 characters")
            continue
        elif re.search("[\W]",username):
            print("Username must be composed of lowercase, uppercase, number or underscore")
            continue
        else:
            return username

def get_valid_name_age_birthday():
    while True: 
        name = input("Input name: ")
        if (len(name)>20 or len(name)<2):
            print("Name must be between 2 to 19 characters")
            continue
        elif re.search(r'(?i)\s+drop',name):
            print("Name must not have SQL keywords followed by a space. ")
            continue
        else:
            break

    while True:
        try:
            birthyear = int(input("Input birthyear: "))
            if (birthyear > 2020 or birthyear<1900):
                print("Input must be between 1900 and 2020")
                continue
            else:
                break
        except ValueError:
            print("Input is not a number")
            continue

    while True:
        try:
            birthmonth = int(input("Input birthmonth: "))
            if (birthmonth > 12 or birthmonth<1):
                print("Input must be between 1 and 12")
                continue
            else:
                break
        except ValueError:
            print("Input is not a number")
            continue        

    while True:
        try:
            birthday = int(input("Input birthday: "))
            if (birthday > 31 or birthday<1):
                print("Input must be between 1 and 31")
                continue
            else:
                break
        except ValueError:
            print("Input is not a number")
            continue
    
    today = date.today() 
    age = today.year - birthyear - ((today.month, today.day) < (birthmonth, birthday)) 

    return [name, age, birthyear, birthday, birthmonth]

def get_valid_filename():
    while True:
        filename = input("Input filename: ")
        if re.search("[~|//]",filename):
            print("Filename must not include backslashes or waves.")
            continue
        else:
            return filename

    