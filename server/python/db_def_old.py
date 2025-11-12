# Public lib
import mysql.connector



# User def
def creatUser(userName, gmail, password, role, enableUser):
    db = mysql.connector.connect(
        host='localhost',
        port="3306",
        user='server',
        password='password',
        database='db'
    )
    myCursor = db.cursor()
    myCursor.execute(f"INSERT INTO users (UserName, Gmail, PasswordHash, Roles, EnabledUser) VALUES('{userName}', '{gmail}', SHA2('{password}', 256), {role}, {enableUser});")
    db.commit()
    db.close()

def deletUser(userID):
    db = mysql.connector.connect(
        host='localhost',
        port="3306",
        user='server',
        password='password',
        database='db'
    )
    myCursor = db.cursor()
    myCursor.execute(f"DELETE FROM users WHERE ID = {userID};")
    db.commit()
    db.close()

def changeUserRole(userID, role):
    db = mysql.connector.connect(
        host='localhost',
        port="3306",
        user='server',
        password='password',
        database='db'
    )
    myCursor = db.cursor()
    myCursor.execute(f"UPDATE users SET Roles = {role} WHERE ID = {userID};")
    db.commit()
    db.close()

def changeUserPassword(userID, password):
    db = mysql.connector.connect(
        host='localhost',
        port="3306",
        user='server',
        password='password',
        database='db'
    )
    myCursor = db.cursor()
    myCursor.execute(f"UPDATE users SET PasswordHash = SHA2('{password}', 256) WHERE ID = {userID};")
    db.commit()
    db.close()

def changeUserName(userID, userName):
    db = mysql.connector.connect(
        host='localhost',
        port="3306",
        user='server',
        password='password',
        database='db'
    )
    myCursor = db.cursor()
    myCursor.execute(f"UPDATE users SET UserName = '{userName}' WHERE ID = {userID};")
    db.commit()
    db.close()

def changeUserGmail(userID, gmail):
    db = mysql.connector.connect(
        host='localhost',
        port="3306",
        user='server',
        password='password',
        database='db'
    )
    myCursor = db.cursor()
    myCursor.execute(f"UPDATE users SET Gmail = '{gmail}' WHERE ID = {userID};")
    db.commit()
    db.close()

def userActive(userID, enableUser):
    db = mysql.connector.connect(
        host='localhost',
        port="3306",
        user='server',
        password='password',
        database='db'
    )
    myCursor = db.cursor()
    myCursor.execute(f"UPDATE users SET EnabledUser = {enableUser} WHERE ID = {userID};")
    db.commit()
    db.close()



# Role def
def deletRole(roleID):
    db = mysql.connector.connect(
        host='localhost',
        port="3306",
        user='server',
        password='password',
        database='db'
    )
    myCursor = db.cursor()
    myCursor.execute(f"UPDATE users SET Roles = 2 WHERE Roles = {roleID};")
    myCursor.execute(f"DELETE FROM roles WHERE ID = {roleID};")
    myCursor.execute(f"DELETE FROM roles_actions WHERE roleID = {roleID};")
    db.commit()
    db.close()

def creatRole(roleName):
    db = mysql.connector.connect(
        host='localhost',
        port="3306",
        user='server',
        password='password',
        database='db'
    )
    myCursor = db.cursor()
    myCursor.execute(f"INSERT INTO roles (RoleName) VALUES('{roleName}');")
    db.commit()
    db.close()

def addActionsToRoles(roleID, actionID):
    db = mysql.connector.connect(
        host='localhost',
        port="3306",
        user='server',
        password='password',
        database='db'
    )
    myCursor = db.cursor()
    myCursor.execute(f"INSERT INTO roles_actions (roleID, actionID) VALUES('{roleID}', '{actionID}');")
    db.commit()
    db.close()



# Chat def
def createChat(chateName):
    db = mysql.connector.connect(
        host='localhost',
        port="3306",
        user='server',
        password='password',
        database='db'
    )
    myCursor = db.cursor()
    myCursor.execute(f"INSERT INTO chat (ChatName) VALUES('{chateName}');")
    db.commit()
    db.close()

def deletChat(chatID):
    db = mysql.connector.connect(
        host='localhost',
        port="3306",
        user='server',
        password='password',
        database='db'
    )
    myCursor = db.cursor()
    myCursor.execute(f"DELETE FROM msg WHERE Chat = {chatID};")
    myCursor.execute(f"DELETE FROM chat WHERE ID = {chatID};")
    db.commit()
    db.close()

def sendMSG(userID, chatID, msg):
    db = mysql.connector.connect(
        host='localhost',
        port="3306",
        user='server',
        password='password',
        database='db'
    )
    myCursor = db.cursor()
    myCursor.execute(f"INSERT INTO msg (Edited, User, Chat, DataInf, MSG) VALUES (FALSE, {userID}, {chatID}, now(), '{msg}';")
    db.commit()
    db.close()

def deletMSG(MSG_ID):
    db = mysql.connector.connect(
        host='localhost',
        port="3306",
        user='server',
        password='password',
        database='db'
    )
    myCursor = db.cursor()
    myCursor.execute(f"DELETE FROM msg WHERE ID = {MSG_ID};")
    db.commit()
    db.close()

def editMSG(MSG_ID, newMSG):
    db = mysql.connector.connect(
        host='localhost',
        port="3306",
        user='server',
        password='password',
        database='db'
    )
    myCursor = db.cursor()
    myCursor.execute(f"UPDATE msg SET Edited = TRUE WHERE ID = {MSG_ID};")
    myCursor.execute(f"UPDATE msg SET MSG = '{newMSG}' WHERE ID = {MSG_ID};")
    db.commit()
    db.close()

# Show data
# TODO