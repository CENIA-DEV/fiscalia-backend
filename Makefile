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
