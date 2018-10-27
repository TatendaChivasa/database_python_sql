import sqlite3
import time
import hashlib

connection = None
cursor = None
getuser = None 

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
        cursor.execute(' PRAGMA foreign_keys=ON; ')
        connection.commit()
    else:
        print("not connected")
        
    return

def sendmessage(email,name):
    global connection, cursor
    print("Your Messages:")
    seen = 'y'
    
    cursor.execute("SELECT * FROM inbox WHERE email=? ;",(email,))
    messages=cursor.fetchall() 
    for i in messages:
        cursor.execute("UPDATE inbox SET seen= ?  WHERE email=? ",(seen,email)) 
        print(i)
      
    numreplies = 0 
    sendmess = False
    inputstring = "Hello" + " "+ name + " " + "!!! " + "Would you like to reply  or send any messages ? I you would like to return to the menu type MENU"
    quest = input(inputstring)
    if (quest.upper() == "YES" ):
        sendmess = True
    elif(quest.upper() == "NO"):
        sendmess = False
    elif(quest.upper() == "MENU"):
        menu(email,name)
        sendmess = False    
    else:
        print("I am sorry I did not understand that :(.... Please type YES,NO or MENU")
        sendmessage(email,name)
    while(sendmess):
        sender = input("Type the persons email:")
        s = "What would you like to tell " + sender + " ?:"
        content = input(s)
        rno = input("what ride no ? :")
        cursor.execute("SELECT datetime('now')")
        d = cursor.fetchone()
        print(d)
        messagelist = (d,sender,content,rno)
        try:
            cursor.execute("INSERT INTO inbox VALUES(?,?,?,?,?,?)", (sender,d[0],email,content,rno,'n'))
        except sqlite3.IntegrityError:
            print("An error occurred. Please try again later.Check that you are sending to a registered member")        
        
        ask = input("Would you like to send or reply any other messages ? I you would like to return to the menu type MENU. ")
       
        if(ask.upper() == "NO"):
            sendmess = False
        elif(ask.upper() == "YES"):
            sendmess = True
        elif(ask.upper() == "MENU"):
            sendmess = False
            menu(email,name)       
        else:
            print("Sorry I don't understand your input. I'll assume that's a No.")
            sendmess = False
    connection.commit()
    return

def offerride ():
    print("offerrides")
    return 

def searchride ():
    print("searchrides")
    
    return 

def bookcancelbookings ():
    print("book/cancelbookings")
    
    return 
def postride ():
    print("post rides")
    return 
def deleterides ():
    print("delete rides")
    return 
def logout():
    print("Bye... Hope you come back")
    print("____________________________________________________________________________________________________________________________________________")
    welcomepage()
    return


def menu (email,name):
    welcomestring = "Hello " + name + " !!!" + "What would you like to do today ?"
    print(welcomestring)
    print("Press 1 to offer rides.")
    print("Press 2 to search rides.")
    print("Press 3 to book or cancel bookings.")
    print("Press 4 to post rides.")
    print("Press 5 to delete rides.")
    print("Press 6 to read/send/ reply messages.")
    print("Press 7 to logout.")
    action =input()
    action = int(action.lower().replace(" ", ""))
    if action == 1: 
        offerride()
    elif action == 2:
        searchride()
    elif action == 3:
        bookcancelbookings()
    elif action == 4:
        postrides()
    elif action == 5:
        deleterides()
    elif action == 6:
        sendmessage(email,name)  
    elif action == 7:
        logout()    
       
    else:
        print("Sorry I didnt get that... I would repeat the menu again." )
        menu(email,name)
        
        
        
    connection.commit()
    return
    
    
    



def signup():
    global connection,getemail
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
            print("The email or phone number has already been used")
        
    connection.commit()
    return

def login():
    global connection, cursor,getuser
    email = input("Please enter a valid email:")
    password = encrypt(input("Please enter a password: "))
    cursor = connection.cursor()
    cursor.execute("SELECT pwd FROM members WHERE email=? ;",(email,))
    rows=cursor.fetchall()
    goodpass = rows[0][0]
    cursor.execute("SELECT name FROM members WHERE email=? ;",(email,))
    name =cursor.fetchone()
    print(name[0])
    print(email)
    if(encrypt(goodpass.replace(" ", "")) == password):
        menu(email,name[0])
        
    else:
        print("Wrong Password")
    cursor.execute(' PRAGMA foreign_keys=ON; ')
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
    
    # register all students in all courses.
    
    connection.commit()
    connection.close()
    return


if __name__ == "__main__":
    main()
