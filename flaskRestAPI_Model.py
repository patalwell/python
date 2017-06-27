import json
import sys
import pprint
import requests
import textwrap
from flask import request, current_app as app


class LivyClient:
    def __init__(self):
        self.url = app.config["LIVY_URI"]
        self.headers = {'Content-Type': 'application/json'}


    def __sanitizeFakeJSON(self, fakeJSON):
        return fakeJSON.replace("u\'{","{").replace("}\'","}")\
            .replace("\\n","").replace("\\","")\
            .replace("'{","{").replace("}'","}")


    def create_session(self):
        data={
            "kind": "pyspark",
            "conf": {
                "spark.jars.packages": ("com.amazonaws:aws-java-sdk-pom:1.10.34"
                                        ",com.amazonaws:aws-java-sdk:1.7.4"
                                        ",org.apache.hadoop:hadoop-aws:2.7.1"
                                        ",com.databricks:spark-csv_2.11:1.5.0"
                                        ",com.databricks:spark-xml_2.11:0.4.1")
            }
        }
        r = requests.post(self.url + '/sessions', data=json.dumps(data), headers=self.headers)
        return r.json()

    def post_spark_modules(self, session_id):
        module_payload = request.json['data']
        data = {"code": textwrap.dedent(module_payload)}
        statement_url = self.url + '/sessions/' + str(session_id) + '/statements'
        r = requests.post(statement_url, data=json.dumps(data), headers=self.headers)
        return r.json()
    # Sample module_payload
        # module_payload
        # """
        # from pyspark.sql import SparkSession
        # spark = SparkSession.builder.getOrCreate()
        # from datetime import date, time
        # """


    def get_tables(self,session_id):
        data = {"code": textwrap.dedent("SHOW TABLES;")}
        statement_url = self.url + '/sessions/' + str(session_id) + '/statements'
        r = requests.post(statement_url, data=json.dumps(data), headers=self.headers)
        return r.json()


    def post_tables(self,session_id):
        table_payload = request.json['data']
        data = {"code": textwrap.dedent(table_payload)}
        statement_url = self.url + '/sessions/' + str(session_id) + '/statements'
        r = requests.post(statement_url, data=json.dumps(data), headers=self.headers)
        return r.json()

    def post_query(self,session_id):
        query_payload = request.json['data']
        data = {"code": textwrap.dedent("""
            spark.sql(""" + '\'' + query_payload + '\'' + """).toJSON().take(100)""")}
        statement_url = self.url + '/sessions/' + str(session_id) + '/statements'
        r = requests.post(statement_url, data=json.dumps(data), headers=self.headers)
        return r.json()

    def post_spark_statement_to_session(self,session_id):
        query_payload = request.json['data']
        data = {"code": textwrap.dedent(query_payload)}
        statement_url = self.url + '/sessions/' + str(session_id) + '/statements'
        r = requests.post(statement_url, data=json.dumps(data), headers=self.headers)
        jsonResponse = r.json()
        return jsonResponse

    def get_sessions(self):
        r = requests.get(self.url + '/sessions', headers=self.headers)
        return r.json()

    def get_session_by_id(self, session_id):
        statement_url = self.url + '/sessions/' + str(session_id)
        a = requests.get(statement_url, headers=self.headers)
        return a.json()

    def get_statements_by_session_id(self, session_id):
        statement_url = self.url + '/sessions/' + str(session_id) + '/statements'
        a = requests.get(statement_url, headers=self.headers)
        result = a.json()

        try:
            for index,statement in enumerate(result["statements"]):
                if "data" in statement['output']:
                    # if possible, modify the raw output string from spark console and transform it into proper JSON
                    if (
                        "data" in statement['output'] and
                        "text/plain" in statement['output']['data'] and
                        len(result["statements"][index]['output']['data']['text/plain']) > 0 and
                        result["statements"][index]['output']['data']['text/plain'][0] == "["
                    ):
                        result["statements"][index]['output']['data']['sparkResult'] = []
                        sanitizedResult = self.__sanitizeFakeJSON(statement['output']['data']['text/plain'])
                        sparkResponse = json.loads(sanitizedResult)
                        result["statements"][index]['output']['data']['sparkResult'] = sparkResponse
        except Exception as e: print(e)
        return result

    def get_statement_by_statement_id(self, session_id, statement_id):
        statement_url = self.url + '/sessions/' + str(session_id) + '/statements/' + str(statement_id)
        a = requests.get(statement_url, headers=self.headers)
        result = a.json()

        try:
            result['output']['data']['sparkResult'] = json.loads(result)
        except:
            try:
                # if possible, modify the raw output string from spark console and transform it into proper JSON
                if (
                    "data" in result['output'] and
                    "text/plain" in result['output']['data'] and
                    len(result['output']['data']['text/plain']) > 0 and
                    result['output']['data']['text/plain'][0] == "["
                ):
                    result['output']['data']['sparkResult'] = {}
                    sanitizedResult = self.__sanitizeFakeJSON(result['output']['data']['text/plain'])
                    sparkResponse = json.loads( sanitizedResult )
                    result['output']['data']['sparkResult'] = sparkResponse
            except:
                print "something went wrong"
        return result
