import pymysql

# -------------------------- 数据库配置（请修改为你自己的信息） --------------------------
DB_CONFIG = {
    "host": "localhost",       # 数据库地址，本地就是localhost
    "port": 3306,              # MySQL端口，默认3306
    "user": "root",            # 你的MySQL用户名
    "password": "root",  # 你的MySQL密码
    "database": "student_manage",  # 数据库名
    "charset": "utf8mb4"
}
# -----------------------------------------------------------------------------------

# 获取数据库连接
def get_db_connection():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except pymysql.MySQLError as e:
        print(f"❌ 数据库连接失败: {e}")
        return None

# 1. 添加学生
def add_student():
    print("\n=== 添加学生信息 ===")
    name = input("请输入学生姓名: ")
    age = int(input("请输入学生年龄: "))
    gender = input("请输入学生性别: ")
    major = input("请输入学生专业: ")

    conn = get_db_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO students (name, age, gender, major) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (name, age, gender, major))
        conn.commit()
        print("✅ 学生信息添加成功！")
    except pymysql.MySQLError as e:
        print(f"❌ 添加失败: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# 2. 查询所有学生
def query_all_students():
    print("\n=== 所有学生信息 ===")
    conn = get_db_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        if not students:
            print("❌ 暂无学生信息")
            return
        print(f"{'学号':<6}{'姓名':<8}{'年龄':<6}{'性别':<6}{'专业':<20}")
        print("-" * 45)
        for s in students:
            print(f"{s[0]:<6}{s[1]:<8}{s[2]:<6}{s[3]:<6}{s[4]:<20}")
    except pymysql.MySQLError as e:
        print(f"❌ 查询失败: {e}")
    finally:
        cursor.close()
        conn.close()

# 3. 根据学号查询单个学生
def query_student_by_id():
    print("\n=== 查询学生信息 ===")
    student_id = int(input("请输入要查询的学生学号: "))
    conn = get_db_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        student = cursor.fetchone()
        if student:
            print(f"\n学号: {student[0]}")
            print(f"姓名: {student[1]}")
            print(f"年龄: {student[2]}")
            print(f"性别: {student[3]}")
            print(f"专业: {student[4]}")
        else:
            print("❌ 未找到该学号的学生")
    except pymysql.MySQLError as e:
        print(f"❌ 查询失败: {e}")
    finally:
        cursor.close()
        conn.close()

# 4. 修改学生信息
def update_student():
    print("\n=== 修改学生信息 ===")
    student_id = int(input("请输入要修改的学生学号: "))
    conn = get_db_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        student = cursor.fetchone()
        if not student:
            print("❌ 未找到该学号的学生")
            return
        print(f"当前信息: 姓名:{student[1]} 年龄:{student[2]} 性别:{student[3]} 专业:{student[4]}")
        print("请输入新信息（直接回车表示不修改）")
        new_name = input("新姓名: ") or student[1]
        new_age = input("新年龄: ")
        new_age = int(new_age) if new_age else student[2]
        new_gender = input("新性别: ") or student[3]
        new_major = input("新专业: ") or student[4]

        sql = "UPDATE students SET name=%s, age=%s, gender=%s, major=%s WHERE id=%s"
        cursor.execute(sql, (new_name, new_age, new_gender, new_major, student_id))
        conn.commit()
        print("✅ 学生信息修改成功！")
    except pymysql.MySQLError as e:
        print(f"❌ 修改失败: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# 5. 删除学生
def delete_student():
    print("\n=== 删除学生信息 ===")
    student_id = int(input("请输入要删除的学生学号: "))
    conn = get_db_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        student = cursor.fetchone()
        if not student:
            print("❌ 未找到该学号的学生")
            return
        confirm = input(f"确认要删除学生 {student[1]} 吗？(y/n): ")
        if confirm.lower() == 'y':
            cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
            conn.commit()
            print("✅ 学生信息删除成功！")
        else:
            print("❌ 已取消删除")
    except pymysql.MySQLError as e:
        print(f"❌ 删除失败: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# 主菜单
def main():
    while True:
        print("\n===== 学生信息管理系统（MySQL版） =====")
        print("1. 添加学生信息")
        print("2. 查询所有学生")
        print("3. 根据学号查询学生")
        print("4. 修改学生信息")
        print("5. 删除学生信息")
        print("6. 退出系统")

        choice = input("\n请输入你的选择(1-6): ")
        if choice == '1':
            add_student()
        elif choice == '2':
            query_all_students()
        elif choice == '3':
            query_student_by_id()
        elif choice == '4':
            update_student()
        elif choice == '5':
            delete_student()
        elif choice == '6':
            print("👋 退出系统，再见！")
            break
        else:
            print("❌ 无效输入，请输入1-6之间的数字")

if __name__ == "__main__":
    main()