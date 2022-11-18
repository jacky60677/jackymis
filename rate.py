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