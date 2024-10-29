# app.py
from flask import Flask, render_template, request, redirect, flash
from config import get_db_connection  # Tập tin cấu hình để lấy kết nối DB

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Khóa bảo mật cho session

# Route trang chủ để thêm sách và thành viên
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Thêm sách
        for i in range(5):
            book_title = request.form.get(f'book_title_{i}')
            if book_title:
                conn = get_db_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO books (title) VALUES (%s)", (book_title,))
                    conn.commit()
                except Exception as e:
                    flash(f'Error adding book: {e}', 'danger')
                finally:
                    cursor.close()
                    conn.close()

        # Thêm thành viên
        for i in range(3):
            member_name = request.form.get(f'member_name_{i}')
            member_birthdate = request.form.get(f'member_birthdate_{i}')
            member_address = request.form.get(f'member_address_{i}')
            if member_name:
                conn = get_db_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO members (name, birthdate, address) VALUES (%s, %s, %s)", 
                                   (member_name, member_birthdate, member_address))
                    conn.commit()
                except Exception as e:
                    flash(f'Error adding member: {e}', 'danger')
                finally:
                    cursor.close()
                    conn.close()

        flash('Books and members added successfully!', 'success')
        return redirect('/')

    return render_template('index.html')

# Route để tạo báo cáo
@app.route('/report')
def report():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.name, m.birthdate, m.address, b.title, t.borrow_date, t.status
        FROM transactions t
        JOIN members m ON t.member_id = m.id
        JOIN books b ON t.book_id = b.id
        WHERE DATE(t.borrow_date) = CURDATE()
    """)
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('report.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
