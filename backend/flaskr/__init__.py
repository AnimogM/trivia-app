import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# page paginator
def paginator(selected, request):

    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    result = [data.format() for data in selected]
    return result[start: end]

# format category


def format_category(categories):
    result = {}
    for category in categories:
        result.update({str(category.id): category.type})

    return result


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    # CORS app
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    # Gets all categories

    @app.route('/categories')
    def get_categories():
        try:
            categories = Category.query.order_by(Category.id).all()

            result = format_category(categories)
            return jsonify({'success': True, 'categories': result,
                            'total_categories': len(result)})
        except:
            abort(404)

    # Gets paginated questions
    @app.route('/questions', methods=['GET'])
    def get_questions():
        try:
            questions = Question.query.order_by(Question.id).all()
            categories = Category.query.order_by(Category.id).all()
            formated_categories = format_category(categories)
            result = paginator(questions, request)

            if len(result) == 0:
                abort()

            return jsonify({'success': True, 'questions': result,
                            'total_questions': len(questions), 'current_category': 'Science',
                            'categories': formated_categories})
        except:
            abort(404)

    # Deletes question using a question ID.
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get_or_404(question_id)
            question.delete()

            questions = Question.query.order_by(Question.id).all()
            categories = Category.query.order_by(Category.id).all()
            formated_categories = format_category(categories)
            result = paginator(questions, request)

            if len(result) == 0:
                abort()

            return jsonify({'success': True, 'deleted': question_id,
                            'questions': result, 'total_questions': len(questions),
                            'current_category': formated_categories[str(question.category)],
                            'categories': formated_categories})

        except:
            abort(422)

    # Creates a new question

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        question = body.get('question', None)
        answer = body.get('answer',  None)
        difficulty = body.get('difficulty')
        category = body.get('category')

        try:
            new_question = Question(
                question=question, answer=answer, difficulty=int(difficulty),
                category=int(category))
            new_question.insert()

            questions = Question.query.order_by(Question.id).all()

            return jsonify({'success': True, 'created': new_question.format(),
                            'total_questions': len(questions)})

        except:
            abort(422)

    # Searches questions based on a search term.

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)

        try:
            questions = Question.query.order_by(Question.id).filter(
                Question.question.ilike("%{}%".format(search_term))
            )

            if len(questions.all()) == 0:
                return jsonify(
                    {
                        "success": True,
                        "questions": [],
                        "total_questions": 0,
                        "current_category": ''
                    }
                )

            else:
                categories = Category.query.order_by(Category.id).all()
                formated_categories = format_category(categories)
                result = paginator(questions.all(), request)

                return jsonify(
                    {
                        "success": True,
                        "questions": result,
                        "total_questions": len(result),
                        "current_category": formated_categories[str(
                            questions.first().category)]
                    }
                )

        except:
            abort(422)

    # Gets questions based on category.

    @app.route('/categories/<int:category_id>/questions')
    def get_question(category_id):
        try:
            questions = Question.query.filter_by(
                category=category_id).order_by(Question.id).all()

            result = [question.format()
                      for question in questions]
            current_category = Category.query.get_or_404(category_id)
            return jsonify({'success': True, 'questions': result,
                            'total_questions': len(result),
                            'current_category': current_category.type})
        except:
            abort(404)

    # Gets questions to play the quiz.
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()

        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)

        try:
            if quiz_category['id'] == 0 and quiz_category['type'] == 'click':
                questions = Question.query.all()
            else:
                questions = Question.query.filter(
                    Question.category == int(quiz_category['id'])).all()
            formated_questions = [question.format() for question in questions
                                  if question.id not in previous_questions]

            random_question = []
            if len(formated_questions) == 0:
                random_question = False
            else:
                random_question = random.choice(formated_questions)
            return jsonify({'success': True, 'question': random_question,
                            'total_questions': len(formated_questions)})

        except:
            abort(422)

    # error handlers

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": 'resource not found'
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    return app
