from pymongo import MongoClient
import traceback
from datetime import datetime

import pdfs
import secrets
from prettytable import PrettyTable
import colorama

def log_exception_to_file(file_name, exception):
    with open(file_name, 'a') as f:
        f.write(str(exception) + '\n')
        traceback.print_exc(file=f)
        f.close()

def reserve_guitar(sn, name):
     colorama.init()
     client = MongoClient(secrets.mongo_host_connection("user", "blank", True))
     db = client["inventory"]
     collection = db["inventory"]

     query = {"S/N": int(sn)}

     document = list(collection.find(query))

     print(document[0])

     if document[0]["RENTED"] == "F":
         print(colorama.Fore.GREEN + "Guitar is confirmed available for rent!" + colorama.Style.RESET_ALL)
         print("\033[3mWould you like to rent it?\033[0m")
         while True:
             ask = input("[Y/n] ")
             if ask.lower() == "y":
                 update_operation = {"$set": {"RENTED": "T"}}

                 result = collection.update_one(query, update_operation)

                 if result.matched_count > 0:
                     print("Successfully blocked guitar!")
                     # Loan forms items after this
                     clas = input("What is your form class? ")

                     while True:
                         email = input("What is your email? ")
                         if pdfs.verify_email(email):
                             break
                         else:
                             print("Invalid email. Please enter again.")

                     pdfs.create_loan_pdf(name=name, email=email, clas=clas, guitar_model=document[0]["Brand"], serial_num=document[0]["Code"])
                 else:
                     print("Failed to block guitar.")
                     break

             elif ask.lower() == "n":
                 print("Returning back to main menu")
             else:
                 print(colorama.Fore.LIGHTRED_EX + "\033[3mInvalid input. Please try again.\033[0m" + colorama.Style.RESET_ALL)
     else:
         print("Sorry, guitar not available. Please try again.")


def view_guitars(name):
    colorama.init()
    client = MongoClient(secrets.mongo_host_connection("user", "blank", True))
    db = client["inventory"]
    collection = db["inventory"]

    documents = list(collection.find())

    table = PrettyTable(["S/N", "Code", "Brand", "Allocation", "Level", "BC", "MOE Code", "Remarks", "Rented"])

    largest_sn = 0

    for document in documents:
        rows = []
        for key in document:
            if key != "_id":
                if str(document[key]) != "nan":
                    rows.append(document[key])
                elif key == "S/N":
                    rows.append(str(document[key]))
                    if largest_sn < int(document["S/N"]):
                        largest_sn = int(document["S/N"])
                else:
                    rows.append("-")


        table.add_row(rows)

    print(table)

    print(colorama.Back.LIGHTBLACK_EX + "\x1B[3mAll data available on the guitars has been shown.\x1B[0m")
    print("To enter which guitar to loan," + colorama.Fore.LIGHTGREEN_EX + " enter the S/N " + colorama.Fore.RESET + "of it. Else," + colorama.Fore.LIGHTRED_EX + " enter q to exit.")



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
    reserve_guitar(1, "advait")