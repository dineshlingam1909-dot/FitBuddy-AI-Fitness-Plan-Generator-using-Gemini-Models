import sqlite3


DATABASE_NAME = "fitbuddy.db"


def get_connection():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    connection.row_factory = sqlite3.Row

    return connection


def init_db():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            weight REAL NOT NULL,
            goal TEXT NOT NULL,
            intensity TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            original_plan TEXT NOT NULL,
            updated_plan TEXT,
            nutrition_tip TEXT NOT NULL,
            feedback TEXT
        )
    """)

    connection.commit()

    connection.close()


def save_user(data):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO users
        (
            user_id,
            name,
            age,
            weight,
            goal,
            intensity
        )
        VALUES (?, ?, ?, ?, ?, ?)

        ON CONFLICT(user_id)
        DO UPDATE SET
            name = excluded.name,
            age = excluded.age,
            weight = excluded.weight,
            goal = excluded.goal,
            intensity = excluded.intensity
    """, (
        data.user_id,
        data.name,
        data.age,
        data.weight,
        data.goal,
        data.intensity
    ))

    connection.commit()

    connection.close()


def get_user(user_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    connection.close()

    return user


def save_plan(
    user_id,
    original_plan,
    nutrition_tip
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO plans
        (
            user_id,
            original_plan,
            nutrition_tip
        )
        VALUES (?, ?, ?)
    """, (
        user_id,
        original_plan,
        nutrition_tip
    ))

    connection.commit()

    plan_id = cursor.lastrowid

    connection.close()

    return plan_id


def get_latest_plan(user_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM plans
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (user_id,))

    plan = cursor.fetchone()

    connection.close()

    return plan


def update_plan(
    plan_id,
    updated_plan,
    feedback
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE plans
        SET
            updated_plan = ?,
            feedback = ?
        WHERE id = ?
    """, (
        updated_plan,
        feedback,
        plan_id
    ))

    connection.commit()

    connection.close()


def get_all_users():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        ORDER BY id DESC
    """)

    users = cursor.fetchall()

    connection.close()

    return users


def get_all_plans():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM plans
        ORDER BY id DESC
    """)

    plans = cursor.fetchall()

    connection.close()

    return plans