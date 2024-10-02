import sqlite3


def connect_to_db(db_name):
    """Connect to the SQLite database."""
    conn = sqlite3.connect(db_name)
    return conn


def create_table(conn):
    """Create a table to store student grades with a composite primary key."""
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS grades (
            duke_id INTEGER NOT NULL,
            assignment_id INTEGER NOT NULL,
            grade REAL NOT NULL,
            PRIMARY KEY (duke_id, assignment_id)
        );
    """
    )
    conn.commit()


def insert_data(conn, duke_id, assignment_id, grade):
    """Insert a grade entry into the grades table."""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO grades (duke_id, assignment_id, grade) VALUES (?, ?, ?)",
        (duke_id, assignment_id, grade),
    )
    conn.commit()


def read_data(conn):
    """Read all data from the grades table."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grades")
    rows = cursor.fetchall()
    return rows


def view_data(conn):
    rows = read_data(conn)

    print("Duke ID | Assignment ID | Grade ")
    print("-------------------------------")
    for row in rows:
        print(f"{row[0]:<7} | {row[1]:<12} | {row[2]:<5}")


def update_data(conn, duke_id, assignment_id, new_grade):
    """Update the grade for a specific student and assignment."""
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE grades SET grade = ? WHERE duke_id = ? AND assignment_id = ?",
        (new_grade, duke_id, assignment_id),
    )
    conn.commit()


def delete_data(conn, duke_id, assignment_id):
    """Delete a specific assignment's grade for a student."""
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM grades WHERE duke_id = ? AND assignment_id = ?", (duke_id, assignment_id)
    )
    conn.commit()


def get_average_grade_per_student(conn):
    """Query to get the average grade for each student."""
    cursor = conn.cursor()
    cursor.execute("SELECT duke_id, AVG(grade) AS average_grade FROM grades GROUP BY duke_id")
    rows = cursor.fetchall()
    print("Duke ID | Average Grade")
    print("----------------------")
    for row in rows:
        print(f"{row[0]:<7} | {row[1]:.3f}")
    return rows


def get_high_achievers(conn):
    """Query to get duke_id and assignment_id for grades greater than 90."""
    cursor = conn.cursor()
    cursor.execute("SELECT duke_id, assignment_id FROM grades WHERE grade > 90")
    rows = cursor.fetchall()
    print("Duke ID | Assignment ID")
    print("-----------------------")
    for row in rows:
        print(f"{row[0]}    | {row[1]}")
    return rows


if __name__ == "__main__":

    # Connect to the database
    conn = connect_to_db("ids706_grades.db")

    # Create the table with composite primary key (duke_id, assignment_id)
    create_table(conn)

    # Insert some sample data
    insert_data(conn, 1234567, 0, 85.0)  # Assignment ID starts from 0
    insert_data(conn, 1234567, 1, 90.5)  # Next assignment ID
    insert_data(conn, 1234567, 2, 99.0)  # Assignment ID 0 for another student
    insert_data(conn, 1234567, 3, 94.0)  # Assignment ID 0 for another student
    insert_data(conn, 7654321, 0, 78.0)  # Assignment ID 0 for another student
    insert_data(conn, 7654321, 1, 85.0)  # Assignment ID 0 for another student
    insert_data(conn, 7654321, 2, 83.0)  # Assignment ID 0 for another student

    print("Data after insertion:")
    view_data(conn)

    # Update a grade
    update_data(conn, 1234567, 0, 88.0)  # Update assignment 0 for duke_id 123456
    print("Data after update:")
    view_data(conn)

    # Delete a grade
    delete_data(conn, 7654321, 0)  # Delete assignment 0 for duke_id 654321
    print("Data after deletion:")
    view_data(conn)

    get_average_grade_per_student(conn)
    get_high_achievers(conn)

    # Close the connection
    conn.close()
