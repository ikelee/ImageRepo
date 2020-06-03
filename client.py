import dao
import helper
import session as se
import os

def login(repo, username, password):
    print("logging in...\n")
    id = repo.login(username, password)

    if id:
        print("Success! \n")
        se.Session(repo, id)
    else:
        print("Failed\n")

def create_new_user(repo):
    username = helper.get_valid_username()
    while repo.check_user_exists(username):
        print("Username in use. Try another one.")
        username = helper.get_valid_username()

    password = helper.get_valid_password()

    successful = repo.create_new_user(username, password)
    if successful:
        repo.create_new_user_info(username, helper.get_valid_name_age_birthday())
        print("New user created. Logging in...")
        login(repo, username, password)
    else:
        print("New user creation failed.\n")


if __name__ == "__main__":
    while(True):
        i = input("Welcome. Press l to login and n for create new user, and o to view open images\n")
        repo = dao.repo()
        if i == 'l':
            username = helper.get_valid_username()
            if not repo.check_user_exists(username):
                print("Username doesn't exist")
                continue
            password = helper.get_valid_password()
            login(repo, username, password)
        elif i == 'n':
            create_new_user(repo)
        elif i == 'o':
            print("ID\t\tName\t\t\t\tPublic")
            for image in repo.get_public_images():
                print(str(image[0]) + "\t\t" + str(image[2]) + "\t\t" + str(image[5]))
            
        else:
            print("wrong input\n")