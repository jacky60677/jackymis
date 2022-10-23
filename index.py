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
def text():
	return render_template("jobsearch.html")

#if __name__ == "__main__":
#	app.run()