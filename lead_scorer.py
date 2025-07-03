import pandas as pd

# Load CSV
df = pd.read_csv("sample_leads.csv")

# Define helper to check for personal emails
def is_personal_email(email):
    generic_keywords = ['info', 'support', 'contact', 'sales', 'admin']
    return not any(keyword in str(email).lower() for keyword in generic_keywords)

# Define the scoring function
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

# Apply scoring to all leads
df['Lead Score'] = df.apply(score_lead, axis=1)

# Show final results
print(df)

# Save to new CSV
df.to_csv("scored_leads.csv", index=False)
