extends Node

var url = "http://127.0.0.1:8000/thing"
var data_to_send = {
  "name": "string",
  "id": 0
}

func _ready():
	$HTTPRequest.request_completed.connect(_on_request_completed)
	var json = JSON.stringify(data_to_send)
	var headers = ["Content-Type: application/json"]
	$HTTPRequest.request(url, headers, HTTPClient.METHOD_POST, json)

func _on_request_completed(result, response_code, headers, body):
	var json = JSON.parse_string(body.get_string_from_utf8())
	print(json)
