import mysql.connector

mydb = mysql.connector.connect(
    host="<<host>>",
    user="<<username>>",
    password="<<password>>",
    database="PasswordManager"
)

cursor = mydb.cursor()

class DataBase:
    def get_srno(self):
        query = """
            select * from vault
        """
        cursor.execute(query)
        fetch = cursor.fetchall()

        return fetch[-1][0]
    
    def specific_record(self, srno):
        query="""
            select * from vault where SrNo=%s
        """
        cursor.execute(query, [srno])
        fetch = cursor.fetchall()
        return fetch

    def insert_record(self, srno, sitename, password):
        query = """
            insert into vault(SrNo, SiteName, Password) values(%s, %s, %s)
        """
        cursor.execute(query, [srno, sitename, password])
        mydb.commit()

    def delete_record(self, srno):
        query = """
            delete from vault where `SrNo` = %s
        """
        cursor.execute(query, [srno])
        mydb.commit()

    def update_record(self, srno, sitename, password):
        query="""
            update vault set SiteName=%s, Password=%s where SrNo=%s
        """
        cursor.execute(query, [sitename, password, srno])
        mydb.commit()

    def show_record(self):
        query = """
            select * from vault
        """
        cursor.execute(query)
        fetch = cursor.fetchall()

        records = []
        for i in fetch:
            record=[]
            for j in range(len(i)):
                if j % 3 == 2:
                    record.append("*****")    
                else:
                    record.append(i[j])
            records.append(record)
        return records
    
    def serialize(self):
        query = """
            select * from vault
        """
        cursor.execute(query)
        fetch = cursor.fetchall()

        record=[]
        for i in fetch:
            for j in range(len(i)):
                if j % 3 == 0:
                    record.append(i[j])
        u_record = [i+1 for i in range(len(record))]

        for i in range(len(record)):
            query = f"""
                update vault set SrNo={u_record[i]} where SrNo={record[i]}
            """
            cursor.execute(query)
            mydb.commit()
