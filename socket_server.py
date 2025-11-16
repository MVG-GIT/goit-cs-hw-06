import socket
from datetime import datetime
import ast
from pymongo import MongoClient


HOST = "0.0.0.0"
PORT = 5000

client = MongoClient("mongodb://mongo:27017/")
db = client["messages_db"]
collection = db["messages"]


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print(f"Socket server is running on port {PORT}")

    while True:
        data, addr = s.recvfrom(4096)
        decoded = data.decode()

        try:
            # Перетворюємо str(dict) на dict
            msg_dict = ast.literal_eval(decoded)
            msg_dict["date"] = str(datetime.now())

            collection.insert_one(msg_dict)
            print("Saved:", msg_dict)

        except Exception as e:
            print("Error decoding message:", e)
