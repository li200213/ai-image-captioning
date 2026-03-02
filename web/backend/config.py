import pymysql

conn = pymysql.connect(
        host='172.24.85.7',
        port=3306,
        user='root',
        password='123456',
        database='user'
    )