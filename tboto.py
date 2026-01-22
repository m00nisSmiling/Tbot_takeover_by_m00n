#!/usr/bin/python
import requests
from tkinter import *
import sys
import json
import os
from tkinter import filedialog

def upload_file():
	l2.configure(text="uploading file", fg="cyan")

	file_path = filedialog.askopenfilename()
	if not file_path:
		textx.insert(0.0, "-------------------\nFAILED: No file selected\n")
		return

	url = f"https://api.telegram.org/bot{botoken.get()}/sendDocument"

	try:
		with open(file_path, "rb") as f:
			files = {
				"document": f
			}
			data = {
				"chat_id": chatid.get(),
				"caption": os.path.basename(file_path)
			}

			resp = requests.post(url, data=data, files=files).json()

		if resp.get("ok") is True:
			textx.insert(
				0.0,
				f"-------------------\nSUCCESS: File uploaded → {os.path.basename(file_path)}\n"
			)
		else:
			error = resp.get("description", "Unknown error")
			textx.insert(
				0.0,
				f"-------------------\nFAILED: {error}\n"
			)

	except Exception as e:
		textx.insert(
			0.0,
			f"-------------------\nFAILED: {e}\n"
		)

def message_sent():
	l2.configure(text="sending message", fg="lime")

	url = f"https://api.telegram.org/bot{botoken.get()}/sendMessage"
	payload = {
		"chat_id": chatid.get(),
		"text": message.get()
	}

	try:
		resp = requests.post(url, data=payload).json()

		if resp.get("ok") is True:
			textx.insert(0.0, "-------------------\nSUCCESS: Message sent\n")
		else:
			error = resp.get("description", "Unknown error")
			textx.insert(0.0, f"-------------------\nFAILED: {error}\n")

	except Exception as e:
		textx.insert(0.0, f"-------------------\nFAILED: {e}\n")

def check_bot_log():
	url = f"https://api.telegram.org/bot{botoken.get()}/getUpdates"
	resp = requests.get(url).json()

	for update in resp.get("result", []):

		update_id = update.get("update_id")
		print(f"Update ID: {update_id}")

		# ─── MESSAGE UPDATE ─────────────────────────
		if "message" in update:
			msg = update["message"]

			message_id = msg.get("message_id")
			text = msg.get("text", "")

			sender = msg.get("from", {})
			chat = msg.get("chat", {})

			sender_id = sender.get("id")
			sender_is_bot = sender.get("is_bot")
			sender_name = f"{sender.get('first_name','')} {sender.get('last_name','')}".strip()
			sender_username = sender.get("username", "")

			chat_id = chat.get("id")
			chat_type = chat.get("type")
			chat_title = chat.get("title", "")
			chat_name = f"{chat.get('first_name','')} {chat.get('last_name','')}".strip()
			chat_username = chat.get("username", "")

			lastresp = f"""| UpdateId: {update_id}
| MessageId: {message_id}
| SenderId: {sender_id}
| SenderIsBot: {sender_is_bot}
| SenderName: {sender_name}
| SenderUsername: {sender_username}
| ChatType: {chat_type}
| ChatTitle: {chat_title}
| ChatId: {chat_id}
| ChatName: {chat_name}
| ChatUsername: {chat_username}
| Message: {text}"""
			textx.insert(0.0, "\n--------------------\n" + lastresp)

		# ─── MY_CHAT_MEMBER UPDATE ──────────────────
		elif "my_chat_member" in update:
			mcm = update["my_chat_member"]
			chat = mcm.get("chat", {})
			new_status = mcm.get("new_chat_member", {}).get("status")

			print(f"Bot status changed in chat {chat.get('id')} → {new_status}")

def check_bot():
	l2.configure(text="checking bot token", fg="yellow")

	url = f"https://api.telegram.org/bot{botoken.get()}/getMe"
	resp = requests.get(url).json()

	if not resp.get("ok"):
		textx.insert(0.0, "\n-------------------\nInvalid bot token")
		return

	result = resp.get("result", {})

	bot_id = result.get("id")
	is_bot = result.get("is_bot")
	first_name = result.get("first_name", "")
	username = result.get("username", "")
	can_join_groups = result.get("can_join_groups")
	can_read_all = result.get("can_read_all_group_messages")
	inline = result.get("supports_inline_queries")
	business = result.get("can_connect_to_business")
	webapp = result.get("has_main_web_app")
	topics = result.get("has_topics_enabled")

	lastresp = f"""| Bot ID: {bot_id}
| Is Bot: {is_bot}
| Name: {first_name}
| Username: @{username}
| Can Join Groups: {can_join_groups}
| Can Read All Group Messages: {can_read_all}
| Supports Inline Queries: {inline}
| Business Enabled: {business}
| Has Main Web App: {webapp}
| Topics Enabled: {topics}"""

	textx.insert(0.0, "\n-------------------\n" + lastresp)


def add_my_server():
	l2.configure(text="transfer mode", fg="red")

	Label(
		f2,
		text="[ Your Server URL To Post Bot Data ]",
		fg="white",
		bg="black"
	).pack(pady=1)

	server_url = StringVar(root)
	Entry(f2, textvariable=server_url, width=80).pack(pady=5)

	def post_to_server():
		url = f"https://api.telegram.org/bot{botoken.get()}/setWebhook"
		payload = {
			"url": server_url.get()
		}

		try:
			resp = requests.post(url, data=payload).json()

			if resp.get("ok") is True:
				textx.insert(
					0.0,
					"\n--------------------\nSUCCESS: Webhook set successfully\n"
				)
			else:
				error = resp.get("description", "Unknown error")
				textx.insert(
					0.0,
					f"\n--------------------\nFAILED: {error}\n"
				)

		except Exception as e:
			textx.insert(
				0.0,
				f"\n--------------------\nFAILED: {e}\n"
			)

	Button(
		f2,
		text="Transfer",
		bg="red",
		fg="white",
		command=post_to_server
	).pack()
	
root = Tk()
root.title("TBT by m00n")
root.configure(bg="black")
root.geometry("900x650")
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)

status_frame = Frame(root, bg="black")
status_frame.grid(row=0, column=0, sticky="ew", pady=5)

l1 = Label(status_frame, text="| ", fg="white", bg="black", font=("bold", 14))
l1.pack(side=LEFT)
l2 = Label(status_frame, text="Idle", fg="lime", bg="black", font=("bold", 14))
l2.pack(side=LEFT)
l3 = Label(status_frame, text=" |", fg="white", bg="black", font=("bold", 14))
l3.pack(side=LEFT)

input_frame = Frame(root, bg="black")
input_frame.grid(row=1, column=0, sticky="ew", padx=20)
input_frame.grid_columnconfigure(1, weight=1)

Label(input_frame, text="Bot Token", fg="white", bg="black").grid(row=0, column=0, sticky="w")
botoken = StringVar(root)
Entry(
	input_frame,
	textvariable=botoken,
	bg="black",
	fg="lime",
	insertbackground="lime"
).grid(row=0, column=1, sticky="ew", pady=5)

Label(input_frame, text="Chat ID", fg="white", bg="black").grid(row=1, column=0, sticky="w")
chatid = StringVar(root)
Entry(
	input_frame,
	textvariable=chatid,
	bg="black",
	fg="lime",
	insertbackground="lime"
).grid(row=1, column=1, sticky="ew", pady=5)

Label(input_frame, text="Message", fg="white", bg="black").grid(row=2, column=0, sticky="w")
message = StringVar(root)
Entry(
	input_frame,
	textvariable=message,
	bg="black",
	fg="lime",
	insertbackground="lime"
).grid(row=2, column=1, sticky="ew", pady=10)

try:
	botoken.set(sys.argv[1])
except IndexError:
	PREDEFINE_TOKEN = "" 
	botoken.set(PREDEFINE_TOKEN)
	pass

btn_frame = Frame(root, bg="black")
btn_frame.grid(row=2, column=0, pady=10)

Button(btn_frame, text="Check Bot", bg="yellow", width=15, command=check_bot).grid(row=0, column=0, padx=5)
Button(btn_frame, text="Check Logs", bg="yellow", width=15, command=check_bot_log).grid(row=0, column=1, padx=5)
Button(btn_frame, text="Webhook", bg="magenta", width=15, command=add_my_server).grid(row=0, column=2, padx=5)
Button(btn_frame, text="Send Message", bg="lime", width=15, command=message_sent).grid(row=0, column=3, padx=5)
file_frame = Frame(root, bg="black")
file_frame.grid(row=5, column=0, pady=10)

Label(
	file_frame,
	text="File Upload",
	fg="white",
	bg="black",
	font=("bold", 12)
).grid(row=0, column=0, columnspan=2, sticky="w", pady=3)

Button(
	file_frame,
	text="Select & Upload File",
	bg="cyan",
	fg="black",
	width=25,
	command=upload_file
).grid(row=1, column=0, padx=5)

log_frame = Frame(root, bg="black")
log_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)
log_frame.grid_rowconfigure(0, weight=1)
log_frame.grid_columnconfigure(0, weight=1)

scroll = Scrollbar(log_frame)
scroll.grid(row=0, column=1, sticky="ns")

textx = Text(
	log_frame,
	bg="black",
	fg="lime",
	insertbackground="lime",
	yscrollcommand=scroll.set,
	wrap=WORD
)
textx.grid(row=0, column=0, sticky="nsew")
scroll.config(command=textx.yview)

f2 = Frame(root, bg="black")
f2.grid(row=4, column=0, pady=10)

root.mainloop()
