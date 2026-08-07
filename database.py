import sqlite3
import os


DB_PATH = "data/fund_nav.db"


def create_database():

    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()


    # 基金基本資料
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fund_master (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company TEXT,

        fund_name TEXT,

        currency TEXT,

        share_class TEXT,

        isin TEXT

    )
    """)


    # 歷史淨值
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nav_history (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        fund_id INTEGER,

        nav_date TEXT,

        nav REAL,

        FOREIGN KEY (fund_id)
        REFERENCES fund_master(id)

    )
    """)


    conn.commit()

    conn.close()



if __name__ == "__main__":

    create_database()

    print("Database created successfully")
