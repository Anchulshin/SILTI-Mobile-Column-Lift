# SocketIO - 채팅기능
from flask_socketio import SocketIO
from flask import Flask, render_template,request,jsonify,Response
import subprocess
import json
import os
import time
import signal

app = Flask(__name__)
app.config['SECRET KEY']='silti'
socketio = SocketIO(app)

serverclient=""
ipjson = {}

########## angle 기능추가 ##########
import wt61cttl_v001
t_angle=wt61cttl_v001.WT61CTTL(0.5)
@app.route('/angle_feed')
def angle_feed():
	def gen_angle():
		angle=str(t_angle.datadp())
		yield angle
	return Response(gen_angle(), mimetype="text")
########## angle 기능추가 ##########

########## height 기능추가 ##########
import board
import busio
import adafruit_vl53l0x
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)
@app.route('/height_feed')
def height_feed():
	def gen_height():
		height = str(vl53.range)
		yield height
	return Response(gen_height(), mimetype="text")
########## height 기능추가 ##########


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


@app.route("/Manual", methods=['POST','GET'])
def Manual_():
	global ipjson
	if request.method=='POST':
		val =request.form
		print(val)
  		#height control
		if val['liftup']=="상대상승":
			height_up(val['synclist'])
		elif val['liftstop']=="상대정지":
			height_stop(val['synclist'])
		elif val['liftdown']=="상대하강":
			height_down(val['synclist'])
		elif val['ang_clock']=='시계방향':
			angle_clock(val['synclist'],val['cntlist'])
		elif val['ang_cnt_clock']=='반시계방향':
			angle_cnt_clock(val['synclist'],val['cntlist'])
		elif val['ang_stop']=='회전정지':
			angle_stop(val['synclist'],val['cntlist'])
		elif val['ab_height_run']=='높이작동':
			absolute_height(val['synclist'])
		elif val['ab_angle_run']=='회전작동':
			absolute_angle(val['cntlist'],val['ab_angle'])
      
		else:
			pass
      
		"""
		liftup = request.form['liftup']
		liftdown = request.form['liftdown']
		liftstop = request.form['liftstop']

		print(liftup)
		"""
		return render_template("Manual.html",  iplistjson=ipjson)


@app.route("/Program")
def Program():
    global ipjson
    df = directory_filelist()
    return render_template("Program.html",  jsonfile={}, iplistjson=ipjson, directory_filelist=df)

@app.route("/Program", methods=['POST','GET'])
def Program_save():
	if request.method=='POST':
		global ipjson
		raw = request.form['raw']
		filename = request.form['filename']
		savefile(raw,filename)
		df = directory_filelist()
		return render_template("Program.html",  jsonfile={}, iplistjson=ipjson, directory_filelist=df)
		
		



@app.route("/Program2", methods=['POST','GET'])
def Program_read():
	if request.method=='POST':
		global ipjson
		readfilename = request.form['read_filename']
		rawjson = readfile(readfilename)
		print(rawjson)
		#df = directory_filelist()
		#print(df)
		return jsonify(rawjson)


@app.route("/Playlist")
def Playlist():
	global ipjson
	global jsonfile
	df = directory_filelist()
	#filename = request.data.decode('utf-8')
	#jsonfile = readfile(filename)
	return render_template("Playlist.html",  iplistjson=ipjson, directory_filelist=df, jsonfile={})

@app.route("/Macro")
def Macro():
	global ipjson
	global jsonfile
	df = directory_filelist()
	#filename = request.data.decode('utf-8')
	#jsonfile = readfile(filename)
	return render_template("Macro.html",  iplistjson=ipjson, directory_filelist=df, jsonfile={})

@app.route('/stopServer', methods=['POST','GET'])
def stopServer():

    return render_template("shutdown.html")
"""

@app.route('/stopServer', methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({ "success": True, "message": "Server is shutting down..." })

"""

########## angle 기능추가 ##########
def angle_clock(ips,cnt_ips):
    print("angle_clock"+ips+cnt_ips)

def angle_cnt_clock(ips,cnt_ips):
    print("angle_cnt_clock"+ips+cnt_ips)

def angle_stop(ips,cnt_ips):
	print("angle_stop"+ips+cnt_ips)

def absolute_angle(ips,cnt_ips):
    print("absolute"+ips+cnt_ips)
########## angle 기능추가 ##########



########## height 기능추가 ##########
def height_up(ips):
    print("height_up"+ips)
    
def height_down(ips):
    print("height_down"+ips)
    
def height_stop(ips):
    print("height_stop"+ips)
    
def absolute_height(ips,ab_height):
    print("absolute"+ips+ab_height)
########## height 기능추가 ##########
















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







#playlist Handling
def savefile(raw,filename):
	print(raw)
	print(filename)
	print(type(raw))
	rawjson = json.loads(raw)
	
	file_path="./playlist/"+str(filename)+".json"
	with open(file_path, 'w') as f:
		json.dump(rawjson,f)	
  
def readfile(filename):
	file_path="./playlist/"+str(filename)
	with open(file_path,'r') as f:
		json_data = json.load(f)
	print(json_data)
	return json_data

def directory_filelist():
	directory="./playlist/"
	file_list = {}
	for i in os.listdir(directory):
		a = os.stat(os.path.join(directory,i))
		file_list[i] = [time.ctime(a.st_atime),time.ctime(a.st_ctime)]
		#file_list.append([i,time.ctime(a.st_atime),time.ctime(a.st_ctime)]) #[file,most_recent_access,created]
	return file_list




    

if __name__ == '__main__':
    socketio.run(app, host="192.168.0.132", debug=True, port=9999)
