import streamlit as st
import pandas as pd

st.title("තොරතුරු සෙවුම් පද්ධතිය")

# මෙතැන ඇති Link එක වෙනුවට ඔබගේ Google Sheet Link එක දමන්න
sheet_url = "import streamlit as st
import pandas as pd

st.title("තොරතුරු සෙවුම් පද්ධතිය")

# Direct CSV Link එක මෙතැනට යොදන්න
sheet_url = "https://docs.google.com/spreadsheets/d/ඔබගේ_SHEET_ID_එක/export?format=csv"

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

try:
    df = load_data(sheet_url)
    search_query = st.text_input("ඔබගේ නම හෝ ID අංකය ඇතුළත් කරන්න:")

    if search_query:
        filtered_df = df[df.astype(str).apply(lambda row: row.str.contains(search_query, case=False)).any(axis=1)]

        if not filtered_df.empty:
            st.success("ඔබගේ විස්තර පහත දැක්වේ:")
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.warning("එබඳු නමක් හෝ අංකයක් පද්ධතියේ හමු නොවීය.")
except Exception as e:
    st.error("Google Sheet එක කියවීමේ දෝෂයක් පවතී. කරුණාකර Link එක Anyone with the link ලෙස වෙනස් කර ඇත්දැයි බලන්න.")
"

@st.cache_data
def load_data(url):
    # Google Sheet Link එක CSV format එකට හරවා කියවීම
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv').replace('/edit#gid=', '/export?format=csv&gid=')
    return pd.read_csv(csv_url)

try:
    df = load_data(sheet_url)
    search_query = st.text_input("ඔබගේ නම හෝ ID අංකය ඇතුළත් කරන්න:")

    if search_query:
        filtered_df = df[df.astype(str).apply(lambda row: row.str.contains(search_query, case=False)).any(axis=1)]

        if not filtered_df.empty:
            st.success("ඔබගේ විස්තර පහත දැක්වේ:")
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.warning("එබඳු නමක් හෝ අංකයක් පද්ධතියේ හමු නොවීය.")
