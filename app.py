import streamlit as st
import sqlite3
import pandas as pd
import os

from database import DB_PATH, create_database
from updater import add_test_fund


# ==========================
# Page Setting
# ==========================

st.set_page_config(
    page_title="Fund NAV Downloader",
    page_icon="📈",
    layout="wide"
)


# ==========================
# Title
# ==========================

st.title("📈 Fund NAV Downloader")

st.caption(
    "Historical NAV Downloader - Version 0.1"
)


# ==========================
# Initialize Database
# ==========================

try:

    create_database()

except Exception as e:

    st.error("Database initialization failed")

    st.exception(e)


# ==========================
# Test Data Button
# ==========================

st.subheader("Database Control")


if st.button("Initialize Test Fund Data"):

    try:

        add_test_fund()

        st.success(
            "Test fund data added successfully!"
        )

        st.rerun()


    except Exception as e:

        st.error(
            "Failed to add test data"
        )

        st.exception(e)



# ==========================
# Check Database
# ==========================

st.divider()

st.subheader("Fund List")


if not os.path.exists(DB_PATH):

    st.warning(
        "Database file does not exist"
    )


else:

    try:

        conn = sqlite3.connect(DB_PATH)


        funds = pd.read_sql(
            """
            SELECT *
            FROM fund_master
            """,
            conn
        )


        if funds.empty:

            st.info(
                "No fund data available. Please initialize test data."
            )


        else:

            st.dataframe(
                funds,
                use_container_width=True
            )


            st.subheader(
                "Historical NAV"
            )


            selected_fund = st.selectbox(
                "Select Fund",
                funds["fund_name"]
            )


            fund_id = funds.loc[
                funds["fund_name"] == selected_fund,
                "id"
            ].iloc[0]


            nav = pd.read_sql(
                """
                SELECT
                    nav_date,
                    nav

                FROM nav_history

                WHERE fund_id = ?

                ORDER BY nav_date DESC
                """,
                conn,
                params=(int(fund_id),)
            )


            st.dataframe(
                nav,
                use_container_width=True
            )


        conn.close()


    except Exception as e:

        st.error(
            "Failed to read database"
        )

        st.exception(e)
