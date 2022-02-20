# SocketIO - 채팅기능
from flask_socketio import SocketIO
from flask import Flask, render_template,request
import subprocess
import json
import os
import time

app = Flask(__name__)
app.config['SECRET KEY']='silti'
socketio = SocketIO(app)

serverclient=""
ipjson = {}




@app.route("/")
def index():
	return render_template("index.html")



@app.route("/test")
def test():
	return render_template("test.html")


@app.route('/', methods=['POST','GET'])
def index2():
	if request.method=='POST':
		passwd = request.form['PW']
		print(passwd)
		if passwd=="0151":
			return render_template("ServerClient.html")
		else:
			return render_template("index.html")

@app.route("/ServerClient")
def ServerClient():
    return render_template("ServerClient.html")
#서버와 클라이언트 지정작업

@app.route('/ServerClient', methods=['POST','GET'])
def APIP_():
	if request.method=='POST':
		APIP = request.form['APIP']
		ipdata = iplist(APIP)
		return render_template("RES_ServerClient.html", data=json.dumps(ipdata), myip="192.168.0.132")
#서버와 클라이언트 지정이 완료됨

"""
@app.route("/ServerClient_CON")
def ServerClient_CON():
    return render_template("ServerClient_CON.html")
"""
@app.route('/ServerClient_CON', methods=['POST','GET'])
def ServerClient_CON():
	if request.method=='POST':
		global serverclient
		serverclient = request.form['serverclient']
		global ipjson
		print("serverclient:",serverclient)
		ipjson = save_communication_set(serverclient)
		return render_template("ServerClient_CON.html", iplistjson=ipjson)




@app.route("/Manual")
def Manual():
    global ipjson
    return render_template("Manual.html",  iplistjson=ipjson)



def save_communication_set(serverclient):
	f=open("MCLIP_TopDown.txt","w")
	ipall = serverclient.split(',')
	global ipjson
	ipjson['server'] = ipall[0]
	ipjson['client'] = ipall[1:len(ipall)]
	f.write(str(ipjson))
	f.close()
	return ipjson



def iplist(apip):
	fiplist=open('iplist.txt', 'w')
	outdata = subprocess.check_output(['sudo nbtscan -s : '+apip+'/24'],shell=True, encoding='utf-8')
	fiplist.write(outdata)
	fiplist=open('iplist.txt', 'r')
	lines = fiplist.readlines()
	ipdata = dict()
	print("Numbers:",len(lines))
	print("\n")
	for line in lines:

		scanone = line.split(':', maxsplit=4)

		ipdata[scanone[0]]={"ip":scanone[0],"NetBiosName":scanone[1].replace(" ",""),"MACAddress":scanone[4].replace("\n","")}
	print("iplist:",ipdata)
	print("\n")
	print(ipdata.keys())
	print("\n")
	print(ipdata.values())
	print("\n")
	return ipdata

	

if __name__ == '__main__':
    socketio.run(app, host="192.168.0.132", debug=True, port=9999)
