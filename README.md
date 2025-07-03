# Caprae Capital AI-Readiness Pre-Screening Challenge

## 🚀 Project: Lead Scoring, Validation & Enrichment Tool
**Built With:** Python, Streamlit, Pandas, Regex  

---

## ✅ What I Built:
A complete lead enhancement tool that:
- Accepts one or more CSV files
- Scores each lead 
- Validates emails and removes duplicates 
- Enriches with metadata like industry, founder, funding stage
- Offers filters and CSV export via an intuitive Streamlit interface

---

## 🎯 Features Implemented

### ✅ 1: Smart Lead Scoring
- Score out of 5 based on:
  - Personal email
  - LinkedIn present
  - HTTPS website
  - Domain length
  - Company name length

### ✅ 2: Data Validation & Deduplication
- Regex email validation
- Duplicate removal (based on email)
- “Verified” tag if email valid and LinkedIn exists

### ✅ 3: Enrichment (Mock)
- Adds:
  - Funding Stage (Seed, Series A, Bootstrapped)
  - Industry (SaaS, FinTech, HealthTech, etc.)
  - Founder Name
  - Auto-generated LinkedIn if missing

---

## 💡 Value to Business
- Instantly highlights high-quality, outreach-ready leads
- Saves analyst time
- Ensures cleaner and more trustworthy lead data
- Multi-source support with unified processing

---

## ⚙️ Tech Stack
- **Python**: core scripting
- **Streamlit**: app interface
- **Pandas**: dataframes and transformations
- **Regex**: email pattern validation

---

## 📥 Outputs
- Filtered & scored CSV
- Downloadable raw file per source (optional)

---


## 🔗 Do Check out **[👉 Try the Live App](https://caprae-lead-scoring-l5ch9zsc8o4cydsjtvgj2y.streamlit.app/)**
