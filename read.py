import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

Cond = input("請輸入關鍵字 : ")

collection_ref = db.collection("111")
#.where("Code","==", "3428")
docs = collection_ref.get()
for doc in docs:
	result = doc.to_dict()

	if Cond in result["Course"]:
	
		print("課程名稱：" + result["Course"]+"，教師姓名：" + result["Leacture"]+"，上課時間 : " + result["Time"]+"，在"+result["Room"]+"上課")