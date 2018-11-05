import sqlite3
import time
import hashlib
import sys
from datetime import datetime
from getpass import getpass 

connection = None
cursor     = None
getuser    = None 


def encrypt(password):
    alg = hashlib.sha256()
    alg.update(password.encode("utf-8"))
    return alg.hexdigest()

def connect():
    global connection, cursor
    
    connection = sqlite3.connect(sys.argv[1] )
    if (connection):
        
        cursor = connection.cursor()
        cursor.execute(' PRAGMA foreign_keys=ON; ')
        connection.commit()
    else:
        print("not connected")
        
    return

def keyword():
    global connecton, cursor
    
    keywordOpt= input("keyword help ? (yes or no)")
    keywordOpt = keywordOpt.lower().replace(" ", "")
     
    #if keywordOpt is yes
    if keywordOpt == "yes":
        kword = input("Enter a keyword (location-code/city/province/adderess):")
        keyword = '%'+kword+'%'
       
        #sql query to select rows that match the keyword from locations table in the database 
        cursor.execute("select * from locations where lcode = ? or city like ? or prov like ? or address like ?;",(kword,keyword,keyword,keyword,))
        
        #sql statement returns a list of location(s)
        location = cursor.fetchall()
        
        #display 5 results for the keyword one at a time
        start = 0;
        end = 5;
        for idx, l in enumerate(location):
            if((idx >= start) and (idx < end)):
                print(l)  
        start = 5
        end = len(location)
            
        if(len(location) > 5):
            see_more_result = input("Would you like to see more results ? (yes or no) :")
            if see_more_result == "yes":
                for idx, l in enumerate(location):
                    if((idx > start) and (idx < end)):
                        print(l)                
            
        #let the member select a location from a list of locatons 
        select_lcode = input("Select a location by typing the lcode:")
        return select_lcode
    
def offerride(email, name):
    global connecton, cursor
    default = None
    now = datetime.now()
    
    print("Ride offers")
    
    #PRICE
    #check price format 
    while True :
        price   = input("Price per seat:") 
        if(price.isdigit())and (int(price)>=0):
            break
        else :
            print("please enter a positive number for price")
    
    #DATE
    #check date format       
    while True:
        date    = input("Date(yyyy-mm-dd):")
        try:
            year,month, day =date.split('-') 
        except:
            print("Enter a valid date")
        
        try:
            year,month, day =date.split('-')
            datetime(int(year), int(month), int(day))
            break
        except ValueError:
            print("Invalid date")
            
    #SEATS
    #check seat format
    while True:
        seats   = input("Number of seats:") 
        if(seats.isdigit())and (int(seats)>=0):
            break
        else :
            print("please enter a positive number for seats")        
     
    #LUGGAGE DESCRIPTION   
    #enter luggage description
    lugDesc = input("Lugage description:") or None 
    
    #DRIVER
    #same as login email
    driver  = email
    
    #CAR NUMBER 
    #members should have an option to add a car number 
    carOpt = input("would you like to add a car number? (Yes/no):")
    carOpt = carOpt.lower().replace(" ", "")
    #user chooses to enter car number 
    if carOpt == "yes":
        carNo = input("Enter car number :")
        
        #make sure car number belongs to the member 
        cursor.execute("select owner from cars where cno = ?; ",(carNo))
        result  = cursor.fetchone()
        if result == None:
            print("The Email you have entered does not match the  car number ")
            offerride(email,name)
        else :
            for row in result:
                member = row
        
            if member == driver:
                driver = member 
        
            else :
                print("The Email you have entered does not match the  car number ")
                offerride(email, name )
                
    #set car number to null if the user enters no
    else :
        carNo = default 
        
    #RIDE NUMBER  
    #uniquely assign a ride number 
    cursor.execute("SELECT rno FROM rides ORDER BY rno DESC LIMIT 1;");
    rideNo = cursor.fetchone()
    if rideNo == None:
        rno = 1
    else :
        for item in rideNo:
            rno = item + 1
    
    #SOURCE 
    print("Enter starting location")
    src=keyword()
    
    #DESTINATION
    print("Enter destination")
    dest = keyword()
    
   
    #ENROUTE 
    enrouteOpt = input("Do you have enroute locations? (yes/no)")
    enrouteOpt = enrouteOpt.lower().replace(" ", "")
    
    # user wants to add enroute locations 
    if enrouteOpt == "yes":
        #call the keyword function
        
        enroute  = map(str, input("Enter location code(s) (separate lcode with commas) :").split(','))
        
        #put lcode into enroute table in the data base
        for item in enroute:
            enroute = item.lower()
            cursor.execute("INSERT INTO enroute (rno, lcode) Values (?, ?)", (rno,enroute))
    # to not add anythoing to the enroute table if the user does not enter any set of enroute locations
    else :
        pass
               
    
    #INSERT
    #insert all of the values into the table rides in the database 
    cursor.execute("INSERT INTO rides VALUES(?,?,?,?,?,?,?,?,?);", (rno, price, date, seats,lugDesc, src, dest, driver, carNo))
    
    connection.commit()
    return 


def searchride():
    global connection, cursor 
    
    print("searchride")
    
    #ask the user to enter a maximum of three inputs 
    keywords = map(str, input("Enter keywords separated by commas (3 maximum) :").split(','))
    
    
    # limit to 3 keywords 
    all_rides =[];
    for i in keywords:
        
        keyword = '%'+i+'%'
        cursor.execute("select * from locations where lcode = ? or city like ? or prov like ? or address like ?;",(i,keyword,keyword,keyword,))   
        location = cursor.fetchall()
        
        for a_location in location:
            location_lcode = a_location[0]
            #while(isless):
            #Stop it from printing duplicates
            cursor.execute("SELECT  DISTINCT r.rno , r.price , r.rdate , r.seats , r.lugDesc , r.src, r.dst, r.driver, r.cno FROM rides r , locations l WHERE ( r.src = ? OR  r.dst = ? );",(location_lcode,location_lcode))
            #do the limit stuff
            
            rides = cursor.fetchall()
            
            for j in rides:
                if j not in all_rides:
                    all_rides.append(j)
    #print(all_rides)
    print("rno      |price  |date       |seats|lugdesc  |src|dst|driver        |cno|")
    for i in all_rides:
        print(str(i[0]) +"      " + "|" + str(i[1])+"     " + "|" + str(i[2]) +" "+ "|" + str(i[3])+"    " + "|" + str(i[4]) + "|" + str(i[5]) + "|" + str(i[6]) + "|" + str(i[7]) +" "+ "|" + str(i[8]))
           
                   
    connection.commit()
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
        #limit both to 5 
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
        #limit both to 5 options to view
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
        bookcancelbookings(email, name)
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
        #list available seats
        available = "SELECT DISTINCT r.rno,(r.seats - sum(b.seats)) FROM rides r, bookings b WHERE r.rno = b.rno AND r.driver = ? GROUP BY r.rno;"
        cursor.execute(available,(email,))
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
            if len(rides) > 5: 
                i = 0
                while i<=5:
                    for j in rides: 
                        print(rides[i]) 
                    i +=1
                opt = input("If you would like to view more rides type ok otherwise type done ")
                opt = opt.lower().replace(" ", "")
                if opt == "ok": 
                    i = 6
                    while i<(len(rides)):
                        for j in rides: 
                            print(rides[i]) 
                        i +=1 
                else:
                    pass
                    
                        
            else:
                for j in rides: 
                        print(j) 
                
            rno = input("Enter the ride number(rno) of the booking that you would like to cancel/press enter if you do not want to cancel any rides: ")
            if rno == "":
                print("You are not cancelling any rides")
                ans = input("Would you like to book other rides (yes/no)")
                ans = ans.lower().replace(" ", "")
                if ans == "yes":  
                    book(email,name)
                    
                else:
                    ans == "no"
                    menu(email, name)                
                #give them the option of booking other members or exiting the bookings
            else: 
                #allow multiple deletes at once
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
                    cursor.execute("SELECT DISRINCT * FROM rides WHERE email = ? ;",(email,))
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
                ans2 = input("would you like to book people any any rides? (yes/no) ")
                ans2 = ans2.lower().replace(" ", "")
                if ans2 == "yes":  
                    book(email,name)
                else:
                    ans2 == "no"
                    menu(email, name)                    
                
    elif reply == "no":
        menu(email, name) 
             
               
    connection.commit()
    #cursor.close()
    return    

def book(email, name):
    print("Enter the details of the member you would like to book on a ride ")
    b_email = input("Enter the email of the user you would like to book ")
    rno = input("Select the ride number on which you want to book the user: ")
    cost = input("Enter the cost of the ride")
    seats = input("Enter the number of seats you are booking for the user: ")
    pickup = input("Enter the pickup location or location code: ")
    dropoff = input("Enter the dropoff location or location code: ")
    
    cursor.execute("SELECT bno FROM bookings")
    bnum = cursor.fetchall()
    bno = max(bnum)
    bno = bno[0] + 1    
    
    #booking message sent to the member
    cursor.execute("INSERT INTO bookings VALUES(?,?,?,?,?,?)", (bno, email, rno, cost, seats, pickup, dropoff))
    
    #warning if ride is being overbooked!! but allow if user confirms
    avail = "SELECT DISTINCT r.rno,(r.seats - sum(b.seats)) FROM rides r, bookings b WHERE r.rno = b.rno AND r.driver = ? GROUP BY r.rno;"
    cursor.execute(avail,(email,))
    availseats =cursor.fetchall()  
    i = 0
    while i < len(availseats):
        avail = availseats[i][i]
        i += 1
        if avail <=0:
            confirm = input("This ride is being overbooked would you like to continue(yes/no): ")
            confirm = confirm.lower().replace(" ", "")
            if confirm == "yes":
                print("your booking was successful!!!")
            else:
                action == "no"
                print("The booking is not confirmed")
                menu(email,name)
        else:
            print("your booking was successful!!!")
    
    cursor.execute("SELECT datetime('now')")
    msg_t_st1 = cursor.fetchone()
    msg1 = msg_t_st1[0]
    content1 = ("You have been booked on the following ride " + str(rno))
    #send message to the customer whose booking has been made
    cursor.execute("INSERT INTO inbox VALUES(?,?,?,?,?,?)", (b_email, msg1, email, content, rno, 'n'))
    ans2 = input("would you like to book people any any rides? (yes/no) ")
    if ans2 == "yes":  
        book()
        
    else:
        ans2 == "no"
        menu(email, name)         
    
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
    email = input("Enter a valid email:")
    cursor.execute("SELECT email FROM members WHERE email=? ;",(email,))
    emailvalid = cursor.fetchall()
    if (emailvalid==[]):
        sign = input("Sorry you do not seem to be a signed up user. Would you like to sign up ? Y/N")
        sign = sign.upper().replace(" ", "")
        if(sign == "Y"):
            signup()
        elif(sign == "N"):
            what = input(" LOGIN to try again")
            what = what.upper().replace(" ", "")
            if(what == "LOGIN" ):         
                login()
            else:
                print("Sorry I didn't understand your input")
                logout()
        else:
            print("Sorry I didn't understand your input")
            logout()    
      
    else:  
        password = encrypt(getpass("Please enter a password: "))
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
        print("Enter the following information")
        signup()
    elif action == "login":
        print("Enter your login details")
        login()
    else:
        print("Please enter a correct" )
        welcomepage()
        
        
    connection.commit()
    return



def main():
    global connection, cursor
    connect()    
    welcomepage()
    
    connection.commit()
    connection.close()
    return


if __name__ == "__main__":
    main()
