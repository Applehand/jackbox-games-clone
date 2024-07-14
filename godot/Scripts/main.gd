extends Node

var session: Session = null
var packed_session: PackedScene = preload("res://Scenes/session.tscn")

@onready var end_session_req: HTTPRequest = $EndSessionReq
@onready var label: Label = $Control/CenterContainer/VBoxContainer/Label
@onready var end_long_polling_button: Button = $Control/CenterContainer/VBoxContainer/CenterContainer/HBoxContainer/EndLongPolling
@onready var start_long_polling_button: Button = $Control/CenterContainer/VBoxContainer/CenterContainer/HBoxContainer/StartLongPolling
@onready var end_session_button: Button = $Control/CenterContainer/VBoxContainer/CenterContainer/HBoxContainer/EndSessionButton
@onready var create_session_button: Button = $Control/CenterContainer/VBoxContainer/CenterContainer/HBoxContainer/CreateSessionButton

func _ready() -> void:
	create_session_button.connect("pressed", create_new_session)
	end_session_button.connect("pressed", end_session)
	start_long_polling_button.connect("pressed", start_long_polling)
	end_long_polling_button.connect("pressed", end_long_polling)

func create_new_session():
	if session:
		print("A session already exists.")
		return

	session = packed_session.instantiate()
	add_child(session)
	label.text = session.id
	session.create_new_server_session()

func start_long_polling():
	if session:
		session.is_long_polling = true
		session.long_poll_server_for_session_updates()
	else:
		print("No session exists to start long polling on.")

func end_long_polling():
	if session:
		if not session.is_long_polling:
			print('Long polling is not active.')
		elif session:
			session.is_long_polling = false
			session.long_poll_server_for_session_updates()
	else:
		print("No session exists to end long polling on.")

func end_session():
	if session:
		var url = "http://127.0.0.1:8000/end-session/" + session.id
		end_session_req.request(url, [], HTTPClient.METHOD_POST)
		print("Session ended.")
		label.text = ""
		session.queue_free()
		session = null
	else:
		print("No session exists to end.")

func test_server_update(session_id):
	var req = HTTPRequest.new()
	add_child(req)
	var url = "http://127.0.0.1:8000/update-client-test/" + session_id
	req.request_completed.connect(test_update_results)
	req.request(url, [], HTTPClient.METHOD_GET)

func test_update_results(result, response_code, headers, body):
	var test_response = JSON.parse_string(body.get_string_from_utf8())
