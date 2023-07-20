import os
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()
USERNAME = os.environ.get('MONGODB_USERNAME')
PASSWORD = os.environ.get('MONGODB_PASSWORD')
CLUSTER  = os.environ.get('MONGODB_CLUSTER')

class ConnectDB:
   def __init__(self, db , col):
      """_summary_
      Args:
         db (_type_string): db_name
         col (_type_string): collection_name
      """
      load_dotenv()
      USERNAME = os.environ.get('MONGODB_USERNAME')
      PASSWORD = os.environ.get('MONGODB_PASSWORD')
      CLUSTER  = os.environ.get('MONGODB_CLUSTER')
      self.conection = 'mongodb+srv://{0}:{1}@{2}.bulpsfe.mongodb.net/myFirstDatabase'.format(USERNAME, PASSWORD, CLUSTER)
      # Atlas へ接続
      self.client = MongoClient(self.conection)
      #DB接続(初回は作成)
      self.db = self.client[db]
      #collection接続(初回は作成)
      self.col = self.db[col]

   def create(self, detas):
      """
      dbへのデータの書き込み
      """
      result = self.col.insert_many(detas)
   
   def read(self):
      """
      dbからデータの読み込み
      """
      data = [d for d in self.col.find()]
      for d in data:
         print (d)

   def close(self):
      """
      #DB切断(終了前に必ず実行する。)
      """
      self.client.close()