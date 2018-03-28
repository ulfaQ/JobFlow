import time, os, pickle, sys
from tools import Tools 

print(""" 
       Welcome to:
       __________.                  
       \_  ____/ | ______  _  __.  
        |   _)|  |/  _ \ \/ \/ / 
        |   \ |  (  <_> )     /  
        \_  / |__|\____/ \/\_/   
          \/  I'm Your brain now.
                                  """)

class Files:
    """ Class for initial setting of pickle-formatted txt files (current job list and history) and setting their info-objects"""
    class Info:
        """ Class is made so that we can store additional information in pickle-file, 
        will be instantiated only when pickle-file doesn't exist)"""

        def __init__(self):
           self.current_id = 0

    def check_files():
        # check if current_job_list.txt exist, if not, create it.
        try:
            with open("current_job_list.txt", "rb") as f:
                pass
        except:
            with open("current_job_list.txt", "wb") as f:
                pickle.dump([self.Info()], f, protocol=4, fix_imports=False)
        # check if hist_log.txt exist, if not, create it.
        try:
            with open("hist_log.txt", "rb") as f:
                pass
        except: # Info object is in hist_log only to fill the first object. No other use
            with open("hist_log.txt", "wb") as f:
                pickle.dump([self.Info()], f, protocol=4, fix_imports=False)

Files.check_files()

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

        print("\nENTER NEW JOB\n")
        self.current_job_list.append(Job(Tools().add_or_edit_job(None, self.info.current_id)))
        self.info.current_id += 1
        print("\n   Job added!")

    def delete_job(self):
        """ Poistaa id:n perusteella valitun työn. """
        id_to_remove = input("\nType the ID of the Job you wan't to delete: ")
        try:
            id_to_remove = int(id_to_remove)
            for i in self.current_job_list[1:]:
                if i.current_id == id_to_remove:

                    #Tallennetaan hist_logiin poistettu työ
                    temp_hist_log = None
                    with open("hist_log.txt", "rb") as f:
                        temp_hist_log = pickle.load(f, fix_imports=False, encoding="ASCII", errors="strict")
                    temp_hist_log.append(i)
                    with open("hist_log.txt", "wb") as f:
                        pickle.dump(temp_hist_log, f, protocol=4, fix_imports=False)
                        
                    n = input("Are you sure you wan't to remove {} : {} : {} : {} : {} (y ,n): ".format("ID: ", i.current_id, i.customer, i.product, i.amount)).lower()
                    if n == "y":
                        self.current_job_list.remove(i)
                    print("\nJob succesfully deleted!")
        except:
            print("\n", rm, "not found in list\n")

    def edit_job(self, n):
        # Katsotaan jos käyttäjä käyttää 'e#p' shortcutia, ja passataan parametri (tällä hetkellä vain p toimii) add_or_edit_job functiolle
        parameter = None
        if len(n) == 1:
            input_id = int(input("Type the ID of the job you wan't to edit: "))

        elif len(n) > 1 and str(n[-1]) != "p":
            input_id = int(n[1:])

        if len(n) > 2 and n[-1] == "p":
            input_id = int(n[1:-1])
            parameter = n[-1]
            print("\nShortcut 'e#p' detected.")

        for i in my_job_list.current_job_list[1:]:
            if i.current_id == input_id:
                index_of_the_job = self.current_job_list.index(i)
                # Tässä korvataan vanha objekti uudella vastaavalla (johon on vaihdettu haluttu parametri)
                self.current_job_list[index_of_the_job] = Job(Tools().add_or_edit_job(i, None, parameter))
                return
        print("JOB ID {} WAS NOT FOUND".format(input_id))


    def show_list(self, job_list):
        print("""
       ID:     ADDED:          PR:    CUSTOMER:           PRODUCT:            AMOUNT:        SHEET:    MATERIAL:         COMMENT:       STATUS:""")
        for i in job_list:
            print("     -----------------------------------------------------------------------------------------------------------------------------------------------------")
            print("     | ", str(i.current_id).ljust(3), " | ", i.addedDate, " | ", str(i.priority).ljust(2), " | ", \
                    i.customer.ljust(15)[:15], " | ", i.product.ljust(15)[:15], " | ", i.amount.ljust(10)[:10], " | ", \
                    i.printing_sheet_size.ljust(5)[:5], " | ", i.material.ljust(13)[:13], " | ", i.comment.ljust(10)[:10], " | ", i.status, " | ")
        print("     -----------------------------------------------------------------------------------------------------------------------------------------------------\n")

    def show_job(self, id_to_show):
        """.ljust(14)[:14]"""
        for i in self.current_job_list[1:]:
            if i.current_id == id_to_show:
                print("""                 
                                                       {}            
                                                      ---------------------------{}  
        _/_/_/  _/      _/  _/_/_/_/   _/_/            ID {} : {} : {} : {}      
         _/    _/_/    _/  _/       _/    _/   _/     ---------------------------{}    
        _/    _/  _/  _/  _/_/_/   _/    _/            Product    : {}                                          
       _/    _/    _/_/  _/       _/    _/   _/        Amount     : {}                                          
    _/_/_/  _/      _/  _/         _/_/                Material   : {}                                          
                                                       Sheet size : {}                                          
                                                       Comment    : {}                                          
                                                      ---------------------------{}    """.format( \
                                                      i.customer, "-".ljust(len(i.status), "-"), \
                                                      i.current_id, i.priority, i.addedDate, i.status, \
                                                      "-".ljust(len(i.status), "-"), \
                                                      i.product, \
                                                      i.amount, \
                                                      i.material,\
                                                      i.printing_sheet_size, \
                                                      i.comment, \
                                                      "-".ljust(len(i.status), "-") ))

    def _clear_job_list(self):
        n = input("Are you sure you wan't to remove all jobs from current_job_list permanently. \
Jobs removed by 'clear' are not saved to history. (y, n): ")
        if n == "y":
            self.current_job_list[1:] = []

class Job:

    def __init__(self, prompted_info):

        self.prompted_info = prompted_info

        self.customer = prompted_info.get("customer")
        self.product = prompted_info.get("product")
        self.amount = prompted_info.get("amount")
        self.material = prompted_info.get("material")
        self.printing_sheet_size = prompted_info.get("printing_sheet_size")
        self.status = prompted_info.get("status")
        self.comment = prompted_info.get("comment")
        self.addedDate = prompted_info.get("addedDate")
        self.current_id = prompted_info.get("current_id")
        self.priority = prompted_info.get("priority") 
        
# Pistetään ohjelma käyntiin
my_job_list = JobList()
# Haetaan työt tiedostosta
my_job_list.get_job_list_from_file()

# Interface:
while True:
    n = input("\nEnter command:\n>>> ")
    if len(n) == 0:
        pass

    elif n.lower() == "a":
        my_job_list.add_job()

    elif n.lower() == "d":
        my_job_list.delete_job()

    elif n[0].lower() == "e":
        my_job_list.edit_job(n)

    elif n.lower() == "q":
        print("\nThank you for using Flow. See you soon!")
        sys.exit()

    elif n.lower() == "clear":
        my_job_list._clear_job_list()

    elif n.lower() == "l":
        print("""
       ___                _     _         _    _    _   _             _ 
      / __|___ _ __  _ __| |___| |_ ___  | |  (_)__| |_(_)_ _  __ _  (_)
     | (__/ _ \ '  \| '_ \ / -_)  _/ -_) | |__| (_-<  _| | ' \/ _` |  _ 
      \___\___/_|_|_| .__/_\___|\__\___| |____|_/__/\__|_|_||_\__, | (_)
                    |_|                                       |___/     """)      
        my_job_list.show_list(my_job_list.current_job_list[1:])
 
    elif n.lower() == "o":
        print("""
                                  _ _     _      
       __ _  ___ ___ ___  ___ ___(_) |__ | | ___  _ 
      / _` |/ __/ __/ _ \/ __/ __| | '_ \| |/ _ \(_)
     | (_| | (_| (_|  __/\__ \__ \ | |_) | |  __/ _ 
      \__,_|\___\___\___||___/___/_|_.__/|_|\___|(_) """)
        my_job_list.show_list(Tools().gimme_my_todo_list(my_job_list.current_job_list[1:]))

    elif n.lower() == "w":
        print("""
                     .__  __  .__                
     __  _  _______  |__|/  |_|__| ____    ____  
     \ \/ \/ /\__  \ |  \   __\  |/    \  / ___\ 
      \     /  / __ \|  ||  | |  |   |  \/ /_/  > _  _  _ 
       \/\_/  (____  /__||__| |__|___|  /\___  / (_)(_)(_)
                   \/                 \//_____/           """)
        my_job_list.show_list([x for x in my_job_list.current_job_list[1:] if "Waiting" in x.status])

    elif n.lower() == "h":
        with open("hist_log.txt", "rb") as f:
            hist = pickle.load(f, fix_imports=False, encoding="ASCII", errors="strict")
            print("""
             __  ___  __   __      
     |__| | /__`  |  /  \ |__) \ / o
     |  | | .__/  |  \__/ |  \  |  o                   
                                    """)
            my_job_list.show_list(hist[1:])

    elif n.lower() == "m":
        print("""
                                    /---------------------------------------------------------------------------\\
       _____ _____ _____ _____ _    | (O) Show Flow     | (A) Add new Job   | (#) Show Job-info | (e#p)         |
      |     |   __|   | |  |  |_|   |-------------------|-------------------|-------------------|---------------|
      | | | |   __| | | |  |  |_    | (L) Show All      | (E) Edit Job      | (clear) Clear All |               |
      |_|_|_|_____|_|___|_____|_|   |-------------------|-------------------|-------------------|---------------|
                                    | (W) Show Waiting  | (D) Delete Job    | (H) Show History  | (Q) Quit      |
                                    \\---------------------------------------------------------------------------/
                                                                                                         """)
    else:
        try:
            int_n = int(n)
            my_job_list.show_job(int_n)
        except:
            print(n, "is not a valid input. See (M)enu for commands.")

    my_job_list.write_pickle_file()
