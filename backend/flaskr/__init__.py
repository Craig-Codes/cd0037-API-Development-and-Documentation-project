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
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={ r"/*": 
                         {"origins": "*"}})
    
    @app.route('/')
    def test():
        print('hello')
        return jsonify({
            "success" : True
        })

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "Content-Type,Authorization,true")
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

 

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.order_by(Category.id).all()

            if len(categories) == 0:
                abort(404)

            # list required to hold all catergories, matching with how front end needs the data
            categories_list = []
            # adding all categories to the dict
            for category in categories:
                categories_list.append(category.type)


            return jsonify({
                "success" : True,
                "categories" : categories_list,
                "total_categories": len(categories_list),
            })

        except:
            abort(404)


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def retrive_questions():

        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)

        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.all()
            # list required to hold all catergories, matching with how front end needs the data
        categories_list = []
            # adding all categories to the dict
        for category in categories:
            categories_list.append(category.type)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(questions),
                "categories": categories_list,
                "total_categories" : len(categories_list)     
            }
        )

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            print(question)

            if question is None:
                abort(404)
            
            else:
                question.delete()

                return jsonify({
                    'success' : True,
                    "deleted" : question_id,
                    'message' : f'Question ${question_id} deleted',
                    "questions": paginate_questions(request, Question.query.order_by(Question.id).all()),
                    "total_questions": len(Question.query.all()),
                })

        except:
            abort(422)
    

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=['POST'])
    def add_question():
        try:
            request_body = request.get_json()
            
            question = request_body.get('question')
            answer = request_body.get('answer')
            difficulty = request_body.get('difficulty')
            category = request_body.get('category')
        
        except:
            abort(422)

        try:
            # add question
            question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
            question.insert()

            return jsonify({
                'success': True,
                'question' : question.question,
                'answer' : question.answer,
                'category' : question.category,
                'difficulty' : question.difficulty
            })

        except:
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
    @app.route("/questions/search", methods=['POST'])
    def search_questions():
        request_body = request.get_json()

        if (request_body is None):
            abort(404)
        else:
            search_term = request_body['searchTerm']

            results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

            paginated_results = paginate_questions(request,results
                                                   )
            categories = Category.query.all()
            # list required to hold all catergories, matching with how front end needs the data
            categories_list = []
            # adding all categories to the dict
            for category in categories:
             categories_list.append(category.type)

            return jsonify(
                {
                "success": True,
                "questions" : paginated_results,
                "total_questions" : len(paginated_results),
                "categories" : categories_list,
                "total_categories" : len(categories_list)   
                })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<id>/questions", methods=['GET'])
    def get_questions_by_category(id):
        # change id to int so that 1 can be added (categories start from 1 not 0)
        converted_id = int(id) + 1
                
        if(converted_id <= 0):
            abort(404)

        categories = Category.query.all()
    
        if(converted_id > len(categories)):
            abort(404)

        try:
            questions = Question.query.filter_by(category=converted_id).all()
            print(questions)
            paginated_questions = paginate_questions(request,questions)


            return jsonify({
                "success": True,
                "questions": paginated_questions,
                "currentCategory": id

            })
        
        except:
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

    @app.route("/quizzes", methods = ["POST"])
    def quiz():

        request_body = request.get_json()

        if (request_body is None):
            abort(422)

        category = request_body['quiz_category']
        previous_questions = request_body['previous_questions']

        print(previous_questions)

        if category["type"] == "click" : # check if catergory is ALL
           questions = Question.query.all()
        else:
           converted_id = int(category["id"]) + 1
           # get question by category, ensuring the question id is not in the previous questions list
           questions = Question.query.filter(Question.id.notin_(previous_questions), Question.category==converted_id).all()
           
           if(len(questions) > 0):
                return jsonify({
                    "success" : True,
                    "question": Question.format(questions[0]),
                    "previousQuestions" : previous_questions,
                    "category":category,
                })      
           else:
                return jsonify({
                    "success" : True,
                    "previousQuestions" : previous_questions,
                    "category":category,
                })     

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )
    
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable Content"}),
            422,
        )
    
    """
    Helper methods
    """
    def paginate_questions(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions

    return app

