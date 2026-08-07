import sqlite3

from database import DB_PATH, create_database


TEST_FUND = {
    "company": "AllianzGI",
    "fund_name": "Allianz Pet & Animal Wellbeing Fund",
    "currency": "USD",
    "share_class": "AT",
    "isin": "TEST123456"
}


TEST_NAV = {
    "nav_date": "2026-08-07",
    "nav": 13.25
}


def add_test_fund():

    # 確保資料庫存在
    create_database()


    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()


    # ==========================
    # Check Fund Exists
    # ==========================

    cursor.execute(
        """
        SELECT id
        FROM fund_master
        WHERE company = ?
        AND fund_name = ?
        AND currency = ?
        AND share_class = ?
        """,
        (
            TEST_FUND["company"],
            TEST_FUND["fund_name"],
            TEST_FUND["currency"],
            TEST_FUND["share_class"]
        )
    )


    fund = cursor.fetchone()


    if fund:

        fund_id = fund[0]

        fund_status = "Fund already exists"


    else:

        cursor.execute(
            """
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
                TEST_FUND["company"],
                TEST_FUND["fund_name"],
                TEST_FUND["currency"],
                TEST_FUND["share_class"],
                TEST_FUND["isin"]
            )
        )


        fund_id = cursor.lastrowid

        fund_status = "Fund created"



    # ==========================
    # Check NAV Exists
    # ==========================

    cursor.execute(
        """
        SELECT id
        FROM nav_history
        WHERE fund_id = ?
        AND nav_date = ?
        """,
        (
            fund_id,
            TEST_NAV["nav_date"]
        )
    )


    nav = cursor.fetchone()


    if nav:

        nav_status = "NAV already exists"


    else:

        cursor.execute(
            """
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
                TEST_NAV["nav_date"],
                TEST_NAV["nav"]
            )
        )


        nav_status = "NAV created"



    conn.commit()

    conn.close()


    return (
        fund_status,
        nav_status
    )



if __name__ == "__main__":

    result = add_test_fund()

    print(result)
