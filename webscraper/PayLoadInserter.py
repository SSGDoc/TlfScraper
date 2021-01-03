import mysql.connector
from mysql.connector import Error

def importPhoneNumbers(name, phoneNum):
    try:
        connection = mysql.connector.connect(user='root', password='digital', host='127.0.0.1', port='3306', auth_plugin='mysql_native_password', database = "datawarehouse")
        cursor = connection.cursor(prepared=True)
        cmd = """UPDATE virksomhed SET tlf = %s WHERE UPPER(navn) = %s"""
        data_tuple= (phoneNum, name)
        cursor.execute(cmd, data_tuple)
        connection.commit()
        
    except mysql.connector.Error as error:print("parameterized query failed {}".format(error))
    
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()