import sqlite3
from database import DB_PATH, create_database


def add_test_fund():

    create_database()

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()


    # 新增測試基金
    cursor.execute("""
    INSERT INTO fund_master
    (
        company,
        fund_name,
        currency,
        share_class,
        isin
    )
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        "AllianzGI",
        "Allianz Pet & Animal Wellbeing Fund",
        "USD",
        "AT",
        "TEST123456"
    ))


    fund_id = cursor.lastrowid


    # 新增測試NAV
    cursor.execute("""
    INSERT INTO nav_history
    (
        fund_id,
        nav_date,
        nav
    )
    VALUES (?, ?, ?)
    """,
    (
        fund_id,
        "2026-08-07",
        13.25
    ))


    conn.commit()

    conn.close()


    print("Test fund added successfully")


if __name__ == "__main__":

    add_test_fund()
