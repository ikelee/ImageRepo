import dao
import os
import helper
import shutil

class Session:
    def __init__(self, repo, id):
        info = repo.get_user_info(id)

        self.repo = repo
        self.id = id
        self.name = info[1]
        self.age = info[2]
        self.birthday = info[3]
        
        os.system('clear')
        print("Welcome, ", self.name)

        while(True):
            i = input("Press a to add images, d to delete images and s to see inventory\n")
            if i == 'a':
                self.add_images()
            elif i == 'd':
                self.delete_images()
            elif i == 's':
                self.see_inventory()
            elif i == 'm':
                self.manage_account()
            else:
                print("wrong input\n")

    def add_images(self):
        while(True):
            i = input("Press i for single upload, b for bulk upload: ")
            if i == 'i':
                filename = helper.get_valid_filename()
                folder = self.select_folder()
                j = input("Press p if you want the image public. Press any other key to make it private. ")
                
                self.upload_one_file(filename, folder, j == 'p')
                return 
            elif i == 'b':
                print("Place images to be uploaded in the upload folder.\n")
                files = os.listdir("upload/")
                folder = self.select_folder()
                j = input("Press p if you want the image public. Press any other key to make it private. ")

                for filename in files:
                    self.upload_one_file(filename, folder, j == 'p')
                return 
            else:
                print("wrong input\n")
        return None

    def delete_images(self):
        while(True):
            image = self.repo.get_image_by_name(helper.get_valid_filename())
            if image != None:
                self.repo.soft_delete_by_id(image[0])
                return
            else:
                "Print existing filename"
                continue

    def see_inventory(self):
        print("ID\t\tName\t\t\t\tPublic")
        for image in self.repo.get_images_by_user(self.id):
            print(str(image[0]) + "\t\t" + str(image[2]) + "\t\t" + str(image[5]))

    def manage_account(self):
        return None

    def select_folder(self):
        print("Which folder would you like this image in?: ")

        folders = self.repo.get_folders(self.id)
        for ind in range(len(folders)):
            print(str(ind) + ". " + folders[ind][2])
        
        while(True):
            i = int(input("Input the folder number: "))
            if i < 0 or i >= len(folders):
                print("Please input valid folder number")
            else:
                return folders[i]

    def upload_one_file(self, filename, folder, is_public):
        shutil.move("upload/" + filename, "repo/" + str(self.id) + "/" + folder[2] + "/")
        if self.repo.add_image(self.id, filename, folder[0], is_public):
            print("Successfully added.")
        else:
            print("Upload failed")