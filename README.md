# Course Recommender

This project is a Course Recommender System built using FastAPI. It provides an API to recommend courses based on user queries, utilizing various recommendation algorithms.

## Project Structure

```
course-recommender
├── src
│   ├── api
│   │   ├── __init__.py
│   │   ├── endpoints.py
│   │   └── models.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── settings.py
│   ├── services
│   │   ├── __init__.py
│   │   └── recommender.py
│   ├── models
│   │   ├── __init__.py
│   │   └── course.py
│   └── main.py
├── tests
│   ├── __init__.py
│   ├── test_api.py
│   └── test_recommender.py
├── requirements.txt
├── Dockerfile
├── .env
├── .gitignore
└── README.md
```

## Requirements

```
fastapi>=0.104.0
uvicorn>=0.24.0
pandas>=2.1.0
scikit-learn>=1.3.0
numpy==1.26.0
python-multipart>=0.0.6
pydantic>=2.5.0
python-dotenv>=1.0.0
requests>=2.31.0
pytest>=7.4.0
httpx>=0.25.0
sentence-transformers>=2.2.2
torch==2.2.2+cpu
```

> **Note**: The system requires at least 2GB RAM for optimal performance, especially during model initialization.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd course-recommender
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the FastAPI application, execute the following command:
```
uvicorn src.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

- **GET /recommend/**: Recommend highlighted courses based on a query.
  - **Query Parameters**:
    - `query`: The search query for course recommendations.
    - `top_n`: The number of recommendations to return (default is 5).

## Testing

To run the tests, use the following command:
```
pytest
```

## Docker

To build the Docker image, run:
```
docker build -t course-recommender .
```

To run the Docker container:
```
docker run -d -p 8000:8000 course-recommender
```

## n8n Integration

To integrate with n8n AI Agent:

1. **Deploy the Course Recommender API** using the Docker instructions above.

2. **Create an AI Agent workflow in n8n** with:
   - Vertex AI Model node (or other compatible model)
   - Simple Memory node
   - Tool node configured for recommend_highlighted

3. **Configure the `recommend_highlighted` tool**:

```json
{
  "name": "recommend_highlighted",
  "description": "Recommends online courses based on a user's query",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "The user's search query"
      },
      "top_n": {
        "type": "integer",
        "description": "Maximum number of courses to recommend"
      }
    },
    "required": ["query"]
  }
}
```

4. **Set the tool implementation** to HTTP Request:
   - Method: GET
   - URL: http://your-api-host:8000/recommend/
   - Query Parameters:
     - query: {{$parameter.query}}
     - top_n: {{$parameter.top_n || 5}}

## Environment Variables

Create a `.env` file in the root directory to set any necessary environment variables for your application.

## Troubleshooting

### Memory Issues

If you encounter "No space left on device" errors:

1. Use a TF-IDF approach instead of sentence-transformers
2. Increase your VM's disk space
3. Clean up unused Docker images: `docker system prune -a`

### Slow Model Initialization

The first startup can be slow as the model initializes. Solutions:

1. Pre-compute embeddings and save to disk
2. Use a smaller model like 'paraphrase-MiniLM-L3-v2'
3. For production, consider a VM with more resources

## License

This project is licensed under the MIT License.