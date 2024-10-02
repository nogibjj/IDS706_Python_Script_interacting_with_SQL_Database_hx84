from main import (
    connect_to_db,
    create_table,
    insert_data,
    read_data,
    update_data,
    delete_data,
    get_average_grade_per_student,
    get_high_achievers,
)


def test_create():
    conn = connect_to_db(":memory:")

    create_table(conn)

    insert_data(conn, "1234567", 0, 85.0)

    data = read_data(conn)
    assert len(data) == 1
    assert data[0][0] == 1234567
    assert data[0][1] == 0
    assert data[0][2] == 85.0

    conn.close()


def test_read():
    conn = connect_to_db(":memory:")

    create_table(conn)

    insert_data(conn, "1234567", 0, 85.0)
    insert_data(conn, "1234567", 1, 90.5)

    data = read_data(conn)
    assert len(data) == 2

    assert data[0][0] == 1234567
    assert data[0][1] == 0
    assert data[0][2] == 85.0

    assert data[1][0] == 1234567
    assert data[1][1] == 1
    assert data[1][2] == 90.5

    conn.close()


def test_update():
    conn = connect_to_db(":memory:")

    create_table(conn)

    insert_data(conn, "1234567", 0, 85.0)

    update_data(conn, "1234567", 0, 88.0)

    data = read_data(conn)
    assert data[0][2] == 88.0  # 成绩应该更新为88.0

    conn.close()


def test_delete():
    conn = connect_to_db(":memory:")

    create_table(conn)

    insert_data(conn, "1234567", 0, 85.0)
    insert_data(conn, "1234567", 1, 90.5)

    delete_data(conn, "1234567", 0)

    data = read_data(conn)
    assert len(data) == 1
    assert data[0][1] == 1
    assert data[0][2] == 90.5

    conn.close()


def test_get_average_grade_per_student():
    conn = connect_to_db("ids706_grades.db")
    data = get_average_grade_per_student(conn)
    assert len(data) == 2
    assert data[0][0] == 1234567
    assert data[0][1] == 92.875

    assert data[1][0] == 7654321
    assert data[1][1] == 84.00


def test_get_high_achievers():
    conn = connect_to_db("ids706_grades.db")
    data = get_high_achievers(conn)
    assert len(data) == 3
    assert data[0][0] == 1234567
    assert data[0][1] == 1
    assert data[1][0] == 1234567
    assert data[1][1] == 2
    assert data[2][0] == 1234567
    assert data[2][1] == 3
