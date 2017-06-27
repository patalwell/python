import json
import requests
import textwrap
from flask import request


class LivyClient(object):
    """
    This is an API model for making a connection to the Livy API and allows the user to define a custom host url

    Attributes:
        url: a user defined host for the livy server, default is http://localhost:8998
        headers: defines our content type as JSON
    """
    def __init__(self, url):
        """inits a connection to the Livy server with a user defined url,
        e.g. livy = LivyClient("http://localhost:8988")"""
        self.url = url
        self.headers = {'Content-Type': 'application/json'}

    def create_session(self):
        """posts session data to the Livy server
        in this case we are telling livy we want to use pyspark and the AWS (s3a://location-of-data) protocol packages
        these packages give the user the ability to load data from S3

        arg:
            n/a

        return:
            A JSON object :
                {
                    "appId": null,
                    "appInfo": {
                    "driverLogUrl": null,
                    "sparkUiUrl": null
                    },
                    "id": 1,
                    "kind": "pyspark",
                    "log": [],
                    "owner": null,
                    "proxyUser": null,
                    "state": "starting"
                }
        """
        data = {"kind": "pyspark", "conf": {"spark.jars.packages": "com.amazonaws:aws-java-sdk-pom:1.10.34,com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.1"}}
        r = requests.post(self.url + '/sessions', data=json.dumps(data), headers=self.headers)
        return r.json()

    def post_spark_modules(self, session_id):
        """submits a JSON object module_payload to the livy server
        users can define there spark packages

        arg:
            session_id: the session id from the create_session() JSON object
            module_payload: {"data": "from pyspark.sql import SparkSession"}

        return:
            A JSON object :
                {
                    "id": 0,
                    "output": null,
                    "state": "waiting"
                }
        """
        module_payload = request.json['data']
        data = {"code": textwrap.dedent(module_payload)}
        statement_url = self.url + '/sessions/{}/statements'.format(session_id)
        r = requests.post(statement_url, data=json.dumps(data), headers=self.headers)
        return r.json()

    def get_tables(self, session_id):
        data = {"code": textwrap.dedent("SHOW TABLES;")}
        statement_url = self.url + '/sessions/{}/statements'.format(session_id)
        r = requests.post(statement_url, data=json.dumps(data), headers=self.headers)
        return r.json()

    def post_tables(self, session_id):
        """submits a JSON object table_payload to the livy server
        users can define temp tables one payload at a time

        arg:
            session_id: the session id from the create_session() JSON object
            table_payload: {"data": "df_customer = spark.read.parquet('s3a://aqapop/DataAlgebraData/tpch/1G/16/customer.parquet')"}
                        {"data": "df_customer = df_customer.registerTempTable('customer')"}

        return:
           {
            "id": 1,
            "output": null,
            "state": "running"
            }
        """
        table_payload = request.json['data']
        data = {"code": textwrap.dedent(table_payload)}
        statement_url = self.url + '/sessions/{}/statements'.format(session_id)
        r = requests.post(statement_url, data=json.dumps(data), headers=self.headers)
        return r.json()

    def post_query(self, session_id):
        """Posts a query to the livy server
         arg:
             session_id: the session id from the create_session() JSON object
             query_payload: {"data": "SELECT * FROM customer"}
         return:
            {
            "id": 1,
            "output": null,
            "state": "running"
            }
         """
        query_payload = request.json['data']
        data = {"code": textwrap.dedent("""
            spark.sql(""" + '\'' + query_payload + '\'' + """).toJSON().take(100)""")}
        statement_url = self.url + '/sessions/{}/statements'.format(session_id)
        r = requests.post(statement_url, data=json.dumps(data), headers=self.headers)
        return r.json()

    def post_spark_statement_to_session(self, session_id):
        """Posts a statement to the livy server with a session_id
            arg:
                session_id: the session id from the create_session() JSON object
                query_payload: {"data" : "Spark command"}
            return:
            {
            "id": 1,
            "output": null,
            "state": "running"
            }
            """
        query_payload = request.json['data']
        data = {"code": textwrap.dedent(query_payload)}
        statement_url = self.url + '/sessions/{}/statements'.format(session_id)
        r = requests.post(statement_url, data=json.dumps(data), headers=self.headers)
        jsonResponse = r.json()
        return jsonResponse

    def get_sessions(self):
        """
        Returns all the sessions the user has created

        arg:
            session_id: the session id from the create_session() JSON object

        returns:
            {
                "appId": null,
                "appInfo": {
                "driverLogUrl": null,
                "sparkUiUrl": null
                },
                "id": 0,
                "kind": "pyspark",
                "log": [],
                "owner": null,
                "proxyUser": null,
                "state": "idle"
            }
        """
        r = requests.get(self.url + '/sessions', headers=self.headers)
        return r.json()

    def get_session_by_id(self, session_id):
        """
         Returns the sessions the user has created by session id

         arg:
             session_id: the session id from the create_session() JSON object

         returns:
          {
            "appId": null,
            "appInfo": {
            "driverLogUrl": null,
            "sparkUiUrl": null
            },
            "id": 0,
            "kind": "pyspark",
            "log": [],
            "owner": null,
            "proxyUser": null,
            "state": "idle"
          }
         """
        statement_url = self.url + '/sessions/{}'.format(session_id)
        a = requests.get(statement_url, headers=self.headers)
        return a.json()

    def get_statements_by_session_id(self, session_id):
        """
        Returns the statements by session id the user has created

        arg:
            session_id: the session id from the create_session() JSON object

        returns:
            {
            "statements": [],
            "total_statements": 0
            }
        """
        statement_url = self.url + '/sessions/{}/statements'.format(session_id)
        a = requests.get(statement_url, headers=self.headers)
        result = a.json()
        try:
            for index,statement in enumerate(result["statements"]):
                # initialize a spark result that is an empty list, even when spark returns no result.
                result["statements"][index]['output']['data']['sparkResult'] = []
                sanitizedResult = statement['output']['data']['text/plain'].replace("u\'{","{").replace("}\'","}")
                # if possible, modify the raw output string from spark console and transform it into proper JSON
                if (
                    "data" in statement['output'] and
                    "text/plain" in statement['output']['data'] and
                    len(statement['output']['data']['text/plain']) > 0 and
                    statement['output']['data']['text/plain'][0] == "["
                ):
                    sparkResponse = json.loads(sanitizedResult)
                    # result["statements"][index]['output']['data']['text/plain'] = sparkResponse
                    result["statements"][index]['output']['data']['sparkResult'] = sparkResponse
        except:
            print "Returning the original unmodified response from Livy"
        return result

    def get_statement_by_statement_id(self, session_id, statement_id):
        statement_url = self.url + '/sessions/{}/statements/{}'.format(session_id, statement_id)
        a = requests.get(statement_url, headers=self.headers)
        result = a.json()
        try:
            # initialize a spark result that is an empty object, even when spark returns no result.
            result['output']['data']['sparkResult'] = {}
            sanitizedResult = result['output']['data']['text/plain'].replace("u\'{","{").replace("}\'","}")
            # if possible, modify the raw output string from spark console and transform it into proper JSON
            if (
                "data" in statement['output'] and
                "text/plain" in statement['output']['data'] and
                len(statement['output']['data']['text/plain']) > 0 and
                statement['output']['data']['text/plain'][0] == "["
            ):
                sparkResponse = json.loads( sanitizedResult )
                # result['output']['data']['text/plain'] = sparkResponse
                result['output']['data']['sparkResult'] = sparkResponse
        except:
            print "Returning the original unmodified response from Livy"
        return result
