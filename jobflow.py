import time, datetime, os, pickle, sys
from tools import get_valid_input, gimme_my_todo_list, gimme_waiting_jobs, edit_job

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
    """ Class is made so that we can store additional information in pickle-file, 
    will be instantiated only when pickle-file is empty (to be specific: Doesn't exist)"""
    def __init__(self):
       self.current_id = 0
try:
    with open("current_job_list.txt", "rb") as f:
        pass
except:
    with open("current_job_list.txt", "wb") as f:
        pickle.dump([Info()], f, protocol=4, fix_imports=False)

# check if hist_log exist, if not, create it.
try:
    with open("hist_log.txt", "rb") as f:
        pass
except:
    with open("hist_log.txt", "wb") as f:
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

    # Funktio tiedoston päivitykseen.
    def write_pickle_file(self):
        with open("current_job_list.txt", "wb") as f:
            pickle.dump(self.current_job_list, f, protocol=4, fix_imports=False)

    # Funktio töiden lisäämiseen.
    def add_job(self):
        """ Ensin otetaan käyttäjältä inputit ja sen jälkeen luodaan Job-objekti annetuilla specseillä ja lisätän se listaan. """

        prompted_info = {
            "customer"             : input("Customer: "),         
            "product"              : input("Product: "),
            "amount"               : input("Amount: "),           
            "material"             : input("Material: "),         
            "comment"              : input("Comment: "),          
            "printing_sheet_size"  : input("Printing_sheet_size: "),
            "current_id"           : self.info.current_id,
            "addedDate"            : datetime.datetime.now().strftime("%d-%m %H:%M"),
            "status"               : get_valid_input("Status 1=ReadyToPrint, 2=Waiting: ", ("1","2")).strip()
            }

        self.current_job_list.append(Job(**prompted_info))
        self.info.current_id += 1

    def remove_job(self, id_to_remove):
        """ Poistaa id:n perusteella valitun työn. """
        for i in self.current_job_list[1:]:
            if i.id == id_to_remove:

                #Tallennetaan hist_logiin poistettu työ
                temp_hist_log = None
                with open("hist_log.txt", "rb") as f:
                    temp_hist_log = pickle.load(f, fix_imports=False, encoding="ASCII", errors="strict")
                temp_hist_log.append(i)
                with open("hist_log.txt", "wb") as f:
                    pickle.dump(temp_hist_log, f, protocol=4, fix_imports=False)
                    
                n = input("Are you sure you wan't to remove {} : {} : {} : {} : {} (y ,n): ".format("ID: ", i.id, i.customer, i.product, i.amount)).lower()
                if n == "y":
                    self.current_job_list.remove(i)

    def show_jobs(self, job_list):
        print("""
       ID:     ADDED:             PR:    CUSTOMER:           PRODUCT:            AMOUNT:        SHEET:    MATERIAL:         COMMENT:       STATUS:""")
        for i in job_list:
            print("     -----------------------------------------------------------------------------------------------------------------------------------------------------")
            print("     | ", str(i.id).ljust(3), " | ", i.addedDate, " | ", str(i.priority).ljust(2), " | ", \
                    i.customer.ljust(15)[:15], " | ", i.product.ljust(15)[:15], " | ", i.amount.ljust(10)[:10], " | ", \
                    i.printing_sheet_size.ljust(5)[:5], " | ", i.material.ljust(13)[:13], " | ", i.comment.ljust(10)[:10], " | ", i.status.ljust(14)[:14], " | ")
        print("     -----------------------------------------------------------------------------------------------------------------------------------------------------\n")

    def show_job(self, id_to_show):
        for i in self.current_job_list[1:]:
            if i.id == id_to_show:
                print("""                                                      -------------------------------------------------------{}                                            
                                                      | ID: {} Priority: {} :  Added: {} : Status: {} |                   
        _/_/_/  _/      _/  _/_/_/_/    _/_/          |------------------------------------------------------{} |
         _/    _/_/    _/  _/        _/    _/         |   Customer : {}                                      {} |
        _/    _/  _/  _/  _/_/_/    _/    _/          |------------------------------------------------------{} |
       _/    _/    _/_/  _/        _/    _/           |    Product : {}                                      {} |
    _/_/_/  _/      _/  _/          _/_/              |   Material : {}                                      {} |
                                                      |     Amount : {}                                      {} |
                                                      | Sheet size : {}                                      {} |
                                                      |    Comment : {}                                      {} |
                                                      -------------------------------------------------------{} 
               """.format("-".ljust(len(i.status), "-"), \
                       str(i.id).ljust(4), i.priority, i.addedDate, i.status, \
                        "-".ljust(len(i.status), "-"), \
                        "-".ljust(len(i.status), "-"), \

                        i.customer, "-".ljust(len(i.status), "-"), \
                        i.product, "-".ljust(len(i.status), "-"), \
                        i.material, "-".ljust(len(i.status), "-"),\
                        i.amount, "-".ljust(len(i.status), "-"),\
                        i.printing_sheet_size, "-".ljust(len(i.status), "-"),\
                        i.comment, "-".ljust(len(i.status), "-"), \
                        "-".ljust(len(i.status), "-")))

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
        self.priority = 0

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
    n = input("Enter command:")

    if n.lower() == "m":
        print("""
                                    -------------------------------------------------------------------------
       _____ _____ _____ _____ _    | (O) Show Flow     | (A) Add new Job   | (#) Show Job-info | (Q) Quit  |
      |     |   __|   | |  |  |_|   |-------------------|-------------------|-------------------|-----------|
      | | | |   __| | | |  |  |_    | (L) Show All      | (E) Edit Job      | (clear) Clear All |           |
      |_|_|_|_____|_|___|_____|_|   |-------------------|-------------------|-------------------|-----------|
                                    | (W) Show Waiting  | (D) Delete Job    | (H) Show History  |           |
                                    -------------------------------------------------------------------------
                                                                                                         """)
    elif n.lower() == "a":
        print("\nENTER NEW JOB:\n")
        my_job_list.add_job()
        my_job_list.write_pickle_file()

    elif n.lower() == "l":
        print("""
       ___                _     _         _    _    _   _             _ 
      / __|___ _ __  _ __| |___| |_ ___  | |  (_)__| |_(_)_ _  __ _  (_)
     | (__/ _ \ '  \| '_ \ / -_)  _/ -_) | |__| (_-<  _| | ' \/ _` |  _ 
      \___\___/_|_|_| .__/_\___|\__\___| |____|_/__/\__|_|_||_\__, | (_)
                    |_|                                       |___/     """)      
        my_job_list.show_jobs(my_job_list.current_job_list[1:])

    elif n.lower() == "d":
        rm = int(input("Type the ID of the job you wan't to remove: "))
        my_job_list.remove_job(rm)
        my_job_list.write_pickle_file()

    elif n.lower() == "e":
        ed = int(input("Type the ID of the job you wan't to edit: "))
        edit_job(my_job_list.current_job_list[1:], ed)
        my_job_list.write_pickle_file()

    elif n.lower() == "h":
        with open("hist_log.txt", "rb") as f:
            hist = pickle.load(f, fix_imports=False, encoding="ASCII", errors="strict")
            print("""
             __  ___  __   __      
     |__| | /__`  |  /  \ |__) \ / o
     |  | | .__/  |  \__/ |  \  |  o                   
                                    """)
            my_job_list.show_jobs(hist[1:])

    elif n.lower() == "q":
        print("\nThank you for using Flow. See you soon!")
        sys.exit()

    elif n.lower() == "clear":
        my_job_list._clear_job_list()
        my_job_list.write_pickle_file()

    elif n.lower() == "o":
        print("""
                                  _ _     _      
       __ _  ___ ___ ___  ___ ___(_) |__ | | ___  _ 
      / _` |/ __/ __/ _ \/ __/ __| | '_ \| |/ _ \(_)
     | (_| | (_| (_|  __/\__ \__ \ | |_) | |  __/ _ 
      \__,_|\___\___\___||___/___/_|_.__/|_|\___|(_) """)
        my_job_list.show_jobs(gimme_my_todo_list(my_job_list.current_job_list[1:]))

    elif n.lower() == "w":
        print("""
                     .__  __  .__                
     __  _  _______  |__|/  |_|__| ____    ____  
     \ \/ \/ /\__  \ |  \   __\  |/    \  / ___\ 
      \     /  / __ \|  ||  | |  |   |  \/ /_/  > _  _  _ 
       \/\_/  (____  /__||__| |__|___|  /\___  / (_)(_)(_)
                   \/                 \//_____/           """)
        my_job_list.show_jobs(gimme_waiting_jobs(my_job_list.current_job_list[1:]))


    else:
        int_n = int(n)
        my_job_list.show_job(int_n)

        
#       try:
#           int_n = int(n)
#           my_job_list.show_job(int_n)
#       except:
#           print(n, "is not a valid input. See (M)enu for commands.")
