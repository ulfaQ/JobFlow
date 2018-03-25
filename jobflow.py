import time, datetime, os, pickle
from tools import get_valid_input, gimme_my_todo_list, EditJob

print(""" 
         Welcome to:
         __________.                  
         \_  ____/ | ______  _  __.  
          |   _)|  |/  _ \ \/ \/ / 
          |   \ |  (  <_> )     /  
          \_  / |__|\____/ \/\_/   
            \/  I'm Your brain now.

   """)

# Check to see if the current_job_list.txt exists. If not, create the file and add the info-object
class Info:
    """ This class is so that we can store additional information in pickle-file, 
    will be instantiated only when pickle-file is empty (to be specific: Doesn't exist)"""
    def __init__(self):
       self.current_id = 0
try:
    with open("current_job_list.txt", "rb") as f:
        pass
except:
    with open("current_job_list.txt", "wb") as f:
        pickle.dump([Info()], f, protocol=4, fix_imports=False)

class JobList:
    """ Class for managing jobs, Instance of this class is created in the last lines """

    # Tehdään lista jossa säilytetään Jobit ajon aikana.
    def __init__(self):
        self.current_job_list = []
        self.info = None # Tähän haetaan info-objekti tiedostosta. Sisältää muuta infoa joka halutaan säilyttää

    # Funktio jolla haetaan työt tiedostosta.
    def get_job_list_from_file(self):
        if os.path.getsize("current_job_list.txt") > 0:
            with open("current_job_list.txt", "rb") as f:
                self.current_job_list = pickle.load(f, fix_imports=False, encoding="ASCII", errors="strict")
                #Lisää tähän objektiin muualla tarvittavaa infoa
                self.info = self.current_job_list[0]

    # Funktio tiedoston päivitykseen
    def write_pickle_file(self):
        with open("current_job_list.txt", "wb") as f:
            pickle.dump(self.current_job_list, f, protocol=4, fix_imports=False)
    # Funktio töiden lisäämiseen.
    def add_job(self):
        """ Ensin otetaan käyttäjältä inputit ja sen jälkeen luodaan Job-objekti annetuilla specseillä """

        # Tervitaanko näitä kaikkia?
        # Tarvitaanko jotain lisää?
        prompted_info = {
            "customer"             : input("Customer: "),         
            "product"              : input("Product: "),
            "amount"               : input("Amount: "),           
            "material"             : input("Material: "),         
            "comment"              : input("Comment: "),          
            "printing_sheet_size"  : input("Printing_sheet_size: "),
            "current_id"           : self.info.current_id,
            "addedDate"            : datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "status"               : get_valid_input("Status: (1=ReadyToPrint, 2=Waiting)", ("1","2"))
            }

        self.current_job_list.append(Job(**prompted_info))
        self.info.current_id += 1

    def remove_job(self, id_to_remove):
        """ Poistaa id:n perusteella valitun työn. """
        for i in self.current_job_list[1:]:
            if i.id == id_to_remove:
                n = input("Are you sure you wan't to remove {} : {} : {} : {} : {} \
                        - (y ,n): ".format(i.id, i.addedDate, i.customer, i.product, i.amount)).lower()
                if n == "y":
                    self.current_job_list.remove(i)

    def show_jobs(self, job_list):
        print("""
           ID:     ADDED:                  URG:   CUSTOMER:           PRODUCT:            AMOUNT:        SHEET:    COMMENT:""")
        for i in job_list[1:]:
            print("         -------------------------------------------------------------------------------------------------------------------------")
            print("         | ", str(i.id).ljust(3), " | ", i.addedDate, " | ", str(i.urgency).ljust(2), " | ", \
                    i.customer.ljust(15)[:15], " | ", i.product.ljust(15)[:15], " | ", i.amount.ljust(10)[:10], " | ", i.printing_sheet_size.ljust(5)[:5], " | ", i.comment.ljust(10)[:10], " | ")
        print("         -------------------------------------------------------------------------------------------------------------------------\n")

    def show_job(self, id_to_show):
        for i in self.current_job_list[1:]:
            if i.id == id_to_show:
                print("""
            ---------------------------------
            Information of the job requested:
            ---------------------------------

                        Id: {}
                     Added: {}
                  Customer: {}
                   Product: {}
                    Amount: {}
                  Material: {}
            PrintSheetSize: {}
                   Comment: {}
                    Status: {}
                   Urgency: {}
                """.format(i.id, i.addedDate, i.customer, i.product, i.amount,\
                        i.material, i.printing_sheet_size, i.comment, i.status, i.urgency))
                break

    def _clear_job_list(self):
        self.current_job_list[1:] = []

class Job:

    def __init__(self, **prompted_info):
        """ Promptataan käyttäjältä työtä koskevat tiedot """
        self.customer = prompted_info.get("customer")
        self.product = prompted_info.get("product")
        self.amount = prompted_info.get("amount")
        self.material = prompted_info.get("material")
        self.printing_sheet_size = prompted_info.get("printing_sheet_size")
        self.status = prompted_info.get("status")
        self.comment = prompted_info.get("comment")
        self.addedDate = prompted_info.get("addedDate")
        self.id = prompted_info.get("current_id")
        self.urgency = 0

        # Muokataan statusta siten että jos input on 2, kysytään syytä mitä odottaa,
        # Jos input on 1, laitetaan statukseksi ready to print
        if self.status == "2":
            waiting_for_what = input("Waiting for what?: ")
            self.status = "Waiting for: " + waiting_for_what 
        elif self.status == "1":
            self.status = "Ready to Print"

# Pistetään ohjelma käyntiin
my_job_list = JobList()
# Haetaan työt tiedostosta
my_job_list.get_job_list_from_file()

# Interface:
while True:
    n = input("What you wanna do? (M)enu: ")

    if n.lower() == "m":
        print("""
                                       --------------------------------------------
          _____ _____ _____ _____ _    | (A) Add new Job    |  (D) Delete Job     | 
         |     |   __|   | |  |  |_|   |--------------------|---------------------| 
         | | | |   __| | | |  |  |_    | (L) List all Jobs  |  (E) Edit Job       | 
         |_|_|_|_____|_|___|_____|_|   |--------------------|---------------------| 
                                       | (O) Ordered List   |  (ID) Show Job-info | 
                                       -------------------------------------------- 
                        """)

    elif n.lower() == "a":
        print("ADD JOB:\n")
        my_job_list.add_job()
        my_job_list.write_pickle_file()

    elif n.lower() == "l":
        print("""
                                   ___                _     _         _    _    _   _             _ 
                                  / __|___ _ __  _ __| |___| |_ ___  | |  (_)__| |_(_)_ _  __ _  (_)
                                 | (__/ _ \ '  \| '_ \ / -_)  _/ -_) | |__| (_-<  _| | ' \/ _` |  _ 
                                  \___\___/_|_|_| .__/_\___|\__\___| |____|_/__/\__|_|_||_\__, | (_)
                                                |_|                                       |___/""")      
        my_job_list.show_jobs(my_job_list.current_job_list)

    elif n.lower() == "d":
        rm = int(input("Type the ID of the job you wan't to remove: "))
        my_job_list.remove_job(rm)
        my_job_list.write_pickle_file()

    elif n.lower() == "e":
        ed = int(input("Type the ID of the job you wan't to edit: "))
        EditJob(my_job_list.current_job_list[1:], ed)
        my_job_list.write_pickle_file()

    elif n.lower() == "clear":
        my_job_list._clear_job_list()
        my_job_list.write_pickle_file()

    elif n.lower() == "o":
        print("""
                          _____ _                   __           _   _          _        _   _             _ 
                         |_   _| |_  ___ _ _ ___   / _|___ _ _  | |_| |_  ___  | |_ __ _| |_(_)_ _  __ _  (_)
                           | | | ' \/ -_) '_/ -_) |  _/ _ \ '_| |  _| ' \/ -_) |  _/ _` | / / | ' \/ _` |  _ 
                           |_| |_||_\___|_| \___| |_| \___/_|    \__|_||_\___|  \__\__,_|_\_\_|_||_\__, | (_)
                                                                                                   |___/""")

        my_job_list.show_jobs(gimme_my_todo_list(my_job_list.current_job_list))

    else:
        try:
            int_n = int(n)
            my_job_list.show_job(int_n)
        except:
            print(n, "is not a valid input. Try something else.")
