'''
import requests
from bs4 import BeautifulSoup
url = "http://www.atmovies.com.tw/movie/next"
Data = requests.get(url)
Data.encoding = "utf-8"
sp = BeautifulSoup(Data.text, "html.parser")
films = sp.select(".filmListAllX li")
for item in films:
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
  print("電影分級:" + rate + "\n")
  print(picture+ "\n")
  print(title+ "\n")
  print(movie_id+ "\n")
  print(hyperlink+ "\n")
  print(showDate+ "\n")
  print(showLength+ "\n")
  '''
import requests
from bs4 import BeautifulSoup

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


from flask import Flask, render_template , request
from datetime import datetime, timezone, timedelta


app = Flask(__name__)

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
        info += "片名：<a href=" + r["hyperlink"] + ">" + r["片名"] + "</a><br>"
        info += "海報：" + r["picture"] + "<br>"
        info += "片長：" + r["showLength"] + " 分鐘<br>"
        info += "上映日期：" + r["showDate"] + "<br>"
        info += "電影分級：" + r["rate"] + "<br><br>"
        return info
  else:  
    return render_template("input.html")
if __name__ == "__main__":
  app.run()