import mysql.connector

mydb = mysql.connector.connect(
    host="<<host>>",
    user="<<username>>",
    password="<<password>>"
)

cursor = mydb.cursor()

class CreateDatabase:
    def __init__(self):
        query = "create schema PasswordManager if not exists"
        cursor.execute(query)
        cursor.execute("use PasswordManager")

        create_table = """
            create table vault(
                SrNo int not null primary key, 
                SiteName varchar(50) not null,
                Password varchar(200) not null
            )
        """
        cursor.execute(create_table)
    
CreateDatabase()