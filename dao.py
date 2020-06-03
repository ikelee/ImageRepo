import pymysql
import pymysql.cursors
import os
import bcrypt
import string
import random

class repo:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.uid = None

        self.open_connection()

    def open_connection(self):
        try:
            self.connection = pymysql.connect(user='root', password='password',
                                    host='127.0.0.1',
                                    database='IMAGE_REPO')
            self.cursor = self.connection.cursor()

        except pymysql.InternalError as error:
            print("Connection Failed")
            print(error)

    def check_user_exists(self, username):
        select = ("SELECT username from `user_credential` where username=%s")
        self.cursor.execute(select, (username))
        if self.cursor.fetchone() != None:
            return True
        else:
            return False

        
    def create_new_user(self, username, password):
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(password.encode("utf-8"), salt)

        insert = ("INSERT INTO `user_credential` (username, password_hash) VALUES(%s, %s)")
        try:
            self.cursor.execute(insert, (username, hash))
            self.cursor.execute("COMMIT")
        except pymysql.IntegrityError:
            print("Error. Username must be unique")
            return False
    
        return True

    def create_new_user_info(self, username, data):
        select = ("select id from user_credential where username=%s")
        self.cursor.execute(select, (username))
        id = self.cursor.fetchone()[0]

        insert = ("INSERT INTO `user_info` (id, `name`, age, birthday) VALUES(%s, %s, %s, %s)")
        os.makedirs('repo/' + str(id) + "/general")
        try:
            self.cursor.execute(insert, (id, data[0], data[1], str(data[2]) + '-' + str(data[4]) + '-' + str(data[3])))
            self.cursor.execute("INSERT INTO folder (user_id, `name`) VALUES(" + str(id) + ", 'general')")
            self.cursor.execute("COMMIT")
        except pymysql.IntegrityError:
            print("Error. Username must be unique")
            return False
    
        return True
    
    def login(self, username, password):
        select = ("SELECT id, password_hash from `user_credential` where username=%s")
        self.cursor.execute(select, (username))
        id, pw_hash = self.cursor.fetchone()
        if bcrypt.checkpw(password.encode("UTF-8"), pw_hash.encode("UTF-8")):
            return id
        else:
            return False

    def get_user_info(self, user_id):
        #TODO: secure with JWT
        select = ("SELECT * from `user_info` where `id`=%s")

        self.cursor.execute(select, user_id)
        return self.cursor.fetchone()

    def get_folders(self, user_id):
        #TODO: secure with JWT
        select = ("SELECT * from `folder` where `user_id`=" + str(user_id) + "")
        self.cursor.execute(select)

        return self.cursor.fetchall()

    def add_image(self, id, name, folder_id, is_public):
        #TODO: secure with JWT
        insert = ("INSERT INTO `image` (`user_id`, `name`, folder_id, public) VALUES(%s, %s, %s, %s)")
        try:
            self.cursor.execute(insert, (id, name, folder_id, is_public))
            self.cursor.execute("COMMIT")
        except pymysql.IntegrityError:
            print("Insert failed.")
            return False
        return True

    def get_images_by_user(self, user_id):
        #TODO: secure with JWT
        select = ("SELECT * from `image` where `user_id`=%s and `deleted` is false")

        self.cursor.execute(select, user_id)
        return self.cursor.fetchall()

    def get_image_by_name(self, name):
        #TODO: secure with JWT
        select = ("SELECT * from `image` where `name`=%s and `deleted` is false")

        self.cursor.execute(select, name)
        return self.cursor.fetchone()

    def soft_delete_by_id(self, id):
        #TODO: secure with JWT
        update = ("UPDATE `image` SET `deleted`=1 where `id`=%s and `deleted` is false")

        self.cursor.execute(update, id)
        self.cursor.execute("COMMIT")
        return self.cursor.fetchone()

    def get_public_images(self):
        select = ("SELECT * from `image` where `deleted` is false and `public` is true")
        self.cursor.execute(select)
        return self.cursor.fetchall()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
