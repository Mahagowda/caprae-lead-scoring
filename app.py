import streamlit as st
import pandas as pd
import re

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="Caprae Lead Tool", layout="wide")
st.markdown("""
    <style>
    .big-title { font-size: 36px; font-weight: bold; color: #4CAF50; }
    .sub-text { font-size: 16px; color: #666666; }
    .section-header { color: #2C3E50; margin-top: 20px; font-size: 22px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# ----------------- HEADER -----------------
st.markdown('<p class="big-title">🚀 Lead Scoring & Enrichment Tool</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Built for Caprae Capital | Upload your lead lists (CSV) and get clean, enriched, and ranked leads.</p>', unsafe_allow_html=True)

# ----------------- FILE UPLOAD -----------------
with st.container():
    st.markdown('<div class="section-header">📁 Upload CSVs</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Upload one or more CSV files (must have Company, Website, Email, LinkedIn)", type="csv", accept_multiple_files=True)

# ----------------- HELPER FUNCTIONS -----------------
def is_personal_email(email):
    generic_keywords = ['info', 'support', 'contact', 'sales', 'admin']
    return not any(keyword in str(email).lower() for keyword in generic_keywords)

def is_valid_email_format(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, str(email)) is not None

def enrich_lead(row):
    domain = str(row['Website']).replace("https://", "").replace("http://", "").split('/')[0]
    enrichment = {}

    if "ai" in domain or "ml" in domain:
        enrichment["Funding Stage"] = "Seed"
    elif "tech" in domain:
        enrichment["Funding Stage"] = "Series A"
    else:
        enrichment["Funding Stage"] = "Bootstrapped"

    if "health" in domain:
        enrichment["Industry"] = "HealthTech"
    elif "fin" in domain:
        enrichment["Industry"] = "FinTech"
    elif "edu" in domain:
        enrichment["Industry"] = "EdTech"
    else:
        enrichment["Industry"] = "SaaS"

    enrichment["Founder"] = "Jane Doe" if pd.notnull(row['Company']) else "N/A"

    if pd.isnull(row['LinkedIn']) or row['LinkedIn'].strip() == "":
        enrichment["LinkedIn"] = f"https://linkedin.com/company/{domain.split('.')[0]}"
    else:
        enrichment["LinkedIn"] = row['LinkedIn']

    return pd.Series(enrichment)

def score_lead(row):
    score = 0
    if pd.notnull(row['Email']) and is_personal_email(row['Email']):
        score += 1
    if pd.notnull(row['LinkedIn']) and row['LinkedIn'].strip() != "":
        score += 1
    if pd.notnull(row['Website']) and row['Website'].startswith("https://"):
        score += 1
    if pd.notnull(row['Website']):
        domain = row['Website'].replace("https://", "").replace("http://", "").split('/')[0]
        if len(domain) > 5:
            score += 1
    if pd.notnull(row['Company']) and len(row['Company']) > 3:
        score += 1
    return score

# ----------------- PROCESS FILES -----------------
if uploaded_files:
    st.markdown('<div class="section-header">📂 Individual Processed Files</div>', unsafe_allow_html=True)

    df_list = []
    for file in uploaded_files:
        name = file.name
        df_temp = pd.read_csv(file)

        # Enrich + validate + score
        df_temp[["Funding Stage", "Industry", "Founder", "LinkedIn"]] = df_temp.apply(enrich_lead, axis=1)
        df_temp['Email Format Valid'] = df_temp['Email'].apply(lambda x: is_valid_email_format(x) if pd.notnull(x) else False)
        df_temp['Verified'] = df_temp.apply(lambda row: 'Yes' if row['Email Format Valid'] and pd.notnull(row['LinkedIn']) and row['LinkedIn'].strip() != "" else 'No', axis=1)
        df_temp['Lead Score'] = df_temp.apply(score_lead, axis=1)

        # Drop duplicates
        df_temp = df_temp.drop_duplicates(subset=['Email'], keep='first')
        df_list.append(df_temp)

        # Download button
        csv = df_temp.to_csv(index=False)
        st.download_button(f"📄 Download Processed - {name}", data=csv, file_name=f"processed_{name}", mime="text/csv")

    # Merge for combined view
    df = pd.concat(df_list, ignore_index=True)

    # ----------------- FILTERS -----------------
    st.markdown('<div class="section-header">🎯 Filters</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([1.5, 1.5, 1.5, 2])

    with col1:
        email_filter = st.selectbox("Email Type", ["All", "Only Personal Emails"])
        if email_filter == "Only Personal Emails":
            df = df[df['Email'].apply(lambda x: is_personal_email(x) if pd.notnull(x) else False)]

    with col2:
        linkedin_only = st.checkbox("✅ LinkedIn Only", value=True)
        if linkedin_only:
            df = df[df['LinkedIn'].notnull() & (df['LinkedIn'].str.strip() != "")]

    with col3:
        verified_only = st.checkbox("✅ Verified Only", value=False)
        if verified_only:
            df = df[df['Verified'] == 'Yes']

    with col4:
        show_enriched = st.checkbox("💡 Show Enriched Data", value=True)

    min_score = st.slider("Minimum Lead Score", 0, 5, 3)
    filtered_df = df[df['Lead Score'] >= min_score]

    # ----------------- RESULTS -----------------
    st.markdown('<div class="section-header">📋 Filtered Leads</div>', unsafe_allow_html=True)
    display_columns = ['Company', 'Website', 'Email', 'LinkedIn', 'Lead Score', 'Verified']
    if show_enriched:
        display_columns += ['Funding Stage', 'Industry', 'Founder']

    st.dataframe(filtered_df[display_columns], use_container_width=True)

    # ----------------- DOWNLOAD COMBINED -----------------
    st.download_button("📥 Download All Filtered Leads", data=filtered_df.to_csv(index=False), file_name="scored_leads_combined.csv", mime="text/csv")
