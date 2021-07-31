import mysql.connector
from mysql.connector import Error

# Matcher Navne i Databasen med Navne fundet med Scraperen
def importPhoneNumbers(name, phoneNum):
    try:
        # Opret forbindelse til databasen
        connection = mysql.connector.connect(user='root', password='digital', host='127.0.0.1', port='3306', auth_plugin='mysql_native_password', database = "datawarehouse")
        cursor = connection.cursor(prepared=True)
        # SQL query
        cmd = """UPDATE virksomhed SET tlf = %s WHERE UPPER(navn) = %s"""
        data_tuple= (phoneNum, name)
        cursor.execute(cmd, data_tuple)
        connection.commit()
        # Throw on query fail
    except mysql.connector.Error as error:print("parameterized query failed {}".format(error))
    
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()