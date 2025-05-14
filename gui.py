#!/usr/bin/python
import requests
from tkinter import *


root = Tk()
root.configure(bg='black')
root.title("TBT by m00n")

f3 = Frame(root)
f3.pack()
l1 = Label(f3,text="[ ",height=2,fg='blue',bg='black',font=("bold",15))
l1.pack(side=LEFT)
l2 = Label(f3,text="",height=2,fg='lime',bg='black',font=("bold",15))
l2.pack(side=LEFT)
l3 = Label(f3,text=" ]",height=2,fg='blue',bg='black',font=("bold",15))
l3.pack(side=LEFT)

Label(root,text="Bot Token",fg='white',width=10,bg='black').pack(pady=1)
botoken = StringVar(root)
Entry(root,textvariable=botoken,fg='lime',bg='black',width=60,insertbackground='lime').pack(pady=5)

Label(root,text="Chat Id",fg='white',bg='black').pack(pady=1)
chatid = StringVar(root)
Entry(root,textvariable=chatid,fg='lime',bg='black',width=60,insertbackground='lime').pack(pady=5)

Label(root,text="Message",fg='white',bg='black').pack(pady=1)
message = StringVar(root)
Entry(root,textvariable=message,fg='lime',bg='black',width=60,insertbackground='lime').pack(pady=15)

def message_sent():
	l2.configure(text="Message Sent!",fg='lime')
	url1 = f"https://api.telegram.org/bot{botoken.get()}/sendMessage"
	data = f"chat_id={chatid.get()}&text={message.get()}"
	resp = requests.post(url1,params=data).text
	textx.insert(0.0,'\n-------------------\n'+resp)

def check_bot_log():
	l2.configure(text="Chat Logs Retrieved!",fg='magenta')
	url1 = f"https://api.telegram.org/bot{botoken.get()}/getUpdates"
	resp = requests.get(url1).text
	textx.insert(0.0,'\n--------------------\n'+resp)

def check_bot():
	l2.configure(text="Checking The Bot Token!",fg='yellow')
	url1 = f"https://api.telegram.org/bot{botoken.get()}/getMe"
	resp = requests.get(url1).text
	textx.insert(0.0,'\n-------------------\n'+resp)

def add_my_server():
	l2.configure(text="Bot Data To Your Server!",fg='red')
	Label(f2,text="[ Your Server URL To Post Bot Data ]",fg='white',bg='black').pack(pady=1)
	server_url = StringVar(root)
	Entry(f2,textvariable=server_url,width=80).pack(pady=5)
	def post_to_server():
		url1 = f"https://api.telegram.org/bot{botoken.get()}/setWebhook?url={server_url.get()}"
		resp = requests.get(url1).text
		textx.insert(0.0,'\n--------------------\n'+resp)
	Button(f2,text="SEND BOT DATA" , bg='red',fg='white',command=post_to_server).pack()
	
	
f1 = Frame(root,bg='black')
f1.pack()
Button(f1,text="Check Bot Token",width=12,command=check_bot,bg='lime').pack(padx=5,side=LEFT)

Button(f1,text="Check Logs",width=12,command=check_bot_log,bg='lime').pack(padx=5,side=LEFT)

Button(f1,text="Send Bot Data To Server",width=20, command=add_my_server,bg='yellow').pack(padx=5,side=LEFT)

Button(f1,text="Send",width=12,command=message_sent,bg='yellow').pack(pady=20)


textx = Text(root,bg='black',fg='lime',width=130,height=20,insertbackground='lime')
textx.pack(pady=5)

f2 = Frame(root,bg='black')
f2.pack()

root.mainloop()
