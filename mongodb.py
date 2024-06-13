from pymongo import MongoClient
import traceback
from datetime import datetime
import secrets
from prettytable import PrettyTable

def log_exception_to_file(file_name, exception):
    with open(file_name, 'a') as f:
        f.write(str(exception) + '\n')
        traceback.print_exc(file=f)
        f.close()

def view_guitars():
    client = MongoClient(secrets.mongo_host_connection("user", "blank", True))
    db = client["inventory"]
    collection = db["inventory"]

    documents = list(collection.find())

    table = PrettyTable(["S/N", "Code", "Brand", "Allocation", "Level", "BC", "MOE Code", "Remarks", "Rented"])

    for document in documents:
        rows = []
        for key in document:
            if key != "_id":
                if str(document[key]) != "nan":
                    rows.append(document[key])
                elif key == "S/N":
                    rows.append(str(document[key]))
                else:
                    rows.append("-")


        table.add_row(rows)

    print(table)

def login(username, password):
    client = MongoClient(secrets.mongo_host_connection(username, password))

    try:
        client.admin.command('ping')
        client.close()
        return True

    except Exception as e:
        print("We have run into an error while trying to log you on.")
        if input("Do you think this is a mistake? ").upper() == "Y":
            now = datetime.now()
            log_exception_to_file(now.strftime("%d.%m.%Y.errorlog"), e)
            print("A file has been created with the corresponding error.")
            print("Please email Advait or Ryan with the file attached to report this issue.")

        return False

if __name__ == "__main__":
    view_guitars()