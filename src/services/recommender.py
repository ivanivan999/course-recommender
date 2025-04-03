from typing import List
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import time
from sentence_transformers import SentenceTransformer
from .data import df

print("Initializing recommender system...")
start_time = time.time()

# Load the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Prepare the combined text for embedding
df['combined_text'] = (
    df['Title'].fillna('') + ' ' +
    df['Short Intro'].fillna('') + ' ' +
    df['Sub-Category'].fillna('') + ' ' +
    df['Skills'].fillna('')
)

# Generate embeddings for all courses at module load time
print("Generating embeddings for all courses (this may take a while)...")
llm_matrix = model.encode(df['combined_text'].tolist(), show_progress_bar=True)

print(f"Embeddings generated! Initialization took {time.time() - start_time:.2f} seconds")


def recommend_by_text_similarity(query, top_n=5, df=None): # add df argument
    """Recommend courses using sentence transformer embeddings"""
    # Encode the query - this is fast since it's just one item
    query_vec = model.encode([query])
    
    # Calculate similarity with all course embeddings - using precomputed llm_matrix
    similarities = cosine_similarity(query_vec, llm_matrix).flatten()
    
    # Get indices of top matches
    top_indices = similarities.argsort()[-top_n:][::-1]

    # Ensure we are using the correct DataFrame to pick recommendations
    if df is None:
        df = globals()['df']
    
    # Return the matched courses
    return df.iloc[top_indices][['Title', 'Category', 'Rating']]


def recommend_highlighted_courses(query, top_n=5):
    """
    Recommends highlighted courses based on a query, prioritizing top-rated,
    top-viewed, and a combined score. Uses precomputed embeddings.
    """
    # Get base recommendations using our pretrained model
    rec_df = recommend_by_text_similarity(query, df=df)  # Pass 'df' to the function
    
    # Join with the needed columns
    rec_df = rec_df[['Title']].merge(df[['Title', 'Category', 'Rating', 'Number of viewers']], on='Title', how='left')

    # Handle potential NaN values
    rec_df['Rating'] = rec_df['Rating'].fillna(0)
    rec_df['Number of viewers'] = rec_df['Number of viewers'].fillna(0)
    
    top_rated = rec_df.sort_values(by='Rating', ascending=False).head(top_n)
    top_viewed = rec_df.sort_values(by='Number of viewers', ascending=False).head(top_n)
    top_combined = rec_df.copy()
    top_combined[['scaled_rating', 'scaled_views']] = MinMaxScaler().fit_transform(top_combined[['Rating', 'Number of viewers']])
    top_combined['composite_score'] = top_combined['scaled_rating'] * 0.7 + top_combined['scaled_views'] * 0.3
    top_combined = top_combined.sort_values(by='composite_score', ascending=False).head(top_n)

    highlighted_recommendations = []

    for i in range(len(top_combined)):
        highlighted_recommendations.append({
            'Query': query,
            'Method': 'Top Combined Score',
            'Title': top_combined.iloc[i]['Title'],
            'Category': top_combined.iloc[i]['Category'],
            'Rating': top_combined.iloc[i]['Rating'],
            'Viewers': top_combined.iloc[i]['Number of viewers']
        })

    return pd.DataFrame(highlighted_recommendations)