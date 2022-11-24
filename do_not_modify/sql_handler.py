from typing import Any

import pandas
import pymysql
import logging
import sshtunnel
from pandas import DataFrame
from pymysql import Connection
from sshtunnel import SSHTunnelForwarder, BaseSSHTunnelForwarderError
from credentials import credentials
from sql_to_json_converter import SQLToJSONConverter


class SSHTunnelHandler:
    def __init__(self, app, credentials):
        self.app = app
        self.credentials = credentials
        self.tunnel = None

    def open_ssh_tunnel(self, verbose=False) -> tuple[SSHTunnelForwarder, str]:
        try:
            if verbose:
                sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG
            self.tunnel = SSHTunnelForwarder(
                (self.credentials["ssh_host"], 22),
                ssh_username=self.credentials["ssh_username"],
                ssh_password=self.credentials["ssh_password"],
                remote_bind_address=('127.0.0.1', 3306)
            )
            self.tunnel.start()
            self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:{}/moodle'.format(
                self.tunnel.local_bind_port)
            return self.tunnel, "Task ['open ssh tunnel']: Successful"
        except BaseSSHTunnelForwarderError:
            return self.tunnel, "Task ['open ssh tunnel']: Failed to open SSH tunnel"

    def close_ssh_tunnel(self) -> str:
        try:
            self.tunnel.close()
            return "Task ['close ssh tunnel']: Successful"
        except Exception as e:
            return "Task ['close ssh tunnel']: Failed; Error: " + e.__str__()


class SQLConnectionHandler:
    def __init__(self, credentials):
        self.credentials = credentials
        self.connection = None

    def mysql_connect(self, tunnel) -> tuple[Connection, str]:
        try:
            self.connection = pymysql.connect(
                host='127.0.0.1',
                user=self.credentials["database_username"],
                passwd=self.credentials["database_password"],
                db=self.credentials["database_name"],
                port=tunnel.local_bind_port
            )
            return self.connection, "Task ['connect to sql']: Successful"
        except BaseException as e:
            return self.connection, "Task [connect to sql]: Failed; Error: " + e.__str__()

    def mysql_disconnect(self) -> str:
        try:
            self.connection.close()
            return "Task ['close sql connection']: Successful"
        except Exception as e:
            return "Task ['close sql connection']: Failed; Error: " + e.__str__()


class QueryHandler:
    def __init__(self, query):
        self.query = query
        self.json_converter = SQLToJSONConverter()

    # noinspection PyMethodMayBeStatic
    def sql_to_pd_dataframe(self, data_as_sql, sql_cursor):
        return pandas.DataFrame(data_as_sql,
                                columns=list(map(lambda x: x[0],
                                                 sql_cursor.description)))

    # noinspection PyMethodMayBeStatic
    def sql_to_json(self, data_as_sql, sql_cursor):
        return self.json_converter.convert_to_json(data_as_sql, sql_cursor) if len(
            data_as_sql) > 0 else None

    def run_query(self, conn):
        try:
            sql_cursor = conn.cursor()
            sql_cursor.execute(self.query)
            result = sql_cursor.fetchall()
            if result == ():
                return [], None, None, "Task ['run query]: Successful BUT returned empty data"
            return self.sql_to_json(result, sql_cursor), self.sql_to_pd_dataframe(result,
                                                                                  sql_cursor), sql_cursor, "Task [" \
                                                                                                           "'run " \
                                                                                                           "query']: " \
                                                                                                           "Successful "
        except Exception as e:
            return [], None, None, "Task ['run query']: Failed; Error: " + e.__str__()


class SQLHandlerFacade:
    def __init__(self, app, query) -> None:
        self.app = app
        self.query = query
        self.ssh_tunnel_handler = SSHTunnelHandler(app, credentials=credentials)
        self.sql_connection_handler = SQLConnectionHandler(credentials=credentials)
        self.query_handler = QueryHandler(query)

    def operation(self) -> tuple[dict[str, list | None | list[str | Any]], DataFrame]:
        results = ["SQL handler facade initializes subsystems..."]
        tunnel, log = self.ssh_tunnel_handler.open_ssh_tunnel()
        results.append(log)
        sql_conn, log = self.sql_connection_handler.mysql_connect(tunnel)
        results.append(log)
        query_result_as_json, query_result_as_pd_dataframe, sql_cursor, log = self.query_handler.run_query(
            conn=sql_conn)
        results.append(log)
        log = self.sql_connection_handler.mysql_disconnect()
        results.append(log)
        log = self.ssh_tunnel_handler.close_ssh_tunnel()
        results.append(log)
        results.append("SQL handler facade operation END")
        return {"log": [logs for logs in results],
                "result": query_result_as_json}, query_result_as_pd_dataframe
