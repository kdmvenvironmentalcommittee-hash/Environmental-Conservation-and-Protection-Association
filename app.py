import streamlit as st
import pandas as pd
import re

# Web Page එකෙහි Layout එක සැකසීම
st.set_page_config(page_title="ECPA - Information Search", layout="centered")

# CSS මඟින් Clean Dark Blue Modern Theme එක සැකසීම
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0a192f 0%, #112240 50%, #1b2a4a 100%);
    }
    
    .main-title {
        font-size: 26px;
        font-weight: bold;
        text-align: center;
        margin-top: 30px;
        margin-bottom: 5px;
        color: #64ffda;
        text-shadow: 0px 2px 8px rgba(0, 0, 0, 0.5);
    }
    .sub-title {
        font-size: 18px;
        font-weight: 600;
        text-align: center;
        color: #e6f1ff;
        margin-bottom: 5px;
    }
    .caption-title {
        font-size: 14px;
        text-align: center;
        color: #8892b0;
        margin-bottom: 30px;
    }
    
    /* Input box style */
    div[data-baseweb="input"] {
        background-color: #112240;
        border-radius: 8px;
        color: #e6f1ff;
    }
    
    /* Table card style */
    .stDataFrame {
        background-color: #112240;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# මාතෘකා තුන මැදට (Center) කිරීම
st.markdown('<div class="main-title">Environmental Conservation and Protection Association</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Information search system</div>', unsafe_allow_html=True)
st.markdown('<div class="caption-title">Program Administrator Division</div>', unsafe_allow_html=True)

# Google Sheet Direct CSV Link
sheet_url = "https://docs.google.com/spreadsheets/d/1cl1wUgzu3LUVzHJEMItGYcY4SrwzNs5H9J84ekDMBz8/export?format=csv"

# තත්පර 60කට වරක් Data Refresh වන පරිදි Cache කිරීම
@st.cache_data(ttl=60)
def load_data(url):
    return pd.read_csv(url)

try:
    df = load_data(sheet_url)
    
    # Text සුද්ධ කිරීමේ ශ්‍රිතය
    def clean_text(text):
        if pd.isna(text):
            return ""
        return re.sub(r'[^a-zA-Z0-9]', '', str(text)).lower()

    search_query = st.text_input("Enter your Name or ID Number / ඔබගේ නම හෝ ID අංකය ඇතුළත් කරන්න:")

    if search_query.strip():
        cleaned_query = clean_text(search_query)
        
        # සියලුම Column වල සෙවීම
        mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False, na=False)).any(axis=1)
        
        # විශේෂිත Cleaned Search (Dots/Spaces නැතුව සෙවීම)
        if not mask.any():
            mask = df.apply(lambda row: row.astype(str).apply(lambda val: cleaned_query in clean_text(val))).any(axis=1)

        filtered_df = df[mask]

        if not filtered_df.empty:
            st.success("Your details / ඔබගේ විස්තර පහත දැක්වේ:")
            
            # හිස් නැති සෛල (Non-empty cells) සහිත දත්ත පමණක් පෙන්වීම
            for idx, row in filtered_df.iterrows():
                valid_row = row.dropna()
                valid_row = valid_row[valid_row.astype(str).str.strip() != ""]
                person_df = pd.DataFrame([valid_row])
                st.dataframe(person_df, use_container_width=True)
        else:
            st.warning("No records found / එබඳු නමක් හෝ අංකයක් පද්ධතියේ හමු නොවීය.")

except Exception as e:
    st.error("Google Sheet එක කියවීමේ දෝෂයක් පවතී. කරුණාකර Access Permissions පරීක්ෂා කරන්න.")
            st.warning("No records found / එබඳු නමක් හෝ අංකයක් පද්ධතියේ හමු නොවීය.")

except Exception as e:
    st.error("Google Sheet එක කියවීමේ දෝෂයක් පවතී. කරුණාකර Access Permissions පරීක්ෂා කරන්න.")
