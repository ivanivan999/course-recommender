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

# Clean 'Rating' column to numeric
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

# Clean 'Number of viewers'
def parse_viewers(val):
    if isinstance(val, str):
        val = val.replace('k', '').replace('K', '').strip()
        try:
            return float(val) * 1000
        except:
            return np.nan
    return val

df['Number of viewers'] = df['Number of viewers'].apply(parse_viewers)

# Fill NA for text features
df['Short Intro'] = df['Short Intro'].fillna('')
df['Category'] = df['Category'].fillna('')
df['Skills'] = df['Skills'].fillna('')
df['Sub-Category'] = df['Sub-Category'].fillna('')