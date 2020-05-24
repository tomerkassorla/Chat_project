import sqlite3


class Database:
    """the class that handle the database - gives functions to write, to read
    and to check what we have in the database"""
    def __init__(self, file_name):
        self.file_name = file_name
        self.conn = None
        self.cursor = None

    def create_connection(self):
        """create connection"""
        self.conn = sqlite3.connect(self.file_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def check_if_username_in_database(self, username):
        """function that return false if username in database"""
        read = self.get_usernames()
        for i in read:
            if i[0] == username:
                return False
        return True

    def check_if_username_password_in_database(self,
                                               list_username_password):
        """check if username and password in database"""
        read = self.read()
        for i in read:
            if i[0] == list_username_password[0] and i[1] == list_username_password[1]:
                return True
        return False

    def get_usernames(self):
        """get all the usernames in database"""
        self.cursor.execute("SELECT DISTINCT name FROM users")
        read = self.cursor.fetchall()
        return read

    def create_table(self, create_table_sql):
        """create table"""
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    def write(self, list_name_password):
        """write to the database the name and the password of the client that register"""
        self.cursor.execute("INSERT INTO users VALUES (?,?)", list_name_password)
        self.conn.commit()

    def read(self):
        """read all the information in the database"""
        self.cursor.execute("SELECT * FROM users")
        read = self.cursor.fetchall()
        return read
