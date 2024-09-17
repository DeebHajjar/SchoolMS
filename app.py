import sqlite3
from datetime import datetime

def display_menu():
    print("Please choose the operation you want to perform")
    print("* To add a student, click on the letter a")
    print("* To delete a student, press the letter d")
    print("* To modify a student's information, press the letter u")
    print("* To view student information, press the letter s")


def add_student():
    conn = None
    try:
        #الاتصال بقاعدة البيانات
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()

        #جمع معلومات الطالب
        student_id = input("Enter the student number: ")
        first_name = input("Enter the student's name: ")
        last_name = input("Enter the student's nickname: ")
        age = input("Enter the student's age: ")
        grade = input("Enter the student's class: ")
        registration_date = datetime.now().strftime("%Y-%m-%d")

        #اضافة معلومات الطالب الى قاعدة البيانات
        #استخدام علامة الاستفهام كمعاملات لمنع هجمات حقن SQL
        cursor.execute('''INSERT INTO students (id, first_name, last_name, age, grade, registration_date)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (student_id, first_name, last_name, age, grade, registration_date))

        #لعرض الدروس الموجودة حاليا في جدول الدروس
        print("Existing lessons:")
        cursor.execute("SELECT * FROM lessons")
        lessons = cursor.fetchall()
        for lesson in lessons:
            print(lesson)

        #اضافة الدروس للطالب
        while True:
            lesson_id = input("Enter the lesson number (press Enter to finish): ")
            if not lesson_id:
                break
            else:
                #اضافة العلاقة بين الدرس والطالب
                cursor.execute('''
                INSERT INTO student_lessons (student_id, lesson_id)
                VALUES (?, ?)
                ''', (student_id, lesson_id))
        
        conn.commit()
        print("The student and lessons have been added successfully.\n")
    #لاظهار الخطأ
    except sqlite3.Error as e:
        print(e)
        #الغاء جميع التغييرات التي حصلت في قاعدة البيانات في حال حدوث خطأ
        if conn:
            conn.rollback()
    
    #اغلاق قاعدة اليانات بالشكل الصحيح
    finally:
        if conn:
            conn.close()


def delete_student():
    conn = None
    try:
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()

        student_id = input("Enter the student number you want to delete: ")
        #التحقق من وجود الطالب
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student = cursor.fetchone()

        if student:
            #حذف الطاب وجميع معلوماته
            cursor.execute("DELETE FROM students WHERE id = ?", (student_id))
            #حذف جميع العلاقات المرتبطة بالطالب
            cursor.execute("DELETE FROM student_lessons WHERE student_id = ?", (student_id))

            conn.commit()
            print(f"The student has been successfully deleted: {student[1]} {student[2]}\n")

        else:
            print("No student found with this number.")

    except sqlite3.Error as e:
        print(e)
        if conn:
            conn.rollback()
    
    finally:
        if conn:
            conn.close()


def update_student():
    conn = None
    try:
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()

        student_id = input("Enter the student number you want to modify: ")
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student = cursor.fetchone()

        if student:
            #اخذ معلومات الطالب الجديدة
            first_name = input("Enter the new student's name (To keep the local value, press Enter): ") or student[1]
            last_name = input("Enter the new student's nickname (To keep the local value, press Enter): ") or student[2]
            age = input("Enter the new student's age (To keep the local value, press Enter): ") or student[3]
            grade = input("Enter the new student's class (To keep the local value, press Enter): ") or student[4]

            #اضافة معلومات الطالب الجديدة الى قاعدة البيانات
            cursor.execute('''
            UPDATE students 
            SET first_name = ?, last_name = ?, age = ?, grade = ?
            WHERE id = ?
            ''', (first_name, last_name, age, grade, student_id))
            
            conn.commit()
            print(f"The student has been successfully updated. \n")
        
        else:
            print("No student found with this number.\n")
    
    except sqlite3.Error as e:
        print(e)
        if conn:
            conn.rollback()
    
    finally:
        if conn:
            conn.close()


def show_student():
    conn = None
    try:
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()

        #التحقق من وجود الطالب وجلب معلوماته
        student_id = input("EntEnter the student number whose information you want to view: ")
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student = cursor.fetchone()
        
        if student:
            print(f"id: {student[0]}\nFirst name: {student[1]}\nLast name: {student[2]}\nAge: {student[3]}\nGrade: {student[4]}\nRegistration date: {student[5]}")

            # جلب الدروس المسجل فيها الطالب
            cursor.execute("""
            SELECT *
            FROM lessons
            JOIN student_lessons ON lessons.id = student_lessons.lesson_id
            WHERE student_lessons.student_id = ?
            """, (student_id,))
            lessons = cursor.fetchall()

            if lessons:
                print("Recorded lessons:", end=" ")
                for lesson in lessons:
                    print(lesson[1], end=" ")
            else:
                print("The student has not registered for any lessons")
        
        else:
            print("No student found with this number.")
        print("\n")
    
    except sqlite3.Error as e:
        print(e)
    
    finally:
        if conn:
            conn.close()

  
def main():
    while True:
        display_menu()
        choice = input("Your choice: ").lower()
        if choice == 'a':
            add_student()
        elif choice == 'd':
            delete_student()
        elif choice == 'u':
            update_student()
        elif choice == 's':
            show_student()
        elif choice == 'exit':
            break
        else:
            print("Invalid selection. Please try again.")


if __name__ == "__main__":
    main()