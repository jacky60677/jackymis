import requests
from bs4 import BeautifulSoup

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


from flask import Flask, render_template , request , make_response , jsonify
from datetime import datetime, timezone, timedelta


app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>陳丞彥Python網頁</h1>"
    homepage += "<a href=/mis target = _blank>MIS</a><br>"
    homepage += "<a href=/today target = _blank>顯示日期時間</a><br>"
    homepage += "<a href=/welcome?nick=Jacky target = _blank>傳送使用者暱稱</a><br>"
    homepage += "<a href=/myself target = _blank>個人網頁</a><br>"
    homepage += "<a href=/account target = _blank>帳號密碼</a><br>"
    homepage += "<a href=/text target = _blank>興趣何倫碼測驗結果</a><br>"
    homepage += "<a href=/jobsearch target = _blank>個人求職自傳履歷網頁</a><br>"
    homepage += "<a href=/search target = _blank>選修課程查詢</a><br>"
    homepage += "<a href=/movienews>讀取開眼電影即將上映影片，寫入Firestore</a><br>"
    homepage += "<a href=/movie target = _blank>電影查詢</a><br>"
    homepage += "<a href=/webhook target = _blank>webdemo</a><br>"
    return homepage




@app.route("/mis")
def course():
    return "<h1>資訊管理學院</h1>"	

@app.route("/today")
def today():
	tz = timezone(timedelta(hours=+8))
	now = datetime.now(tz)
	return render_template("today.html", datetime = str(now))	

@app.route("/welcome",methods=["GET", "POST"])
def welcome():
	user = request.values.get("nick")
	return render_template("welcome.html", name = user)	

@app.route("/myself")
def myself():
	return render_template("myself.html")	

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd 
        return result
    else:
        return render_template("account.html")

@app.route("/text")
def text():
	return render_template("text.html")

@app.route("/jobsearch")
def jobsearch():
	return render_template("jobsearch.html")

@app.route("/search" , methods=["GET", "POST"])
def search():
	collection_ref = db.collection("111")
	docs = collection_ref.get()
	if request.method == "POST":
		classkeyword = request.form["classkeyword"]
		teacherkeyword = request.form["teacherkeyword"]
		#Cond = input(keyword) 
	
		Result = ""

		for doc in docs:
			r = doc.to_dict()

			if classkeyword in r["Course"] and teacherkeyword in r["Leacture"]:
				Result += "課程代碼 : " + r["Code"] + "<br>" + "課程名稱：" + r["Course"] + "<br>" +"，教師姓名：" + r["Leacture"]+ "<br>" +"，上課時間 : " + r["Time"]+ "<br>" +"，在"+r["Room"]+"上課" + "<br>"
		return Result
	else:
		return render_template("search.html")

	if Result == " " :
		Result = "Sorry"

@app.route("/movienews")
def movienews():
	url = "http://www.atmovies.com.tw/movie/next/"
	Data = requests.get(url)
	Data.encoding = "utf-8"
	sp = BeautifulSoup(Data.text, "html.parser")
	result=sp.select(".filmListAllX li")
	lastUpdate = sp.find("div", class_="smaller09").text[5:]

	for item in result:
		picture = item.find("img").get("src").replace(" ", "")
		title = item.find("div", class_="filmtitle").text
		movie_id = item.find("div", class_="filmtitle").find("a").get("href").replace("/", "").replace("movie", "")
		hyperlink = "http://www.atmovies.com.tw" + item.find("div", class_="filmtitle").find("a").get("href")
		show = item.find("div", class_="runtime").text.replace("上映日期：", "")
		show = show.replace("片長：", "")
		show = show.replace("分", "")
		showDate = show[0:10]
		showLength = show[13:]
		images = item.select("img")
        
		if len(images) == 1:
			rate = "目前尚無分級資訊"
		else:
			rate = images[1].get("src")
			if rate == "/images/cer_G.gif":
				rate = "普遍級(一般觀眾皆可觀賞)"
			elif rate == "/images/cer_P.gif":
				rate = "輔導級(未滿十二歲之兒童不得觀賞)"
			elif rate == "/images/cer_F2.gif":
				rate = "保護級(未滿六歲之兒童不得觀賞，六歲以上未滿十二歲之兒童須父母、師長或成年親友陪伴輔導觀賞)"
			elif rate == "/images/cer_F5.gif":
				rate = "輔導級(未滿十五歲之人不得觀賞)"
			elif rate == "/images/cer_R.gif":
				rate = "限制級(未滿十八歲之人不得觀賞)"
		#print("電影分級:" + rate + "\n")

		doc = {
			"title" : title ,
			"rate" : rate ,
			"picture" : picture ,
			"hyperlink" : hyperlink ,
			"showDate" : showDate ,
			"showLength" : showLength ,
			"lastUpdate" : lastUpdate 
		}

		doc_ref = db.collection("丞彥電影").document(movie_id)
		doc_ref.set(doc)
	return "近期上映電影已爬蟲及存檔完畢，網站最近更新日期為：" + lastUpdate


@app.route("/movie",methods=["GET", "POST"])
def movie():
	if request.method == "POST":
		collection_ref = db.collection("丞彥電影")
		docs = collection_ref.order_by("showDate").get()
		MovieTitle = request.form["MovieTitle"]
		info = ""   
	
		for doc in docs:
			r=doc.to_dict()
			if MovieTitle in r["title"]:
				info +=  "片名：<a href=" + r["hyperlink"] + ">" + r["title"] + "</a><br>"
				info += "海報：" + r["picture"] + "<br>"
				info += "片長：" + r["showLength"] + " 分鐘<br>"
				info += "上映日期：" + r["showDate"] + "<br>"
				info += "電影分級：" + r["rate"] + "<br><br>"
		if MovieTitle == "":
			info += "查無此電影 <a href = http://www.atmovies.com.tw/movie/next/>前往官網</a>"
		return info
	else:  
		return render_template("input.html")

@app.route("/webhook", methods=["GET","POST"])
def webhook():
	if request.method == "POST":
		# build a request object
		req = request.get_json(force=True)
		# fetch queryResult from json
		action =  req.get("queryResult").get("action")
		#msg =  req.get("queryResult").get("queryText")
		#info = "動作：" + action + "； 查詢內容：" + msg
		if (action == "rateChoice"):
			rate =  req.get("queryResult").get("parameters").get("rate")
			if (rate == "輔12級"):
				rate = "輔導級(未滿十二歲之兒童不得觀賞)"
			elif (rate == "輔15級"):
				rate = "輔導級(未滿十五歲之人不得觀賞)"
			info = "您選擇的電影分級是：" + rate + "，相關電影：\n"

			collection_ref = db.collection("丞彥電影")
			docs = collection_ref.get()
			result = ""
			for doc in docs:
				dict = doc.to_dict()
				if rate in dict["rate"]:
					result += "片名：" + dict["title"] + "\n"
					result += "介紹：" + dict["hyperlink"] + "\n\n"
			info += result
		elif (action == "MovieDetail"): 
			cond =  req.get("queryResult").get("parameters").get("FilmQ")
			keyword =  req.get("queryResult").get("parameters").get("any")
			info = "您要查詢電影的" + cond + "，關鍵字是：" + keyword + "\n\n"
			if (cond == "片名"):
				collection_ref = db.collection("丞彥電影")
			docs = collection_ref.get()
			found = False
			for doc in docs:
				dict = doc.to_dict()
				if keyword in dict["title"]:
					found = True 
					info += "片名：" + dict["title"] + "\n"
					info += "海報：" + dict["picture"] + "\n"
					info += "影片介紹：" + dict["hyperlink"] + "\n"
					info += "片長：" + dict["showLength"] + " 分鐘\n"
					info += "分級：" + dict["rate"] + "\n" 
					info += "上映日期：" + dict["showDate"] + "\n\n"
			if not found:
				info += "很抱歉，目前無符合這個關鍵字的相關電影喔"

		elif (action == "CityWeather"):
			city =  req.get("queryResult").get("parameters").get("city")
			token = "rdec-key-123-45678-011121314"
			url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=" + token + "&format=JSON&locationName=" + str(city)
			Data = requests.get(url)
			Weather = json.loads(Data.text)["records"]["location"][0]["weatherElement"][0]["time"][0]["parameter"]["parameterName"]
			Rain = json.loads(Data.text)["records"]["location"][0]["weatherElement"][1]["time"][0]["parameter"]["parameterName"]
			MinT = json.loads(Data.text)["records"]["location"][0]["weatherElement"][2]["time"][0]["parameter"]["parameterName"]
			MaxT = json.loads(Data.text)["records"]["location"][0]["weatherElement"][4]["time"][0]["parameter"]["parameterName"]
			info = city + "的天氣是" + Weather + "，降雨機率：" + Rain + "%"
			info += "，溫度：" + MinT + "-" + MaxT + "度"
	else:
		return render_template("webhook.html")
	#return make_response(jsonify({"fulfillmentText": info}))

if __name__ == "__main__":
	app.run()
