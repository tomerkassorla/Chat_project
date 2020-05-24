import pickle
import database
import threading
import sqlite3


class SyncDatabase:
    def __init__(self):
        self.database = database.Database("database.p")
        self.semaphore = threading.Semaphore(10)
        self.lock = threading.Lock()

    def read(self):
        self.lock.acquire()
        print("wait for sem")
        self.semaphore.acquire()
        print("sem now")
        self.lock.release()
        print(self.database.read())
        self.semaphore.release()

    def write(self, key, value):
        print("wait for lock")
        self.lock.acquire()
        print("lock now")
        self.database.write(key, value)
        self.lock.release()


conn = sqlite3.connect("blitch.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE name_lastn
                    (name TEXT,last_name TEXT''')
my_name_lastn = [("Tomer", "kassorla")]
cursor.executemany("INSERT INTO name_lastn VALUES (?,?)", my_name_lastn)
syncdatabase = SyncDatabase()
for i in range(5):
    t = threading.Thread(target=syncdatabase.write, args=("first name" + str(i), "Tomer"))
    t.start()
for i in range(13):
    t = threading.Thread(target=syncdatabase.read)
    t.start()

# d.write("grade", "yoodbeit")
db_dict = {"first name": "Tomer", "last name": "Kassorla"}
