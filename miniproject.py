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

def offerride (email,name):
    global connecton, cursor
    default = "null"
    
    print("Ride offers")
    price   = input("Price per seat:")
    date    = input("Date:")
    seats   = input("Number of seats:")
    lugDesc = input("Lugage description:")
    driver  = email
    
    #CAR NUMBER : members should have an option to add a car number 
    carOpt = input("would you like to add a car number? (Yes/no):")
    carOpt = carOpt.lower().replace(" ", "")
    
    
    
    #user chooses to enter car number 
    if carOpt == "yes":
        carNo = input("Enter car number :")
        #make sure car number belongs to the member 
        cursor.execute("select owner from cars where cno = ? ;",(carNo,))
        result  = cursor.fetchone()
        for row in result :
            member = row 
        if member == driver:
            driver = member 
        
        #i dont know what to do in this case , should I call the fuction again?
        
        else :
            print("Sorry there the Email you have entered does not match the  car number. You can't take someones car")
            offerride()
    
    
    else :
        #set car number to null if the user enters no
        carNo = default 
        
        
        
    #ENROUTE : members should have an option to enter enroute locations 
    #option for adding enroute locations 
    enrouteOpt = input("Do you have enroute locations? (yes/no)")
    enrouteOpt = enrouteOpt.lower().replace(" ", "")
    
    # user wants to add enroute locations 
    if enrouteOpt == "yes":
        enroute  = map(str, input("Enter location code(s) (separate lcode with commas) :").split(','))
        
        #put lcode into enroute table in the data base
        for item in i:
            enroute = enroute.lower()
            print(item)        
     
    # to not add anythoing to the enroute table if the user does not enter any set of enroute locations
    else :
        pass
               
    
    
     
    
    
    #KEYWORD SECTION FOR locations(source , destination, enroute )
    #user enters a keyword option
    keywordOpt= input("keyword help ? (yes or no)")
    keywordOpt = keywordOpt.lower().replace(" ", "")
     
    
    #if keywordOpt is yes
    if keywordOpt == "yes":
        keyword = input("Enter a keyword for locatio-code/city/province/adderess")
        kword = "%"+keyword+ "%"
        
        #sql query to select rows that match the keyword from locations table in the database , limit the result to five 
        cursor.execute("select * from locations where keyword = lcode or city like ? or province like ? or address like ? LIMIT 5; ",(keyword,))
        #sql statement returns a list of location(s)
        location = cursor. fetchall()
        
        #let the member select a location from a list of locatons 
        #once you get one row, assign values to the source , destination , enroute 
        
        #src  = input("Starting location:")
        #dest = input("Destination")
        
        
        dest    = input("Final destination:")
    
    
   
    
    
    
    #uniquely assign a ride number 
    cursor.execute("SELECT MAX(rno) FROM rides ORDER BY rno DESC LIMIT 1;");
    rno = cursor. fetchone()
    print(rno)
    rideno = rno[0] + 1 
    
    #inserat all of the values into the table rides in the database 
    cursor.execute("INSERT INTO rides VALUES(?,?,?,?,?,?,?,?);", (rideno, price, date, seats,lugDesc, src, dest, driver, cno))
    
    
                
    #keyword should be lcode 
    #if key word is no lcode , it should return all locations that hav the keyword as a substring in city, province or address fields
    #not more than five matching locaions
    #ensure that the car number belongs to the member 
    
    
    connection.commit()
    return

def searchride ():
    print("searchrides")
    keyword = tuple(list(input("Please enter a keyword : ").split()))
    
    
    for i in keyword:
        check = "%" + i + "%"
        
        isless = True
        #while(isless):
        print(i)
        count = 0
        cursor.execute("SELECT  DISTINCT r.rno , r.price , r.rdate , r.seats , r.lugDesc , r.src, r.dst, r.driver, r.cno FROM rides r , locations l , enroute e WHERE ( r.src = l.lcode OR  r.dst = l.lcode  OR  (e.lcode = l.lcode AND e.rno = r.rno )) AND (l.city Like ?  OR  l.prov Like ? OR  l.address like ?);",(check,check,check))
        rides = cursor.fetchall()
        for j in rides:
            count = count + 1 
            print(rides)
            #if(count == 5):
                #isless = False
                #con = input("Would you like to view more")
                #if (con == "yes"):
                    #count = 0
                    #isless = True
                
                        
                    
    
    return 

def bookcancelbookings ():
    print("book/cancelbookings")
    
    return 
def postrides (email,name):
    global connection, cursor, getuser, getemail
    rdate = input("Please provide a date for the ride(yyyy-mm-dd): ") 
    p_lcode = input("Please provide a pick up location code: ") 
    d_lcode = input("Please provide a drop off location code: ")
    price = input("Please enter the amount you are willing to pay per seat: ")
    
    #check date input
    try:
        datetime.datetime.strptime(rdate, "%Y-%m-%d")
    except ValueError:
        print("Enter a valid date format!!")
        postrides(email,name)
    
    #check that lcodes exist in table      
    # The request rid is set by your system to a unique number and not already in the table   
    cursor.execute("SELECT lcode FROM locations WHERE lcode=? ;",(p_lcode,))
    pickup = cursor.fetchall()
    cursor.execute("SELECT lcode FROM locations WHERE lcode=? ;",(d_lcode,))
    dropoff = cursor.fetchall()        
    if len(pickup) == 0:
        print("invalid pick up location")
    elif len(dropoff) == 0:
            print("invalid drop off location")  
    else:
        cursor.execute("SELECT rid FROM requests")
        rides = cursor.fetchall()
        rid = max(rides)
        rid = rid[0] + 1
        info = (rid, email, rdate, p_lcode, d_lcode, price,)
        cursor.execute("INSERT INTO requests (rid, email, rdate, pickup, dropoff, amount) VALUES(?,?,?,?,?,?)", (rid, email, rdate, p_lcode, d_lcode, price)) #not insertiingg       
        print("Your ride has been requested!!!")
        
    dec = input("Would you like to request another ride (yes/no): ")
    dec = dec.lower().replace(" ", "")
    if dec == "yes":  
        postrides(email, name)
        
    else:
        dec == "no"
        menu(email, name)

           
    connection.commit(email, name)
    return
def sdrequests (email,name):
    global connection, cursor
    action = input("Type all requests to view  all your requests  and city requests to view requests from a specific city or location and MENU to return to Menu: ")
    
    if(action.lower().replace(" ", "") == "allrequests"):
        # dosomething 
        print("your requests")
        cursor.execute("SELECT * FROM requests WHERE email=? ;",(email,))
        messages=cursor.fetchall() 
        for i in messages:
            print(i)
        delete = input("Would you like to delete any of your rides ?")
        if(delete.lower().replace(" ","") == "yes"):
            rid =  tuple(list(input("Please list the rid's of the requests which you would like to delete seperated by spaces and press enter when u are done")))
            for i in rid:
                cursor.execute("DELETE FROM requests WHERE rid  = ? AND email= ?;",(i,email))
        sdrequests(email,name)
    elif(action.lower().replace(" ", "") == "cityrequests"):
        loc=input("Please enter your location code or city for the requests")
        location = "%"+loc+"%"
        cursor.execute("SELECT * FROM requests r ,locations l  WHERE  (r.pickup = l.lcode OR r.dropoff = l.lcode) AND (l.lcode like ? OR l.city like ? ) ;",(location,location))
        messages=cursor.fetchall() 
        for i in messages:
            print(i)     
        delete = input("Would you like to message any of the posters ?")
        if(delete.lower().replace(" ","") == "yes"):
            rid =  input("Enter the rid of the ride you would to talk about?")
            content = input("What would you like to tell the poster;")
            rno = input ("What is the rno?:")
            cursor.execute("SELECT email,rdate FROM requests WHERE rid =?;",(rid,))
            stuff = cursor.fetchone()
            poster = stuff[0]
            date = stuff[1]
            
            try:
                cursor.execute("INSERT INTO inbox VALUES(?,?,?,?,?,?)", (email,date,poster,content,rno,'n'))
            except sqlite3.IntegrityError:
                print("An error occurred. Please try again later.Check that you are sending to a registered member")                  
            
        sdrequests(email,name)
    elif(action.lower().replace(" ", "") == "MENU"):
        menu()  
    else:
        sdrequests(email,name)
   
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
    print("Press 5 to search/delete ride requests.")
    print("Press 6 to read/send/ reply messages.")
    print("Press 7 to logout.")
    action =input()
    action = int(action.lower().replace(" ", ""))
    if action == 1: 
        offerride(email,name)
    elif action == 2:
        searchride()
    elif action == 3:
        bookcancelbookings()
    elif action == 4:
        postrides(email,name)
    elif action == 5:
        sdrequests(email,name)
    elif action == 6:
        sendmessage(email,name)  
    elif action == 7:
        logout()    
       
    else:
        print("Sorry I didnt get that... I would repeat the menu again." )
        menu(email,name)
        
        
        
    connection.commit()
    return
    
    
def bookcancelbookings (email, name):
    global connection, cursor
    
    #listing of all bookings
    reply = input("Would you like to see the bookings?(yes/ no)")
    reply = reply.lower().replace(" ", "")
    if reply == "yes":
        cursor.execute("SELECT DISTINCT * FROM rides r, bookings b WHERE r.rno = b.rno AND r.driver = ? ;",(email,))
        #nums=cursor.fetchall()
        #cursor.execute("SELECT * FROM bookings WHERE rno = ? ;",(nums,))
        rides=cursor.fetchall()        
        #getting all the bookings 
        
        #printing all the bookings 
        if len(rides) == 0: 
            print("You have no rides at the moment")
            option = input("return to menu(yes/no)")
            option = option.lower().replace(" ", "")
            if option == "yes": 
                menu(email, name)
            else:
                logout()
            #let them decide what they wanna do
            #menu(email,name)  # ########
        else: 
            for j in rides: 
                print(j) 
            rno = input("Enter the ride number(rno) of the booking that you would like to cancel/press enter if you do not want to cancel any rides: ")
            if rno == "":
                print("You are not cancelling any rides")
                ans = input("Would you like to book other rides (yes/no)")
                if ans == "yes":  
                    book()
                    
                else:
                    ans == "no"
                    menu(email, name)                
                #give them the potion of booking other members or exiting the bookings
            else:    
                receiving = cursor.execute("SELECT email FROM bookings WHERE rno = ? ;",(rno,))
                cursor.execute("DELETE FROM bookings WHERE rno = ?;",(rno,))# ######
                print("The following booking has been successfully cancelled " + str(rno))
                cursor.execute("SELECT * FROM bookings WHERE rno = ? ;",(rno,))
                rides2=cursor.fetchall()                
                if len(rides2) == 0: 
                    print("You have no bookings remaining")
                #ask them if they want to do other things
                else:
                    print("You have the following remaining bookings:")
                    cursor.execute("SELECT * FROM rides WHERE email = ? ;",(email,))
                    #getting all the remaining bookings 
                    new_bookings=cursor.fetchall()                    
                    for i in new_bookings:
                        print(i)
                content = ("The following ride was cancelled " + str(rno))
                cursor.execute("SELECT datetime('now')")
                msg_t_st = cursor.fetchone()
                msg = msg_t_st[0]
                #send message to the customer whose booking has been cancelled
                cursor.execute("INSERT INTO inbox VALUES(?,?,?,?,?,?)", (receiving, msg, email, content, rno, 'n'))
                
    elif reply == "no":
        menu(email, name) 
             
               
    connection.commit()
    #cursor.close()
    return    
def book():
    print("Enter the details of the member you would like to book on a ride")
    email = input("Enter the email of the user you would like to book ")
    rno = input("Enter the ride number on which you want to book the user: ")
    cost = input("Enter the cost of the ride")
    seats = input("Enter the number of seats you are booking for the user:")
    #pickup = input("Enter the 
    
    
    connection.commit()
    #cursor.close()
    return     
def postrides (email,name):
    global connection, cursor, getuser, getemail
    rdate = input("Please provide a date for the ride(yyyy-mm-dd): ") 
    p_lcode = input("Please provide a pick up location code: ") 
    d_lcode = input("Please provide a drop off location code: ")
    price = input("Please enter the amount you are willing to pay per seat: ")
    
    #check date input
    try:
        datetime.datetime.strptime(rdate, "%Y-%m-%d")
    except ValueError:
        print("Enter a valid date format!!")
        postrides(email,name)
    
    #check that lcodes exist in table      
    # The request rid is set by your system to a unique number and not already in the table   
    cursor.execute("SELECT lcode FROM locations WHERE lcode=? ;",(p_lcode,))
    pickup = cursor.fetchall()
    cursor.execute("SELECT lcode FROM locations WHERE lcode=? ;",(d_lcode,))
    dropoff = cursor.fetchall()        
    if len(pickup) == 0:
        print("invalid pick up location")
    elif len(dropoff) == 0:
            print("invalid drop off location")  
    else:
        cursor.execute("SELECT rid FROM requests")
        rides = cursor.fetchall()
        rid = max(rides)
        rid = rid[0] + 1
        info = (rid, email, rdate, p_lcode, d_lcode, price,)
        cursor.execute("INSERT INTO requests VALUES(?,?,?,?,?,?)", (rid, email, rdate, p_lcode, d_lcode, price)) 
        print("Your ride has been requested!!!")
        
    dec = input("Would you like to request another ride (yes/no): ")
    dec = dec.lower().replace(" ", "")
    if dec == "yes":  
        postrides(email, name)
        
    else:
        dec == "no"
        menu(email, name)

           
    connection.commit()
    #cursor.close()
    #connection.close()
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
    cursor.execute("SELECT email FROM members WHERE email=? ;",(email,))
    emailvalid = cursor.fetchall()
    if (emailvalid==[]):
        sign = input("Sorry you do not seem to be a signed up user. Would you like to sign up ? Y/N")
        if(sign.upper() == "Y"):
            signup()
        elif(signup.upper() == "N"):
            what = input(" LOGIN to try again")
            if(what == "LOGIN" ):         
                login()
            else:
                print("Sorry I didn't understand your input")
                logout()
        else:
            print("Sorry I didn't understand your input")
            logout()    
        
        
        
        
    else:  
        password = encrypt(input("Please enter a password: "))
        cursor = connection.cursor()
        cursor.execute("SELECT pwd FROM members WHERE email=? ;",(email,))
        rows=cursor.fetchall()
        goodpass = rows[0][0]
        cursor.execute("SELECT name FROM members WHERE email=? ;",(email,))
        name =cursor.fetchone()
        if(encrypt(goodpass.replace(" ", "")) == password):
            menu(email,name[0])
            
        else:
            print("Wrong Password")
            login()           
            
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
