# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

To run the server, execute:
```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

### Documentation Trivia API

`GET /api/categories`

- Fetches a list of categories
- Request Arguments: None
- Results: A json contain categories

```javascript
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": True
}
```

`GET /api/questions?page=${integer}`

- Fetches a list of question
- Request Arguments: None
- Results: A json contain questions

  ```javascript
  {
    "success": True,
    "questions": [
      {
        "id": 5,
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
        "answer": "Maya Angelou",
        "difficulty": 2,
        "category": 4
      }
    ],
    "totalQuestions": 19,
    "categories": {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
    },
    "currentCategory": "History"
  }
  ```

`DELETE /api/questions/{id}`

- Deletes question of the given ID if it exists
- Results: total question after delete

  ```javascript
  {
    "success": true,
    "total_questions": 18
  }
  ```

`POST /api/questions`

- Sends a post request to add a new question into DB.
- Request Body:
  ```javascript
  {
    "question": "How much?",
    "answer": "100",
    "difficulty": 1,
    "category": 3
  }
  ```
- Result: List result and total question

  ```javascript
  {
    "success": true, 
    "created": 24, 
    "questions": [
      {
        "answer": "Maya Angelou",
        "category": "4", 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      }, 
      .....
    ], 
    "total_questions": 19
  }
  ```

`POST /api/search`

- Search for one or more questions using the search term.
- Request Body:
  ```javascript
  {
    "searchTerm": "What"
  }
  ```
- Results: List results of question and total questions.

```javascript
{
  "success": True, 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": "4", 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    },
    ....
  ], 
  "total_questions": 6
}
```

`GET /api/categories/{id}/questions`

- Fetches a list of questions by given category id
- Request Arguments: id (interger)
- Results: A list of questions

  ```javascript
  {
    "success": true, 
    "current_category": "Geography", 
    "questions": [
      {
        "answer": "Lake Victoria", 
        "category": "3", 
        "difficulty": 2, 
        "id": 13, 
        "question": "What is the largest lake in Africa?"
      }, 
      {
        "answer": "The Palace of Versailles", 
        "category": "3", 
        "difficulty": 3, 
        "id": 14, 
        "question": "In which royal palace would you find the Hall of Mirrors?"
      }, 
      .....
    ], 
    "total_questions": 3
  }
  ```

`POST /api/quizzes`

- Fetches the next question base on POST request
- Request Body:
  ```javascript
  {
    'previous_questions': 1
    "quiz_category": "category"
  }
  ```
- results: the next question in the same category

  ```javascript
  {
    "question": {
      "answer": "100", 
      "category": "3", 
      "difficulty": 1, 
      "id": 24, 
      "question": "How much?"
    }, 
    "success": True,
    "previousQuestion": 1
  }
  ```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```