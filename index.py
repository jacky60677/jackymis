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

@app.route("/movie_news")
def movie_news():
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

        images = t.select("img")
  		if len(images) == 1:
    		rate = "目前尚無分級資訊"
  		else:
    		rate = images[1].get("src")
    		if rate== "/images/cer_G.gif":
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
            "title": title,
            "rate": rate,
            "picture": picture,
            "hyperlink": hyperlink,
            "showDate": showDate,
            "showLength": showLength,
            "lastUpdate": lastUpdate
         }

        doc_ref = db.collection("丞彥電影").document(movie_id)
        doc_ref.set(doc)
    return "近期上映電影已爬蟲及存檔完畢，網站最近更新日期為：" + lastUpdate 


@app.route("/movie",methods=["GET", "POST"])
def movie():
	collection_ref = db.collection("丞彥電影")
	docs = collection_ref.get()
	if request.method == "POST":
		MovieTitle = request.form["MovieTitle"]
		info = ""     
        rate = ""
		for doc in docs:
			r=doc.to_dict()
			if MovieTitle in r["片名"]: 
				info +=  "片名：<a href=" + r["hyperlink"] + ">" + r["片名"] + "</a><br>" 
				info += "海報：" + r["picture"] + "<br>"
				info += "片長：" + r["showLength"] + " 分鐘<br>" 
				info += "上映日期：" + r["showDate"] + "<br><br>"

				info += "電影分級：" + rate + "<br><br>"           
		return info
	else:  
		return render_template("input.html")

#if __name__ == "__main__":
#	app.run()
