import streamlit as st
import sqlite3
import pandas as pd
import os

from database import DB_PATH, create_database
from updater import add_test_fund


st.set_page_config(
    page_title="Fund NAV Downloader",
    page_icon="📈",
    layout="wide"
)


st.title("📈 Fund NAV Downloader")


if st.button("Initialize Test Fund Data"):

    add_test_fund()

    st.success(
        "Test fund data added!"
    )

    st.rerun()
