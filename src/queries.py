import json
import os

import cx_Oracle
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


class OracleDB:
    def __init__(self, queries_path="queries.json"):
        for attr in ["host", "port", "sid", "user", "password"]:
            setattr(self, attr, os.environ[attr])

        self.dsn = cx_Oracle.makedsn(host=self.host, port=self.port, sid=self.sid)

        self.conn = cx_Oracle.connect(
            user=self.user, password=self.password, dsn=self.dsn
        )

        self.queries = self.load_queries(queries_path)

    def load_queries(self, queries_path):
        with open(queries_path, "r") as json_file:
            queries = json.load(json_file)

        return queries

    def get_rucs(self):
        query = self.queries["get_rucs"]
        df = pd.read_sql(query, self.conn)

        return df["RUC"].unique().tolist()

    def get_ruc_info(self, rucs_list):
        rucs = ", ".join(f"'{ruc}'" for ruc in rucs_list)
        query_relato = self.queries["query_info"][0]["query"].replace(
            "{RUCS_VALUE}", rucs
        )
        df = pd.read_sql(query_relato, self.conn)

        relatos = (
            df.groupby("RUC")
            .agg({"CRR_IDHECHO": "first", "RELATO": " ".join})
            .reset_index()["RELATO"]
            .tolist()
        )

        query_cod = self.queries["query_info"][1]["query"].replace("{RUCS_VALUE}", rucs)
        codigos = pd.read_sql(query_cod, self.conn)["COD_DELITO"].tolist()

        dicc = {
            ruc: {"relato": relato, "cod_delito": codigo}
            for ruc, relato, codigo in zip(rucs_list, relatos, codigos)
        }

        return dicc
