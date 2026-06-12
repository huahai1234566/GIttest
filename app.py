import socket as _socket
_orig_getfqdn = _socket.getfqdn
_socket.getfqdn = lambda name='': name or 'localhost'

import pymysql
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "student_manage",
    "charset": "utf8mb4"
}


def get_db_connection():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except pymysql.MySQLError as e:
        return None


# ---------- 页面 ----------

@app.route('/')
def index():
    return render_template('index.html')


# ---------- API ----------

@app.route('/api/students', methods=['GET'])
def api_get_all_students():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "数据库连接失败"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        students = []
        for s in rows:
            students.append({
                "id": s[0],
                "name": s[1],
                "age": s[2],
                "gender": s[3],
                "major": s[4]
            })
        return jsonify(students)
    except pymysql.MySQLError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/students/<int:student_id>', methods=['GET'])
def api_get_student(student_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "数据库连接失败"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        s = cursor.fetchone()
        if not s:
            return jsonify({"error": "未找到该学生"}), 404
        return jsonify({
            "id": s[0],
            "name": s[1],
            "age": s[2],
            "gender": s[3],
            "major": s[4]
        })
    except pymysql.MySQLError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/students', methods=['POST'])
def api_add_student():
    data = request.get_json()
    name = data.get('name', '')
    age = data.get('age', 0)
    gender = data.get('gender', '')
    major = data.get('major', '')

    if not name:
        return jsonify({"error": "姓名不能为空"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "数据库连接失败"}), 500
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO students (name, age, gender, major) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (name, age, gender, major))
        conn.commit()
        return jsonify({"id": cursor.lastrowid, "message": "添加成功"}), 201
    except pymysql.MySQLError as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/students/<int:student_id>', methods=['PUT'])
def api_update_student(student_id):
    data = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "数据库连接失败"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        if not cursor.fetchone():
            return jsonify({"error": "未找到该学生"}), 404

        new_name = data.get('name', '')
        new_age = data.get('age', 0)
        new_gender = data.get('gender', '')
        new_major = data.get('major', '')

        if not new_name:
            return jsonify({"error": "姓名不能为空"}), 400

        sql = "UPDATE students SET name=%s, age=%s, gender=%s, major=%s WHERE id=%s"
        cursor.execute(sql, (new_name, new_age, new_gender, new_major, student_id))
        conn.commit()
        return jsonify({"message": "修改成功"})
    except pymysql.MySQLError as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def api_delete_student(student_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "数据库连接失败"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        if not cursor.fetchone():
            return jsonify({"error": "未找到该学生"}), 404

        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        conn.commit()
        return jsonify({"message": "删除成功"})
    except pymysql.MySQLError as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')
