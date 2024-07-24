import json
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


class PostgresDB:
    def __init__(self, queries_path="dicts/queries.json"):
        for attr in ["psql_host", "psql_db", "psql_user", "psql_password"]:
            setattr(self, attr, os.environ[attr])

        self.conn = psycopg2.connect(
            host=self.psql_host,
            database=self.psql_db,
            user=self.psql_user,
            password=self.psql_password,
        )

        self.cursor = self.conn.cursor()
        self.queries = self.load_dicts(queries_path)
        self.keys = [
            "relato",
            "codigo_delito",
            "sug_curso",
            "sug_precla",
            "curso_accion",
            "precla",
            "comentarios",
            "estado",
            "grupo_delito",
            "fecha",
        ]

    def load_dicts(self, queries_path):
        with open(queries_path, "r") as json_file:
            queries = json.load(json_file)

        return queries

    def get_rucs(self):
        query = self.queries["postgres_db"]["get_rucs"]
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results = list(map(lambda x: x[0], results))

        dicc = {"rucs_list": results}

        return dicc

    def get_classified_rucs(self):
        query = self.queries["postgres_db"]["get_classified_rucs"]
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results = list(map(lambda x: x[0], results))

        dicc = {"rucs_list": results}

        return dicc

    def get_user_info(self, user):
        query = self.queries["postgres_db"]["get_user_info"].replace("{USER}", user)
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results = results[0]

        return {
            "user": user,
            "full_name": results[0],
            "password": results[1],
            "fiscalia": results[2],
        }

    def get_ruc_info(self, ruc_list):
        ruc_tuple = tuple(ruc_list)
        query = self.queries["postgres_db"]["get_ruc_info"]
        self.cursor.execute(query, (ruc_tuple,))
        results = self.cursor.fetchall()

        return {causa[0]: dict(zip(self.keys, causa[1:])) for causa in results}

    def create_ruc(self, dicc_causa):
        query = self.queries["postgres_db"]["insert_ruc"]
        values = [dicc_causa[elemento] for elemento in dicc_causa.keys()]
        values_tuple = tuple(values)

        try:
            self.cursor.execute(query, values_tuple)
            self.conn.commit()

            return {"success": True, "message": "Element created succesfully."}
        except Exception as e:
            self.conn.rollback()

            return {"success": False, "message": e}

    def delete_rucs(self, rucs_list):
        query = self.queries["postgres_db"]["delete_rucs"]
        rucs_tuple = tuple(rucs_list)

        try:
            self.cursor.execute(query, (rucs_tuple,))
            self.conn.commit()

            return {"success": True, "message": "Elements deleted successfully"}
        except Exception as e:
            self.conn.rollback()

            return {"success": False, "message": e}

    def update_ruc(self, ruc, update_dicc):
        query = self.queries["postgres_db"]["update_ruc"].replace("{RUC}", ruc)
        update_string = ""

        for key in update_dicc.keys():
            update_string = update_string + f"{key} = '{update_dicc[key]}', "

        update_string = update_string[:-2]
        query = query.replace("{VALUES}", update_string)

        try:
            self.cursor.execute(query)
            self.conn.commit()

            return {"success": True, "message": "Element updated successfully"}
        except Exception as e:
            self.conn.rollback()

            return {"success": False, "message": e}

    def search_rucs(self, search_dicc):
        query = self.queries["postgres_db"]["search_rucs"]

        for key in search_dicc.keys():
            query += f" AND {key} = '{search_dicc[key]}'"

        self.cursor.execute(query)
        results = self.cursor.fetchall()

        return {causa[0]: dict(zip(self.keys, causa[1:])) for causa in results}
