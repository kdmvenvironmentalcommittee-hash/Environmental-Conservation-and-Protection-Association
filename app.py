import streamlit as st
import pandas as pd
import re

# App එකේ මාතෘකා සැකසීම
st.title("Environmental Conservation and Protection Association")
st.subheader("Information search system")
st.caption("Program Administrator Division")

# Google Sheet Direct CSV Link
sheet_url = "https://docs.google.com/spreadsheets/d/1cl1wUgzu3LUVzHJEMItGYcY4SrwzNs5H9J84ekDMBz8/export?format=csv"

# තත්පර 60කට වරක් Data Refresh වන පරිදි Cache කිරීම
@st.cache_data(ttl=60)
def load_data(url):
    return pd.read_csv(url)

try:
    df = load_data(sheet_url)
    
    # Text සුද්ධ කිරීමේ ශ්‍රිතය (Dots, Extra spaces ඉවත් කිරීම)
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
            
            # හමුවූ සෑම පුද්ගලයෙකුටම අදාළ දත්ත පමණක් පෙන්වීම
            for idx, row in filtered_df.iterrows():
                # හිස් නොවන (Non-empty / Non-NaN) Columns පමණක් තෝරා ගැනීම
                valid_data = {}
                for col in df.columns:
                    val = row[col]
                    # හිස් සෛල (NaN, None, හෝ Empty String) පරීක්ෂා කිරීම
                    if pd.notna(val) and str(val).strip() != "":
                        valid_data[col] = val
                
                # දත්ත DataFrame එකක් ලෙස සකසා පෙන්වීම
                person_df = pd.DataFrame([valid_data])
                st.dataframe(person_df, use_container_width=True)
        else:
            st.warning("No records found / එබඳු නමක් හෝ අංකයක් පද්ධතියේ හමු නොවීය.")

except Exception as e:
    st.error("Google Sheet එක කියවීමේ දෝෂයක් පවතී. කරුණාකර Access Permissions පරීක්ෂා කරන්න.")
    
