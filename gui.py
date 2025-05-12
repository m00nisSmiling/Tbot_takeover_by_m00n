import requests
from tkinter import *


root = Tk()
root.configure(bg='black')
Label(root,text="Bot Token",fg='white',width=10,bg='black').pack(pady=1)
botoken = StringVar(root)
Entry(root,textvariable=botoken,width=60).pack(pady=5)

Label(root,text="Chat Id",fg='white',bg='black').pack(pady=1)
chatid = StringVar(root)
Entry(root,textvariable=chatid,width=60).pack(pady=5)

Label(root,text="Message",fg='white',bg='black').pack(pady=1)
message = StringVar(root)
Entry(root,textvariable=message,width=60).pack(pady=15)

def message_sent():

	url1 = f"https://api.telegram.org/bot{botoken.get()}/sendMessage"
	data = f"chat_id={chatid.get()}&text={message.get()}"
	resp = requests.post(url1,params=data).text
	textx.insert(0.0,'\n-------------------\n'+resp)

def check_bot_log():
	url1 = f"https://api.telegram.org/bot{botoken.get()}/getUpdates"
	resp = requests.get(url1).text
	textx.insert(0.0,'\n--------------------\n'+resp)

def check_bot():
	url1 = f"https://api.telegram.org/bot{botoken.get()}/getMe"
	resp = requests.get(url1).text
	textx.insert(0.0,'\n-------------------\n'+resp)

def add_my_server():
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


textx = Text(root,bg='black',fg='lime',width=100,height=20)
textx.pack(pady=5)

f2 = Frame(root,bg='black')
f2.pack()

root.mainloop()
