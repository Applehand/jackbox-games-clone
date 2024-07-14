extends Node
class_name Session

var id: String = ""
var is_long_polling: bool = false

func _ready() -> void:
	print("New session created.")
	id = gen_session_id()
	$LongHTTPRequest.request_completed.connect(long_poll_server_results)

func gen_session_id() -> String:
	var id = ""
	var chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	var rng = RandomNumberGenerator.new()
	for i in range(4):
		id += chars[rng.randi_range(0, chars.length() - 1)]
	
	return id
	
func create_new_server_session():
	var url = "http://127.0.0.1:8000/create-new-session/" + id
	var req = HTTPRequest.new()
	add_child(req)
	req.request_completed.connect(_on_new_session_created)
	req.request(url, [], HTTPClient.METHOD_POST)

func _on_new_session_created(result, response_code, headers, body):
	var json = JSON.parse_string(body.get_string_from_utf8())

func long_poll_server_for_session_updates():
	var url = "http://127.0.0.1:8000/poll-server-for-updates/" + id
	if is_long_polling:
		$LongHTTPRequest.request(url, [], HTTPClient.METHOD_GET)
		print("Starting long poll.")
	else:
		$LongHTTPRequest.cancel_request()
		print("Ending long poll.")

func long_poll_server_results(result, response_code, headers, body):
	var server_updates = JSON.parse_string(body.get_string_from_utf8())
	if response_code == 200:
		long_poll_server_for_session_updates()
	else:
		print('Issue with long poll.')
