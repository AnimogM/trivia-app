# Trivia API Reference

## Getting started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, <http://127.0.0.1:5000/>, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

## Error handling

Errors are returned as JSON objects in the following format:

        {
            "success": False,
            "error": 400,
            "message": "bad request"
        }

The API will return three error types when requests fail:

| status code |      message       |
| :---------- | :----------------: |
| 200         |     successful     |
| 400         |    bad request     |
| 404         | resource not found |
| 405         | method not allowed |
| 422         |   unprocessable    |

## Documentation Example

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

example:

`curl -L -X GET 'http://127.0.0.1:5000/categories'`

        {
          "categories":
          {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
            },
          "success": true,
          "total_categories": 6
          }

`GET '/questions'`

- Fetches a list of questions paginated questions
- Request Arguments: page
- Returns: An object with an array of questions that contains an object of question, difficulty and answer key value pair, current category and the categories.

example:

`curl -L -X GET 'http://127.0.0.1:5000/questions'`

        {
          "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
          },
          "current_category": "Science",
          "questions": [
            {
              "answer": "Uruguay",
              "category": 6,
              "difficulty": 4,
              "id": 11,
              "question": "Which country won the first ever soccer World Cup in 1930?"
            }
          ],
          "success": true,
          "total_questions": 13
        }

`DELETE '/questions/<int:question_id>'`

- Deletes question with id.
- Request Arguments: question_id
- Returns: successful with id of deleted question

example:

`curl -L -X DELETE 'http://127.0.0.1:5000/questions/12'`

`POST '/questions'`

- creates a new question on a particular category
- Request Arguments: None
- body: `{ "searchTerm": "who"}`
- Returns: An array of question object whoose question contains the search term based of categories.

example:

`curl -L -X POST 'http://127.0.0.1:5000/questions' \ -H 'Content-Type: application/json' \ --data-raw '{ "question": "what is my name", "answer": "maryam", "category": 5, "difficulty": 2 }'`

        {
            "created": {
                "answer": "maryam",
                "category": 5,
                "difficulty": 2,
                "id": 33,
                "question": "what is my name"
            },
            "success": true,
            "total_questions": 13
        }

`POST '/questions/search'`

- Searchs for questions based on a search term. case insensitive
- Request Arguments: None
- body: `{ "searchTerm": "who"}`
- Returns: An array of question object whoose question contains the search term based of categories.

example:

    `curl -L -X POST 'http://127.0.0.1:5000/questions/search' -H 'Content-Type: application/json' --data-raw '{ "searchTerm": "who"}'`

            {
              "categories": {
              "1": "Science",
              "2": "Art",
              "3": "Geography",
              "4": "History",
              "5": "Entertainment",
              "6": "Sports"
              },
              "current_category": "Science",
              "questions": [
                {
                  "answer": "Uruguay",
                  "category": 6,
                  "difficulty": 4,
                  "id": 11,
                  "question": "Which country won the first ever soccer World Cup in 1930?"
                }
              ],
              "success": true,
              "total_questions": 13
            }

`GET '/categories/<int:category_id>/questions'`

- Fetches all the questiions based on a particular category.
- Request Arguments: category_id
- Returns: An array of questions based on a category containing question, difficulty and answer key value pairs.

example:

`curl -L -X GET 'http://127.0.0.1:5000/categories/1/questions'`

          {
              "current_category": "Science",
              "questions": [
                  {
                      "answer": "The Liver",
                      "category": 1,
                      "difficulty": 4,
                      "id": 20,
                      "question": "What is the heaviest organ in the human body?"
                  }
              ],
              "success": true,
              "total_questions": 2
          }

`POST '/quizzes'`

- Fetches random question to play the game, either all or based on a particular category. It takes in an array of previous questions and the quiz category to fetch all questions based on a category
- Request Arguments: None
- body: `json={ 'previous_questions': [20, 21], 'quiz_category': {'id': 1, 'type': "Science"} })`
- Returns: An object containing question, difficulty and answer key value pairs. returns false if all questions has been fetched

example:

`curl -L -X POST 'http://127.0.0.1:5000/quizzes' \ -H 'Content-Type: application/json' \ --data-raw '{ "previous_questions": [20], "quiz_category": {"id": 1, "type": "Science"} }'`

        {
            "question": {
                "answer": "Alexander Fleming",
                "category": 1,
                "difficulty": 3,
                "id": 21,
                "question": "Who discovered penicillin?"
            },
            "success": true,
            "total_questions": 1
        }
