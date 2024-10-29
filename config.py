# config.py
import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='your_username',       # Thay 'your_username' bằng tên người dùng của bạn
        password='your_password',   # Thay 'your_password' bằng mật khẩu của bạn
        database='library_db'       # Tên cơ sở dữ liệu
    )
    return conn
