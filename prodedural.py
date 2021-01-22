import uuid, hashlib, mysql.connector, os

SQLpassword = os.environ.get('dbPassword')
 
con = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password=f"{SQLpassword}",
  database="DBusers"
)

cur = con.cursor()

# cur.execute("SHOW DATABASES")
# db = cur.fetchall()
# print(db)

def getUserInfo():
    valid = False
    while not valid:
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        email = input("Enter an email:")
        if username and password and email:
            valid = True
        #regex username, password, email.
        # 
    return username, password, email 

def loginGetInfo():
        valid = False
        while not valid:
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            if username and password:
                valid = True
                print('Validated \n')
        #regex username, password, email.
        
        return username, password

def addToDb(username, HashedPassword, email):
    try:
        sql = f"""INSERT INTO `users` VALUES ('{username}', '{HashedPassword}','{email}')"""
        cur.execute(sql)
        con.commit()
    except:
        print('Did not insert')
    else:
        print('All done :) ')

def hashPassword(password):
    salt = uuid.uuid4().hex
    hashedPassword = hashlib.sha256(salt.encode()+password.encode()).hexdigest()+":"+salt

    return hashedPassword


#sha256 is a common hashing algo, that will always produce the same hash for the same input. 

#salt - a randomly generated value, that uses UUID4 method. -> .hex is used to convert the output of UUID4 into a hexidecimal value

#user inputs a password of: pass1234. I then add the salt to this, create a new value and place that into the hashing algorithm. 

#the hashed output (pass1234+salt) is stored in the DB with the original salt. hashedPass+':'+salt 

#nbow someone tries to log in. I get a passwordA = 'pass1234'.   passwordA+salt -> hashingAlgo




def verifyhash(userpass, storedpass):   #Verifies the hash
    try:   #Prevents crash in instance of invalid stored hash
        password,salt=storedpass.split(":")
    except:
        pass
    else:
        found = False
        dbPassword = password
        userGuessPassword = hashlib.sha256(salt.encode()+userpass.encode()).hexdigest()
        if dbPassword == userGuessPassword:
            found = True

    return found



def main():
    x = 0
    while not x:
        try:
            choice = int(input('Welcome to the program. Choose form the following: \n1.Register \n2.Login 3.Exit '))
        except:
            print("Please enter either 1, 2 or 3 to indicate your choice ")
        else:
            if choice == 1:
                username, password, email = getUserInfo()
                hashedUserpass = hashPassword(password)
                addToDb(username, hashedUserpass, email) #add to database
            elif choice == 2:
                loggedIn = False
                username, password = loginGetInfo()
                while not loggedIn:
                        #get username and password
                        sql = f"""SELECT password FROM users WHERE username='{username}'"""
                        cur.execute(sql)
                        items = cur.fetchone()
                        print(items)
                        if items:
                            dbPassword = items[0]
                            match = verifyhash(password, dbPassword)
                            if match:
                                loggedIn = True
                                print('You are now logged in. ')
                            else:
                                print('The password doesnt match')
                        else:
                            print('Sorry, I could not find you ')

            elif choice == 3:
                print('Goodbye!')
                x = 1
            else:
                print('Please type 1, 2 or 3 to indicate your choice: ')


while(1):
    main()
        
# sql = f"""SELECT username, password FROM users WHERE username='shaff' and password='pass'"""
# cur.execute(sql)
# items = cur.fetchone()
# print(items)


# hashedUserpass = hashPassword(password)
# otherHash = hashPassword('password') #already stored in db on sign up
# print(verifyhash('password', otherHash))
# print(hashedUserpass)
