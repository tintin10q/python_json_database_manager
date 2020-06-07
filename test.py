from database_manager import Database

db = Database

with db('test') as users:
    users["quinten"] = {"status": "cool"}
    users["foo"] = "bar"
