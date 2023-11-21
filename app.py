import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secret key for session security

# Function to create the SQLite database table
def create_table():
    connection = sqlite3.connect('students.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            parent_name TEXT NOT NULL,
            parent_phone TEXT NOT NULL,
            address TEXT NOT NULL,
            room_number INTEGER NOT NULL,
            course TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    ''')

    connection.commit()
    connection.close()

# Create the SQLite database table
create_table()

@app.route('/')
def index():
    search = request.args.get('search', '')
    
    connection = sqlite3.connect('students.db')
    cursor = connection.cursor()

    # Use LIKE to perform a case-insensitive search
    cursor.execute('''
        SELECT * FROM students
        WHERE student_name LIKE ? OR parent_name LIKE ?
    ''', ('%'+search+'%', '%'+search+'%'))

    students = cursor.fetchall()

    connection.close()

    return render_template('index.html', students=students, search=search)
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_name = request.form['student_name']
        parent_name = request.form['parent_name']
        parent_phone = request.form['parent_phone']
        address = request.form['address']
        room_number = request.form['room_number']
        course = request.form['course']
        year = request.form['year']

        connection = sqlite3.connect('students.db')
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO students (student_name, parent_name, parent_phone, address, room_number, course, year)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (student_name, parent_name, parent_phone, address, room_number, course, year))

        connection.commit()
        connection.close()

        flash('Student added successfully', 'success')
        return redirect(url_for('index'))

    return render_template('add_student.html')

# ...

# ...

@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    connection = sqlite3.connect('students.db')
    cursor = connection.cursor()

    if request.method == 'POST':
        # Retrieve updated data from the form
        student_name = request.form['student_name']
        parent_name = request.form['parent_name']
        parent_phone = request.form['parent_phone']
        address = request.form['address']
        room_number = request.form['room_number']
        course = request.form['course']
        year = request.form['year']

        # Update the student data in the database
        cursor.execute('''
            UPDATE students
            SET student_name=?, parent_name=?, parent_phone=?, address=?, room_number=?, course=?, year=?
            WHERE id=?
        ''', (student_name, parent_name, parent_phone, address, room_number, course, year, student_id))

        connection.commit()
        connection.close()

        flash('Student updated successfully', 'success')
        return redirect(url_for('index'))

    # Fetch the existing student data for pre-filling the form
    cursor.execute('SELECT * FROM students WHERE id=?', (student_id,))
    student_data = cursor.fetchone()

    connection.close()

    if student_data:
        return render_template('edit_student.html', student_data=student_data)
    else:
        flash('Student not found', 'error')
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
