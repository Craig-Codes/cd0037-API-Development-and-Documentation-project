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

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

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
- Returns: An object with a two keys, `categories`, that contains an object of `id: category_string` key: value pairs and 'total categories', which contains the int value of the number of categories. .

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}

{
  "total_categories": 6
}
```

`GET '/api/v1.0/questions'`

- Fetches a dictionary of questions, with each question containing the its id, question, answer, category id, and difficulty
- Request Arguments: None
- Returns: An Object with four keys,
  - `questions`, that contains an object of `id: int_id` `question: string_question_content` `answer: string_answer` `category: int_category_id` `difficulty: int_difficulty`.
  - `total_questions` is an object with the integer value of the total number of questions.
  - `categories` is an object containing a list of all category types within the questions.
  - `total_categories` is an object containing the integer value of the number of categories within the questions.

```json
{
 "questions": "Question[]",
  }

{
"total_questions":"5"
}

{
"categories":"Science, Art, Geography, History, Entertainment, Sports"
}

{
  "total_categories":"6"
}
```

`DELETE '/api/v1.0/questions/<question_id>'`

- Deletes a particular question from the API database
- Request Arguments: question_id from query params
- Returns: An object containing three keys,
  - `deleted: int_question_id` - the id of the deleted question
  - `message`, containing the question id which was deleted
  - `questions`, an array of `questions` objects, that contain: `id: int_id` `question: string_question_content` `answer: string_answer` `category: int_category_id` `difficulty: int_difficulty`
  - `total_questions` is an object with the integer value of the total number of questions

```json
{
  "deleted":6

}

{
  "message":"Question 6 deleted",
  "questions": "Question[]",
  }

{
  "total_questions":"26"
}
```

`POST '/api/v1.0/questions/'`

- Adds a new question to the database
- Request Arguments: question, answer, difficulty, and category from request body
- Returns: an object with four properties,
  - `question`: string representing the question text
  - `answer`:string representing the question answer
  - `category`: integer representing the question category
  - `difficulty`: integer representing the question difficulty

```json
{
  "questions": "New Question Text",
  "answer": "New Question Answer",
  "category": "1",
  "difficulty": "1"
}
```

`POST '/api/v1.0/questions/search'`

- API searches through the questions, using pattern matching
- Request Arguments: searchTerm, a string used for pattern matching in the dataset
- Returns: an object of four keys,
  - `questions`, an array of `questions` objects, that contain: `id: int_id` `question: string_question_content` `answer: string_answer` `category: int_category_id` `difficulty: int_difficulty`
  - `total_questions` is an object with the integer value of the total number of questions
  - `categories` is an object containing a list of all category types within the questions.
  - `total_categories` is an object containing the integer value of the number of categories within the questions.

```json
{
  {
"categories":"Science, Art, Geography, History, Entertainment, Sports"
}

{
 "questions": "Question[]",
}

{
"total_questions":"5"
}


{
  "total_categories":"6"
}
```

`GET '/api/v1.0/categories/<id>/questions'`

- Returns all questions of a particular category
- Request Arguments: id, which is used to determine the category of feedback to be returned
- Returns: an object of four keys,
  - `questions`, an array of `questions` objects, that contain: `id: int_id` `question: string_question_content` `answer: string_answer` `category: int_category_id` `difficulty: int_difficulty`
  - `total_questions` is an object with the integer value of the total number of questions
  - `categories` is an object containing a list of all category types within the questions.
  - `total_categories` is an object containing the integer value of the number of categories within the questions.

```json
{
 "questions": "Question[]",
}

{
"total_questions":"5"
}

{
"categories":"Science, Art, Geography, History, Entertainment, Sports"
}

{
  "total_categories":"6"
}
```

`POST '/api/v1.0/quizzes'`

- Starts the quiz, returning a question, a list of previous questions, and the chosen category of the quiz
- Request Arguments:
  - quiz_category - the question category selected
  - previous_questions - a list of previous questions, keeping track of what has already been asked so that questions are not repeated
- Returns: an object of three keys,
  - `question`: string containing the question
  - `previous_questions`, an array of `questions` objects, that contain: `id: int_id` `question: string_question_content` `answer: string_answer` `category: int_category_id` `difficulty: int_difficulty`
  - `category`: integer representing the question category

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
