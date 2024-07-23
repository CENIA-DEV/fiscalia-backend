import json
import os

import cx_Oracle
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


class OracleDB:
    def __init__(
        self, queries_path="dicts/queries.json", agrupador_path="dicts/agrupador.json"
    ):
        for attr in ["host", "port", "sid", "user", "password"]:
            setattr(self, attr, os.environ[attr])

        self.dsn = cx_Oracle.makedsn(host=self.host, port=self.port, sid=self.sid)

        self.conn = cx_Oracle.connect(
            user=self.user, password=self.password, dsn=self.dsn
        )

        self.queries = self.load_dicts(queries_path)
        self.agrupador = self.load_dicts(agrupador_path)

    def load_dicts(self, queries_path):
        with open(queries_path, "r") as json_file:
            queries = json.load(json_file)

        return queries

    def get_rucs(self):
        query = self.queries["saf_db"]["get_rucs"]
        df = pd.read_sql(query, self.conn)

        return df["RUC"].unique().tolist()

    def get_ruc_info(self, rucs_list):
        rucs = ", ".join(f"'{ruc}'" for ruc in rucs_list)
        query_relato = self.queries["saf_db"]["query_info"][0]["query"].replace(
            "{RUCS_VALUE}", rucs
        )
        df = pd.read_sql(query_relato, self.conn)
        df["RELATO"] = df["RELATO"].fillna("")

        relatos = (
            df.groupby("RUC")
            .agg({"CRR_IDHECHO": "first", "RELATO": " ".join})
            .reset_index()["RELATO"]
            .tolist()
        )

        query_cod = self.queries["saf_db"]["query_info"][1]["query"].replace(
            "{RUCS_VALUE}", rucs
        )
        query_fec = self.queries["saf_db"]["query_info"][2]["query"].replace(
            "{RUCS_VALUE}", rucs
        )
        codigos = pd.read_sql(query_cod, self.conn)["COD_DELITO"].tolist()
        fechas = pd.read_sql(query_fec, self.conn)["FEC_CAPTURA"].tolist()
        agrupadores = list(map(self.get_agrupador, codigos))

        dicc = {
            ruc: {
                "relato": relato,
                "cod_delito": str(codigo),
                "fecha": fecha,
                "agrupador": agrupador,
            }
            for ruc, relato, codigo, fecha, agrupador in zip(
                rucs_list, relatos, codigos, fechas, agrupadores
            )
        }

        return dicc

    def get_agrupador(self, codigo):
        try:
            return self.agrupador[str(codigo)]["agrupador"]
        except KeyError:
            return ""
