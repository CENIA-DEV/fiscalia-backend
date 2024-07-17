.PHONY: run
run:
	uvicorn api:app --reload

.PHONY: test-get-rucs
test-get-rucs:
	curl 127.0.0.1:8000/get_rucs/ -X GET

.PHONY: test-get-user-info
test-get-user-info:
	curl 127.0.0.1:8000/get_user_info/ -X POST -d '{"user": "tgomez"}' -H 'Content-Type: application/json'

.PHONY: test-get-ruc-info
test-get-ruc-info:
	curl 127.0.0.1:8000/get_ruc_info/ -X POST -d '{"rucs_list":["1234-6"]}' -H 'Content-Type: application/json'

.PHONY: test-delete-ruc
test-create-delete-ruc:
	curl 127.0.0.1:8000/get_ruc_info/ -X POST -d '{"rucs_list":["1234-8"]}' -H 'Content-Type: application/json'
	curl 127.0.0.1:8000/create_ruc/ -X POST -d '{"dicc_causa": {"ruc": "1234-8", "relato": "relato de ejemplo", "codigo_delito": "ABC", "sug_curso": "investiga", "sug_precla": "VIF", "curso_accion": "investiga", "precla": "VIF", "comentarios": "comentarios de prueba"}}' -H 'Content-Type: application/json'
	curl 127.0.0.1:8000/get_ruc_info/ -X POST -d '{"rucs_list":["1234-8"]}' -H 'Content-Type: application/json'
	curl 127.0.0.1:8000/delete_rucs/ -X POST -d '{"rucs_list":["1234-8"]}' -H 'Content-Type: application/json'
	curl 127.0.0.1:8000/get_ruc_info/ -X POST -d '{"rucs_list":["1234-8"]}' -H 'Content-Type: application/json'

.PHONY: test-update-ruc
test-update-ruc:
	curl 127.0.0.1:8000/get_ruc_info/ -X POST -d '{"rucs_list":["1234-6"]}' -H 'Content-Type: application/json'
	curl 127.0.0.1:8000/update_ruc/ -X POST -d '{"ruc": "1234-6", "update_dicc": {"codigo_delito": "AB", "sug_curso": "investigar"}}' -H 'Content-Type: application/json'
	curl 127.0.0.1:8000/get_ruc_info/ -X POST -d '{"rucs_list":["1234-6"]}' -H 'Content-Type: application/json'
