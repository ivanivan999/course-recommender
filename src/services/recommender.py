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


def recommend_by_text_similarity(query: str) -> pd.DataFrame:
    """Recommend courses using sentence transformer embeddings"""
    # Encode the query - this is fast since it's just one item
    query_vec = model.encode([query])
    
    # Calculate similarity with all course embeddings - using precomputed llm_matrix
    similarities = cosine_similarity(query_vec, llm_matrix).flatten()
    
    # Get indices of top matches
    top_indices = similarities.argsort()[::-1]
    
    # Return the matched courses
    return df.iloc[top_indices]


def recommend_highlighted_courses(query: str, top_n: int = 5) -> pd.DataFrame:
    """
    Recommends highlighted courses based on a query, prioritizing top-rated,
    top-viewed, and a combined score. Uses precomputed embeddings.
    """
    # Get base recommendations using our pretrained model
    rec_df = recommend_by_text_similarity(query)
    
    # Join with the needed columns
    rec_df = rec_df[['Title']].merge(df[['Title', 'Category', 'Rating', 'Number of viewers']], on='Title', how='left')

    # Handle potential NaN values
    rec_df['Rating'] = rec_df['Rating'].fillna(0)
    rec_df['Number of viewers'] = rec_df['Number of viewers'].fillna(0)
    
    # Create the three recommendation types
    top_rated = rec_df.sort_values(by='Rating', ascending=False).head(top_n)
    top_viewed = rec_df.sort_values(by='Number of viewers', ascending=False).head(top_n)
    
    # Create combined score using MinMaxScaler
    top_combined = rec_df.copy()
    
    # Check if there are enough rows to perform scaling
    if len(top_combined) >= 2:  # MinMaxScaler needs at least 2 samples
        scaler = MinMaxScaler()
        top_combined[['scaled_rating', 'scaled_views']] = scaler.fit_transform(top_combined[['Rating', 'Number of viewers']])
        top_combined['composite_score'] = top_combined['scaled_rating'] * 0.7 + top_combined['scaled_views'] * 0.3
        top_combined = top_combined.sort_values(by='composite_score', ascending=False).head(top_n)
    else:
        # If not enough rows, just use what we have
        top_combined = top_combined.head(top_n)

    # Format results
    highlighted_recommendations = []
    
    # # Add top rated courses
    # for i in range(min(len(top_rated), top_n)):
    #     highlighted_recommendations.append({
    #         'Query': query,
    #         'Method': 'Top Rated',
    #         'Title': top_rated.iloc[i]['Title'],
    #         'Category': top_rated.iloc[i]['Category'],
    #         'Rating': float(top_rated.iloc[i]['Rating']),
    #         'Viewers': int(top_rated.iloc[i]['Number of viewers'])
    #     })

    # # Add top viewed courses
    # for i in range(min(len(top_viewed), top_n)):
    #     highlighted_recommendations.append({
    #         'Query': query,
    #         'Method': 'Top Viewed',
    #         'Title': top_viewed.iloc[i]['Title'],
    #         'Category': top_viewed.iloc[i]['Category'],
    #         'Rating': float(top_viewed.iloc[i]['Rating']),
    #         'Viewers': int(top_viewed.iloc[i]['Number of viewers'])
    #     })

    # Add top combined score courses
    for i in range(min(len(top_combined), top_n)):
        highlighted_recommendations.append({
            'Query': query,
            'Method': 'Top Combined Score',
            'Title': top_combined.iloc[i]['Title'],
            'Category': top_combined.iloc[i]['Category'],
            'Rating': float(top_combined.iloc[i]['Rating']),
            'Viewers': int(top_combined.iloc[i]['Number of viewers'])
        })

    return pd.DataFrame(highlighted_recommendations)