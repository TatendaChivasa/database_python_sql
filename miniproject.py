import sqlite3
import time
import hashlib

connection = None
cursor = None

def encrypt(password):
    alg = hashlib.sha256()
    alg.update(password.encode("utf-8"))
    return alg.hexdigest()

def connect(path):
    global connection, cursor
    
    connection = sqlite3.connect(path)
    if (connection):
        
        cursor = connection.cursor()
        #cursor.execute("select * from inbox;")
        #rows=cursor.fetchall()
        #print (rows)
        #cursor.execute(' PRAGMA foreign_keys=ON; ')
        connection.commit()
    else:
        print("not connected")
        
    return
def login():
    global connection, cursor
    email = input("Please enter a valid email:")
    password = encrypt(input("Please enter a password"))
    name = first_name +" "+ last_name
    
    if password != password2:
        print(" Password do not match")
        signup()
    else:
        user_data = (email, phone, name,password)
        cur.execute("SELECT * FROM membes WHERE email=? and pwd=? ;" (email, password))
    connection.commit()
    return
def signup():
    global connection, cursor
    email = input("Enter a valid email: ")
    phone = input("Enter enter a phone number: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    password = encrypt(input("Enter a password: "))
    password2 = encrypt(input("Re-enter your password: "))
    
    name = first_name +" "+ last_name
    
    if password != password2:
        print(" Password do not match")
        signup()
        
    else:
        user_data = (email, phone, name,password)
        try:
            cursor.execute("INSERT INTO members VALUES(?,?,?,?)", (email, phone, name,password))
        except sqlite3.IntegrityError:
            print("this email has already been used")
        
    connection.commit()
    return


def welcomepage():
    global connection, cursor
    action =input("Would you like to signup or login ?")
    action = action.lower().replace(" ", "")
    if action == "signup":
        print("yass")
        signup()
    elif action == "login":
        print("login")
        login()
    else:
        print("Please enter a correct" )
        welcomepage()
        
        
    connection.commit()
    return




def main():
    global connection, cursor
    
    path = "./Miniproject1/miniproject.db"
    connect(path)
    #drop_tables()
    #define_tables()
    #insert_data()
    welcomepage()
    #### your part ####
    # register all students in all courses.
    
    connection.commit()
    connection.close()
    return


if __name__ == "__main__":
    main()
