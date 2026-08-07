import os
import sqlite3

import pandas as pd
import streamlit as st

from database import DB_PATH, create_database
from updater import add_test_fund


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Fund NAV Downloader",
    page_icon="📈",
    layout="wide"
)


# ============================================================
# Header
# ============================================================

st.title("📈 Fund NAV Downloader")

st.caption(
    "Historical NAV Downloader - Version 0.1"
)


# ============================================================
# Database Initialization
# ============================================================

try:

    create_database()

except Exception as e:

    st.error("Database initialization failed.")

    st.exception(e)

    st.stop()


# ============================================================
# Database Control
# ============================================================

st.subheader("Database Control")


if st.button(
    "Initialize Test Fund Data",
    type="primary"
):

    try:

        fund_status, nav_status = add_test_fund()

        st.success(
            f"{fund_status} | {nav_status}"
        )

        st.rerun()

    except Exception as e:

        st.error(
            "Failed to initialize test fund data."
        )

        st.exception(e)


# ============================================================
# Divider
# ============================================================

st.divider()


# ============================================================
# Fund List
# ============================================================

st.subheader("Fund List")


if not os.path.exists(DB_PATH):

    st.warning(
        "Database file does not exist."
    )

    st.stop()


try:

    conn = sqlite3.connect(DB_PATH)

    funds = pd.read_sql_query(
        """
        SELECT
            id,
            company,
            fund_name,
            currency,
            share_class,
            isin

        FROM fund_master

        ORDER BY company, fund_name
        """,
        conn
    )


    # ========================================================
    # No Fund Data
    # ========================================================

    if funds.empty:

        st.info(
            "No fund data available. "
            "Please click 'Initialize Test Fund Data'."
        )


    # ========================================================
    # Fund Data Available
    # ========================================================

    else:

        st.dataframe(
            funds,
            width="stretch",
            hide_index=True
        )


        # ====================================================
        # Historical NAV
        # ====================================================

        st.subheader("Historical NAV")


        selected_fund_name = st.selectbox(
            "Select Fund",
            options=funds["fund_name"].tolist()
        )


        selected_fund = funds[
            funds["fund_name"] == selected_fund_name
        ].iloc[0]


        fund_id = int(
            selected_fund["id"]
        )


        nav = pd.read_sql_query(
            """
            SELECT
                nav_date,
                nav

            FROM nav_history

            WHERE fund_id = ?

            ORDER BY nav_date DESC
            """,
            conn,
            params=(fund_id,)
        )


        # ====================================================
        # NAV Available
        # ====================================================

        if nav.empty:

            st.info(
                "No historical NAV data available for this fund."
            )


        else:

            st.dataframe(
                nav,
                width="stretch",
                hide_index=True
            )


            # =================================================
            # NAV Summary
            # =================================================

            st.caption(
                f"Total NAV records: {len(nav):,}"
            )


    conn.close()


except Exception as e:

    try:
        conn.close()
    except Exception:
        pass

    st.error(
        "Failed to read database."
    )

    st.exception(e)
