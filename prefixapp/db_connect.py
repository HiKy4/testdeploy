# myapp/db_connect.py
import pymongo
from pymongo import MongoClient


    # Thay thế các giá trị này bằng thông tin kết nối của bạn
url = "mongodb://localhost:27017"
    
client = pymongo.MongoClient(url)
db = client['databaseTestdj']
collection = db['collectionTestdj']
collectionCart = db['collection_cart']