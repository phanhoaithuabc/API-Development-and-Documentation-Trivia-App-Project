import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    """
    @TODO: Set up CORS. Allow '*' for origins. 
    Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/api/categories")
    def get_categories():
        try:
            categories = Category.query.all()
            result = dict()
            for item in categories:
                result[item.id] = item.type

            return jsonify({
                'success': True,
                'categories': result
            })
        except Exception as e:
            print('error:', e)
            abort(404)

    def paginate_questions(request, input):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = [question.format() for question in input]
        final_questions = questions[start:end]
        return final_questions

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of 
    the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/api/questions')
    def get_questions():
        try:
            questions = Question.query.order_by(Question.id).all()
            result_questions = paginate_questions(request, questions)
            if (len(result_questions) == 0): 
                abort(404)

            categories = Category.query.all()
            result_categories = {}
            for item in categories:
                result_categories[item.id] = item.type

            return jsonify({
                'success': True,
                'questions': result_questions,
                'total_questions': len(questions),
                'categories': result_categories,
                'currentCategory': any(category.format() for category in categories)
            })
        except Exception as e:
            print('error:', e)
            abort(404)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, 
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    
    @app.route('/api/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            question = Question.query.get(id)

            if not question:
                abort(404)

            question.delete()

            remaining_questions = Question.query.all()

            return jsonify({
                'success': True,
                'total_questions': len(remaining_questions)
            })

        except Exception as e:
            print('Error:', e)
            abort(500)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will 
    appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/api/questions", methods=['POST'])
    def add_question():
        try:
            body = request.get_json()
            question = body.get('question')
            answer = body.get('answer')
            category = body.get('category')
            difficulty = body.get('difficulty')
            if question is None or answer is None:
                abort(422)
            question_object = Question(question=question, 
                                       answer=answer, 
                                       category=category, 
                                       difficulty=difficulty)
            question_object.insert()
            selection = Question.query.order_by(Question.id).all()
            result_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'created': question_object.id,
                'questions': result_questions,
                'total_questions': len(selection)
            })
        except Exception as e:
            print('error: ', e)
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/api/search", methods=['POST'])
    def search_question():
        search = request.get_json().get('searchTerm')
        questions = Question.query.filter(Question.question.ilike('%'+search+'%')).all()
        try:
            result_questions = paginate_questions(request, questions)
            return jsonify({
                'success': True,
                'questions': result_questions,
                'total_questions': len(questions)
            })
        except Exception as e:
            print('error: ',e)
            abort(404)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/api/categories/<int:id>/questions")
    def get_questions_by_category(id):
        category = Category.query.filter_by(id=id).one_or_none()
        try:
            questions_by_category = Question.query.filter_by(category=str(id)).all()
            result_questions = paginate_questions(request, questions_by_category)
            return jsonify({
                'success': True,
                'questions': result_questions,
                'total_questions': len(questions_by_category),
                'current_category': category.type
            })
        except Exception as e:
            print('error: ', e)
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/api/quizzes', methods=['POST'])
    def get_question_to_play_quiz():
        body = request.get_json()
        quiz_category = body.get('quiz_category', {})
        previous_questions = body.get('previous_questions', [])

        try:
            if quiz_category.get('id') == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter_by(category=quiz_category.get('id')).all()

            if not questions:
                abort(404)

            available_questions = [q for q in questions if q.id not in previous_questions]

            if not available_questions:
                return jsonify({
                    'success': True,
                    'message': 'No more questions available',
                    'question': None,
                    'previousQuestions': previous_questions
                })

            next_question = random.choice(available_questions)

            return jsonify({
                'success': True,
                'question': {
                    'id': next_question.id,
                    'question': next_question.question,
                    'answer': next_question.answer,
                    'category': next_question.category,
                    'difficulty': next_question.difficulty
                },
                'previousQuestions': previous_questions
            })

        except Exception as e:
            print('Error: ', e)
            abort(500)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            'error': 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            "success": False,
            'error': 404,
            "message": "Page not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_resource(error):
        return jsonify({
            "success": False,
            'error': 422,
            "message": "Unprocessable resource"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            'error': 500,
            "message": "Internal server error"
        }), 500

    @app.errorhandler(405)
    def invalid_method(error):
        return jsonify({
            "success": False,
            'error': 405,
            "message": "Invalid method!"
        }), 405

    return app
