import json
from app.api.v1 import blueprint_v1
from flask import make_response, jsonify, request
from app.api.v1.chat.models import Question
from app.extensions import db


@blueprint_v1.route('/faqs', methods=["POST"])
def create_question():
    details = request.get_json()
    question = details['question']
    answer = details['answer']

    new_question = Question(question=question, answer=answer)
    db.session.add(new_question)
    db.session.commit()

    return dict(new_question.as_dict())


@blueprint_v1.route('/faqs', methods=["GET"])
def get_faqs():
    return make_response(jsonify(
        {
            "questions": json.loads(get_all_faqs())
        }
    ))


@blueprint_v1.route('/chat', methods=["GET", "POST"])
def chat():
    return make_response(jsonify(
        {
            "question": "Hey! I'm Arrotech. Happy to chat with you. What would you like to do today?",
            "questions": json.loads(get_all_faqs())
        }
    ))


@blueprint_v1.route('/chat/<choice>', methods=["GET", "POST"])
def answers(choice):
    faqs = json.loads(get_all_faqs())
    qas = []
    for faq in faqs:
        if faq['question'] == choice:
            qas.append(faq)
    return make_response(jsonify(
        {
            "message": "Frequently asked questions!",
            "questions": qas
        }
    ))


@blueprint_v1.route('/faqs/delete_all', methods=["DELETE"])
def delete_all_faqs():
    faqs = Question.query.all()
    for faq in faqs:
        db.session.delete(faq)
        db.session.commit()
    return make_response(jsonify(
        {
            "message": "NO CONTENT!",
            "status": 204
        }
    ), 204)


def get_all_faqs():
    faqs = Question.query.all()
    questions = []
    for faq in faqs:
        questions.append(faq.as_dict())
    return json.dumps(questions, default=str)
