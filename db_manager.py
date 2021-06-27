import mysql.connector as mysql
db = mysql.connect(host="localhost",user="root",password="password",database="project")
cursor = db.cursor()

def dbcheckuserpass(username,password):
    sql = "select username from user where username = %s and password= %s;"
    val =(username,password)
    cursor.execute(sql,val)
    myresult = cursor.fetchall()
    if (username,) in myresult:
        return 'user exists'
    else:
        return 'user dont exists'

def dbcheckuser(username,password):
    sql = "select username from user where username = %s;"
    val =(username,)
    cursor.execute(sql,val)
    myresult = cursor.fetchall()
    if (username,) in myresult:
        return 'user exists'
        
    else:
        return 'user dont exists'
