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

- **GET /recommend_highlighted/**: Recommend highlighted courses based on a query.
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

## Environment Variables

Create a `.env` file in the root directory to set any necessary environment variables for your application.

## License

This project is licensed under the MIT License.