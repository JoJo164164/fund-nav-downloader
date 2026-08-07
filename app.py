import streamlit as st
import sqlite3
import pandas as pd
import os

from database import DB_PATH, create_database


st.set_page_config(
    page_title="Fund NAV Downloader",
    page_icon="📈",
    layout="wide"
)


st.title("📈 Fund NAV Downloader")


# 建立資料庫
create_database()


# 檢查資料庫是否存在

if not os.path.exists(DB_PATH):

    st.warning("Database not found")

else:

    conn = sqlite3.connect(DB_PATH)


    # 讀取基金資料

    funds = pd.read_sql(
        """
        SELECT *
        FROM fund_master
        """,
        conn
    )


    if funds.empty:

        st.info(
            "No fund data available"
        )


    else:

        st.subheader(
            "Available Funds"
        )


        selected = st.selectbox(
            "Select Fund",
            funds["fund_name"]
        )


        fund_id = funds[
            funds["fund_name"] == selected
        ]["id"].iloc[0]


        nav = pd.read_sql(
            f"""
            SELECT
                nav_date,
                nav

            FROM nav_history

            WHERE fund_id = {fund_id}

            ORDER BY nav_date DESC
            """,
            conn
        )


        st.subheader(
            "Historical NAV"
        )


        st.dataframe(
            nav,
            use_container_width=True
        )


    conn.close()
