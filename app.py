import streamlit as st
import pandas as pd
import re

# Web Page එකෙහි Layout එක සැකසීම
st.set_page_config(page_title="ECPA - Information Search", layout="centered")

# Option 1: Direct Live Dark Ocean Video URL
video_url = "https://assets.mixkit.co/videos/preview/mixkit-dramatic-dark-stormy-sea-waves-42617-large.mp4"

# CSS මඟින් Live Video Background එක සහ Text Styling සැකසීම
st.markdown(
    f"""
    <style>
    #bgVideo {{
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%;
        min-height: 100%;
        width: auto;
        height: auto;
        z-index: -100;
        object-fit: cover;
        filter: brightness(0.55); /* පසුබිම අඳුරු කර අකුරු පැහැදිලිව පෙන්වීමට */
    }}

    .main-title {{
        font-size: 26px;
        font-weight: bold;
        text-align: center;
        margin-top: 30px;
        margin-bottom: 5px;
        color: #FFFFFF;
        text-shadow: 2px 2px 6px #000000;
    }}
    .sub-title {{
        font-size: 18px;
        font-weight: 600;
        text-align: center;
        color: #E0E0E0;
        margin-bottom: 5px;
        text-shadow: 1px 1px 4px #000000;
    }}
    .caption-title {{
        font-size: 14px;
        text-align: center;
        color: #CCCCCC;
        margin-bottom: 30px;
        text-shadow: 1px 1px 4px #000000;
    }}
    </style>

    <video autoplay loop muted playsinline id="bgVideo">
        <source src="{video_url}" type="video/mp4">
    </video>
    """,
    unsafe_allow_html=True
)

# මාතෘකා තුන මැදට (Center) කිරීම - Logo නොමැත
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
    
