from src.postgres import PostgresDB
from src.queries import OracleDB

BASE_PATH = "src/dicts/"


def update_rucs(oracle, postgres):
    oracle_rucs = oracle.get_rucs()
    postgres_rucs = postgres.get_rucs()
    classified_rucs = postgres.get_classified_rucs()

    for ruc in oracle_rucs:
        ruc_info = oracle.get_ruc_info([ruc])

        if ruc_info == {}:
            continue

        if (
            ruc not in postgres_rucs["rucs_list"]
            and ruc not in classified_rucs["rucs_list"]
        ):
            relato = ruc_info[ruc]["relato"]

            if len(relato) > 10000:
                relato = relato[:10000]

            dicc_causa = {
                "ruc": ruc,
                "relato": relato,
                "codigo_delito": ruc_info[ruc]["cod_delito"],
                "sug_curso": inf_sug_curso(relato),
                "sug_precla": inf_sug_precla(relato),
                "curso_accion": "",
                "precla": "",
                "comentarios": "",
                "estado": "Sin Preclasificar",
                "grupo_delito": ruc_info[ruc]["agrupador"],
                "fecha": ruc_info[ruc]["fecha"].strftime("%Y-%m-%d %H:%M:%S"),
            }

            success = postgres.create_ruc(dicc_causa)

            if success["success"]:
                print(f"Created ruc: {ruc}")
            else:
                print(f"Failed to create ruc: {ruc}. Error: {success['message']}")

        else:
            ruc_postgres_info = postgres.get_ruc_info([ruc])

            if (
                not ruc_postgres_info[ruc]["codigo_delito"]
                == ruc_info[ruc]["cod_delito"]
            ):
                update_dicc = {
                    "codigo_delito": ruc_info[ruc]["cod_delito"],
                    "grupo_delito": ruc_info[ruc]["agrupador"],
                }

                postgres.update_ruc(ruc, update_dicc)
                print(f"Updated ruc: {ruc}")
            else:
                print(f"Skipping ruc: {ruc}")


def inf_sug_curso(relato):
    return ""


def inf_sug_precla(relato):
    return ""


def main():
    oracle = OracleDB(
        queries_path=f"{BASE_PATH}queries.json",
        agrupador_path=f"{BASE_PATH}agrupador.json",
    )
    postgres = PostgresDB(queries_path=f"{BASE_PATH}queries.json")

    update_rucs(oracle, postgres)


if __name__ == "__main__":
    main()
