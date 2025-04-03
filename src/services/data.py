import pandas as pd
from pathlib import Path
import numpy as np

# Get the absolute path to the data directory
data_dir = Path(__file__).parent.parent / 'data'
df = pd.read_csv(data_dir / 'Online_Courses.csv')
# Drop any row with nulls in critical fields
required_cols = ['Title', 'Rating', 'Short Intro', 'Category', 'Skills', 'Number of viewers']
df = df.dropna(subset=required_cols)

# Filter to only English courses
if 'Language' in df.columns:
    df = df[df['Language'] == 'English']
df = df.dropna(subset=['Title', 'Rating'])

# Clean rating field
if 'Rating' in df.columns:
    df['Rating'] = df['Rating'].astype(str).str.extract(r'(\d+\.\d+)').astype(float)

# Clean viewers field
if 'Number of viewers' in df.columns:
    df['Number of viewers'] = df['Number of viewers'].astype(str).str.replace(',', '').str.strip()
    df['Number of viewers'] = pd.to_numeric(df['Number of viewers'], errors='coerce')

# Drop exact duplicate courses based on Title and Instructor (if available)
if 'Instructor' in df.columns:
    df = df.drop_duplicates(subset=['Title', 'Instructor'])
else:
    df = df.drop_duplicates(subset=['Title'])

# Fill NA for text features
df['Short Intro'] = df['Short Intro'].fillna('')
df['Category'] = df['Category'].fillna('')
df['Skills'] = df['Skills'].fillna('')
df['Sub-Category'] = df['Sub-Category'].fillna('')