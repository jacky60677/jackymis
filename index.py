import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


from flask import Flask, render_template , request
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
    homepage += "<a href=/movie target = _blank>電影查詢</a><br>"
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
		Result = "Sorry，沒找到"

@app.route("/movie",methods=["GET", "POST"])
def movie():
	'''
	collection_ref = db.collection("丞彥電影")
	docs = collection_ref.get()
	'''
	if request.method == "POST":
        MovieTitle = request.form["MovieTitle"]
        info = ""     
        collection_ref = db.collection("丞彥電影")
        #docs = collection_ref.where("title","==", "夜鷹的單戀").get()
        docs = collection_ref.order_by("showDate").get()
        for MovieTitle in docs:
            if MovieTitle in doc.to_dict()["片名"]: 
                info += "片名：" + doc.to_dict()["片名"] + "<br>" 
                info += "海報：" + doc.to_dict()["picture"] + "<br>"
                info += "影片介紹：" + doc.to_dict()["hyperlink"] + "<br>"
                info += "片長：" + doc.to_dict()["showLength"] + " 分鐘<br>" 
                info += "上映日期：" + doc.to_dict()["showDate"] + "<br><br>"           
        return info
    else:  
        return render_template("input.html")

#if __name__ == "__main__":
#	app.run()
