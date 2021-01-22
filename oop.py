import uuid, hashlib, mysql.connector, os



class DBCon():
    def __init__(self):
        self.host = '127.0.0.1'
        self.user = 'root'
        self.password = os.environ.get('dbPassword')
        self.dataBase = 'DBUsers'
        self.cur = None
        self.con = None

    def getCon(self):
        self.con = mysql.connector.connect(
        host = self.host,
        user = self.user,
        password =f"{self.password}",
        database= self.dataBase
        )

        self.cur = self.con.cursor()

    def closeDB(self):
        self.con.close()


    def showDatabases(self):
        self.cur.execute('SHOW DATABASES')
        dbs = self.cur.fetchall()
        print(dbs)
# dataB.showDatabases()

class DatabaseActions():
    def __init__(self):
        self.dbCur = dataB.cur
        self.dbCon = dataB.con


    def addToDb(self, username, HashedPassword, email):
        try:
            sql = f"""INSERT INTO `users` VALUES ('{username}', '{HashedPassword}','{email}')"""
            self.dbCur.execute(sql)
            self.commit1()
        except:
            print('Did not insert')
        else:
            print('All done :) ')


    def commit1(self):
        self.dbCon.commit()

    def execute(self, sqlCommand):
        self.dbCur.execute(sqlCommand)

class HashingPasswords():

    def hashPassword(self, password):
        salt = uuid.uuid4().hex
        hashedPassword = hashlib.sha256(salt.encode()+password.encode()).hexdigest()+":"+salt

        return hashedPassword


    def verifyhash(self, userpass, storedpass):   #Verifies the hash
        try:   #Prevents crash in instance of invalid stored hash
            password,salt=storedpass.split(":")
        except:
            pass
        else:
            data = []
            data.append(password)
            data.append(hashlib.sha256(salt.encode()+userpass.encode()).hexdigest())
        
        return data[0]==data[1]

class UserActions():
    def __init__(self):
        self.exitP = 0

    def login(self):
        valid = False
        loggedIn = False
        while not valid:
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            if username and password:
                valid = True
                print('Validated \n')
        while not loggedIn:
            sql = f"""SELECT password FROM users WHERE username='{username}'"""
            dbActions.execute(sql)
            items = dbActions.dbCur.fetchone()
            print(items)
            if items:
                dbPassword = items[0]
                match = hasher.verifyhash(password, dbPassword)
                if match:
                    loggedIn = True
                    print('You are now logged in. ')
                else:
                    print('The password doesnt match')
            else:
                print('Sorry, I could not find you ')




    def register(self):
        valid = False
        while not valid:
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            email = input("Enter an email:")
            if username and password and email:
                valid = True

        hashedUserpass = hasher.hashPassword(password) 
        dbActions.addToDb(username, hashedUserpass, email)
        ##not yet checked if already exisits

    def exit(self):
        print('Goodbye!')
        self.exitP = 1

class Program():

    def main(self):
    
        userA.exitP = 0
        while not userA.exitP:
            try:
                choice = int(input('Welcome to the program. Choose form the following: \n1.Register \n2.Login \n3.Exit \n'))
            except:
                print("Please enter either 1, 2 or 3 to indicate your choice ")
            else:
                if choice == 1:
                    userA.register()
                elif choice == 2:
                    userA.login()
                elif choice == 3:
                    userA.exit()
                else:
                    print('Please type 1, 2 or 3 to indicate your choice: ')




dataB = DBCon()
dataB.getCon()
dbActions = DatabaseActions()
hasher = HashingPasswords()
userA = UserActions()
currentP = Program() 

currentP.main()
