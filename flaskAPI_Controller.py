from flask import jsonify
from . import api
from ..models.livy import LivyClient


@api.route('/livy/sessions', methods=['GET'])
def get_session():
    livy = LivyClient()
    return jsonify(livy.get_sessions())


@api.route('/livy/sessions', methods=['POST'])
def create_spark_session():
    livy = LivyClient()
    return jsonify(livy.create_session())


@api.route('/livy/sessions/<int:session_id>', methods=['GET'])
def get_session_by_id(session_id):
    livy = LivyClient()
    return jsonify(livy.get_session_by_id(session_id))


@api.route('/livy/sessions/<int:session_id>/statements', methods=['GET'])
def get_statements_by_session_id(session_id):
    livy = LivyClient()
    return jsonify(livy.get_statements_by_session_id(session_id))


@api.route('/livy/sessions/<int:session_id>/statements', methods=['POST'])
def post_spark_statement_to_session(session_id):
    livy = LivyClient()
    return jsonify(livy.post_spark_statement_to_session(session_id))


@api.route('/livy/sessions/<int:session_id>/sparkmodules', methods=['POST'])
def post_spark_modules(session_id):
    livy = LivyClient()
    return jsonify(livy.post_spark_modules(session_id))


@api.route('/livy/sessions/<int:session_id>/tables', methods=['GET'])
def get_tables(session_id):
    livy = LivyClient()
    return jsonify(livy.get_tables(session_id))


@api.route('/livy/sessions/<int:session_id>/tables', methods=['POST'])
def post_tables(session_id):
    livy = LivyClient()
    return jsonify(livy.post_tables(session_id))


@api.route('/livy/sessions/<int:session_id>/query', methods=['POST'])
def post_query_for_session(session_id):
    livy = LivyClient()
    return jsonify(livy.post_query(session_id))


@api.route('/livy/sessions/<int:session_id>/statements/<int:statement_id>', methods=['GET'])
def get_statement_by_statement_id(session_id, statement_id):
    livy = LivyClient()
    return jsonify(livy.get_statement_by_statement_id(session_id, statement_id))
