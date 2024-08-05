.PHONY: run
run:
	uvicorn api:app --reload

.PHONY: test-get-rucs
test-get-rucs:
	curl 127.0.0.1:8000/get_rucs/ -X GET

.PHONY: test-get-ruc-info
test-get-ruc-info:
	curl 127.0.0.1:8000/get_ruc_info/ -X POST -d '{"rucs_list":["1234-6"]}' -H 'Content-Type: application/json'

.PHONY: test-update-ruc
test-update-ruc:
	curl 127.0.0.1:8000/get_ruc_info/ -X POST -d '{"rucs_list":["1234-6"]}' -H 'Content-Type: application/json'
	curl 127.0.0.1:8000/update_ruc/ -X POST -d '{"ruc": "1234-6", "update_dicc": {"codigo_delito": "AB", "sug_curso": "investigar"}}' -H 'Content-Type: application/json'
	curl 127.0.0.1:8000/get_ruc_info/ -X POST -d '{"rucs_list":["1234-6"]}' -H 'Content-Type: application/json'

.PHONY: test-get-grupos
test-get-grupos:
	curl 127.0.0.1:8000/get_grupo_delitos/ -X GET

.PHONY: test-get-estados
test-get-estados:
	curl 127.0.0.1:8000/get_estados/ -X GET

.PHONY: test-get-precla
test-get-precla:
	curl 127.0.0.1:8000/get_curso_precla/ -X GET

.PHONY: test-get-causas
test-get-causas:
	curl 127.0.0.1:8000/get_causas/ -X GET

.PHONY: test-search-rucs
test-search-rucs:
	curl 127.0.0.1:8000/search_rucs/ -X POST -d '{"grupo_delito":"Otros Delitos"}' -H 'Content-Type: application/json'
