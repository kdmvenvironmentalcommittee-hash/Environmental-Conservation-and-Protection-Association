import streamlit as st
import pandas as pd
import re

# Web Page එකෙහි Layout එක සැකසීම
st.set_page_config(page_title="ECPA - Information Search", layout="centered")

# CSS මඟින් titles මැදට (Center) කිරීම සහ Display හැඩගැන්වීම
st.markdown(
    """
    <style>
    .main-title {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 18px;
        font-weight: 600;
        text-align: center;
        color: #4A4A4A;
        margin-bottom: 5px;
    }
    .caption-title {
        font-size: 14px;
        text-align: center;
        color: #7A7A7A;
        margin-bottom: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 1. Logo එක GitHub එකේ Upload කර ඇත්නම් එහි නම යොදන්න:
logo_url = "logo.png" 

# Logo එක මැදට පෙන්වීම
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    try:
        st.image(logo_url, width=140)
    except:
        pass

# 2. මාතෘකා තුන මැදට (Center) කිරීම
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
            
            # හමුවූ සෑම පුද්ගලයෙකුටම අදාළ දත්ත පමණක් පෙන්වීම (Empty cells රහිතව)
            for idx, row in filtered_df.iterrows():
                valid_data = {}
                for col in df.columns:
                    val = row[col]
                    if pd.notna(val) and str(val).strip() != "":
                        valid_data[col] = val
                
                person_df = pd.DataFrame([valid_data])
                st.dataframe(person_df, use_container_width=True)
        else:
            st.warning("No records found / එබඳු නමක් හෝ අංකයක් පද්ධතියේ හමු නොවීය.")

except Exception as e:
    st.error("Google Sheet එක කියවීමේ දෝෂයක් පවතී. කරුණාකර Access Permissions පරීක්ෂා කරන්න.")
    
