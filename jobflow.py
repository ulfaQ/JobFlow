import time, datetime, os, pickle, sys
# Own modules:
from tools import Tools
from files import Files
from pdf_generator import MakePDF

Files.check_files()

print(""" 
       Welcome to:
       __________.                  
       \_  ____/ | ______  _  __.  
        |   _)|  |/  _ \ \/ \/ / 
        |   \ |  (  <_> )     /  
        \_  / |__|\____/ \/\_/   
          \/  I'm Your brain now.
                                  """)

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

        print("\n    ENTERING NEW JOB\n")
        self.current_job_list.append(Job(Tools().add_or_edit_job(None, self.info.current_id)))
        print("\n   Job {} added!".format(self.info.current_id))
        self.info.current_id += 1

    def delete_job(self):
        """ Poistaa id:n perusteella valitun työn. """
        id_to_remove = input("\nType the ID of the Job you wan't to delete: ")

        if id_to_remove.isdigit():
            id_to_remove = int(id_to_remove)
        else:
            print("    {} is not valid input. ID can only contain integers.".format(id_to_remove))
            return

        n = None
        for i in self.current_job_list[1:]:
            if i.job_id == id_to_remove:

                n = Tools().get_valid_input("Are you sure you wan't to remove {} : {} : {} : {} : {} ?".format("ID: ", i.job_id, i.customer, i.product, i.amount), ("y", "n")).lower()

                if n == "y":
                    self.current_job_list.remove(i)
                    i.status = ("DELETED {}".format(datetime.datetime.now().strftime("%d-%m-%Y %H:%M")))
                    #Tallennetaan hist_logiin poistettu työ
                    temp_hist_log = None
                    with open("hist_log.txt", "rb") as f:
                        temp_hist_log = pickle.load(f, fix_imports=False, encoding="ASCII", errors="strict")
                    temp_hist_log.append(i)
                    with open("hist_log.txt", "wb") as f:
                        pickle.dump(temp_hist_log, f, protocol=4, fix_imports=False)
                    print("\n    Job succesfully deleted!")
                    return

                elif n == "n":
                    print("\n    Deletion cancelled!")
                    return
    
        print("\n    ID: {} NOT FOUND".format(id_to_remove))

    def edit_job(self, n):
        # Katsotaan jos käyttäjä käyttää 'e#p' shortcutia, ja passataan parametri (tällä hetkellä vain p toimii) add_or_edit_job functiolle
        input_id = None
        suggestion = None
        if n == "e":
            suggestion = input("\nType the ID of the job you wan't to edit: ")
            if suggestion.isdigit():
                input_id = int(suggestion)
              #except:
               #    if input_id == "q":
               #        break
               #    print(input_id, " is not a valid input. ID can only contain integers! (q to cancel): ")

        if len(n) > 1 and n[1:].isdigit():
            input_id = int(n[1:])

        parameter = None
        if len(n) > 2 and n[-1] == "p" and n[1:-1].isdigit():
            input_id = int(n[1:-1])
            parameter = n[-1]
            print("\n    Shortcut 'e#p' detected.")

        for i in RUNNING_LIST.current_job_list[1:]:
            if i.job_id == input_id:
                index_of_the_job = self.current_job_list.index(i)
                # Tässä korvataan vanha objekti uudella vastaavalla (johon on vaihdettu haluttu parametri)
                self.current_job_list[index_of_the_job] = Job(Tools().add_or_edit_job(i, None, parameter))
                return

        print("\n    ID {} NOT FOUND".format(input_id))
        
    def show_list(self, job_list):
        print("""
       ID:     ADDED:          PR:    CUSTOMER:           PRODUCT:            AMOUNT:        SHEET:    MATERIAL:         COMMENT:       STATUS:""")
        for i in job_list:
            print("     ------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("     | ", str(i.job_id).ljust(3), " | ", i.addedDate, " | ", str(i.priority).ljust(2), " | ", \
                    i.customer.ljust(15)[:15], " | ", i.product.ljust(15)[:15], " | ", i.amount.ljust(10)[:10], " | ", \
                    i.printing_sheet_size.ljust(5)[:5], " | ", i.material.ljust(13)[:13], " | ", i.comment.ljust(10)[:10], " | ", str(i.status).ljust(16)[:16], "| ")
        print("     ------------------------------------------------------------------------------------------------------------------------------------------------------\n")

    def show_job_info(self, id_to_show):
        """.ljust(14)[:14]"""
        for i in self.current_job_list[1:]:
            if i.job_id == id_to_show:
                rivitetty_comment = Tools.rivitetty(i.comment, len(i.status) + 13)
                print("""                 
                                                       {}            
                                                      ---------------------------{}  
        _/_/_/  _/      _/  _/_/_/_/   _/_/            ID {} : {} : {} : {}      
         _/    _/_/    _/  _/       _/    _/   _/     ---------------------------{}    
        _/    _/  _/  _/  _/_/_/   _/    _/            Product    : {}                                          
       _/    _/    _/_/  _/       _/    _/   _/        Amount     : {}                                          
    _/_/_/  _/      _/  _/         _/_/                Material   : {}                                          
                                                       Sheet size : {}""".format( \
                                                      i.customer, "-".ljust(len(i.status), "-"), \
                                                      i.job_id, i.priority, i.addedDate, i.status, \
                                                      "-".ljust(len(i.status), "-"), \
                                                      i.product, \
                                                      i.amount, \
                                                      i.material,\
                                                      i.printing_sheet_size, \
                                                       ))
                                        
                print("""                                                       Comment    : {}""".format(rivitetty_comment[0]))
                for row in rivitetty_comment[1:]:
                    print("                                                                    {}".format(row))

                print(  "                                                      ---------------------------{}".format("-".ljust(len(i.status), "-")))

    def _clear_job_list(self):
        n = Tools().get_valid_input("Are you sure you wan't to remove all jobs from current_job_list permanently. \
Jobs removed by 'clear' are not saved to history. ", ("y", "n"))
        if n == "y":
            self.current_job_list[1:] = []
        if n == "n":
            print("\n   CLEAR CANCELLED")

    def restore_from_history(self):
        n = input("\nType the ID of the job you wan't to restore: ")
        job_found = False
        temp_hist_log = None
        with open("hist_log.txt", "rb") as f:
            temp_hist_log = pickle.load(f, fix_imports=False, encoding="ASCII", errors="strict")
        for job in temp_hist_log[1:]:
            if job.job_id == int(n):
                job_found = True
                job.status = Tools().get_status(Tools().get_valid_input("Input a new STATUS for restored job:", ("1","2")))
                temp_hist_log.remove(job)
                self.current_job_list.append(job)
                with open("hist_log.txt", "wb") as f:
                    pickle.dump(temp_hist_log, f, protocol=4, fix_imports=False)
                print("\n    Job {} succesfully restored from history!".format(n))
                return

        if not job_found:
            print("\n    Job id {} not found.".format(n))
                        
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
        self.job_id = prompted_info.get("job_id")
        self.priority = prompted_info.get("priority") 
        
# Interface:
class Interface:
    def interface():
        n = input("\nEnter command\n>>> ")
        n = n.lower()
        if len(n) == 0:
            pass

        # Making report-pdf's
        elif n == "ro":
            MakePDF().make_report(Tools().gimme_my_todo_list(RUNNING_LIST.current_job_list[1:]), "Acceccible Jobs")
            print("\n    Created a PDF report of all accessible jobs.")
        elif n == "rl":
            MakePDF().make_report(RUNNING_LIST.current_job_list[1:], "All Jobs")
            print("\n    Created a PDF report of all jobs.")
        elif n == "rw":
            MakePDF().make_report([x for x in RUNNING_LIST.current_job_list[1:] if "Waiting" in x.status], "Waiting Jobs")
            print("\n    Created a PDF report of all waiting jobs.")
        # End report-pdf's

        elif n == "a":
            RUNNING_LIST.add_job()

        elif n == "d":
            RUNNING_LIST.delete_job()

        elif n[0] == "e":
            RUNNING_LIST.edit_job(n)

        elif n == "q":
            print("\n    Thank you for using Flow. See you soon!")
            sys.exit()

        elif n == "clear":
            RUNNING_LIST._clear_job_list()

        elif n == "gh":
            RUNNING_LIST.restore_from_history()

        elif n == "l":
            print("""
       ___                _     _         _    _    _   _             _ 
      / __|___ _ __  _ __| |___| |_ ___  | |  (_)__| |_(_)_ _  __ _  (_)
     | (__/ _ \ '  \| '_ \ / -_)  _/ -_) | |__| (_-<  _| | ' \/ _` |  _ 
      \___\___/_|_|_| .__/_\___|\__\___| |____|_/__/\__|_|_||_\__, | (_)
                    |_|                                       |___/     """)      
            RUNNING_LIST.show_list(RUNNING_LIST.current_job_list[1:])
     
        elif n == "o":
            print("""
                                  _ _     _      
       __ _  ___ ___ ___  ___ ___(_) |__ | | ___  _ 
      / _` |/ __/ __/ _ \/ __/ __| | '_ \| |/ _ \(_)
     | (_| | (_| (_|  __/\__ \__ \ | |_) | |  __/ _ 
      \__,_|\___\___\___||___/___/_|_.__/|_|\___|(_) """)
            RUNNING_LIST.show_list(Tools().gimme_my_todo_list(RUNNING_LIST.current_job_list[1:]))

        elif n == "w":
            print("""
                     .__  __  .__                
     __  _  _______  |__|/  |_|__| ____    ____  
     \ \/ \/ /\__  \ |  \   __\  |/    \  / ___\ 
      \     /  / __ \|  ||  | |  |   |  \/ /_/  > _  _  _ 
       \/\_/  (____  /__||__| |__|___|  /\___  / (_)(_)(_)
                   \/                 \//_____/           """)
            RUNNING_LIST.show_list([x for x in RUNNING_LIST.current_job_list[1:] if "Waiting" in x.status])

        elif n == "h":
            with open("hist_log.txt", "rb") as f:
                hist = pickle.load(f, fix_imports=False, encoding="ASCII", errors="strict")
                print("""
             __  ___  __   __      
     |__| | /__`  |  /  \ |__) \ / o
     |  | | .__/  |  \__/ |  \  |  o                   
                                    """)
            RUNNING_LIST.show_list(hist[1:])

        elif n == "m":
            print("""
                                    /--------------------------------------------------------------------------------------------\\
       _____ _____ _____ _____ _    | (O) Show Flow     | (A) Add new Job   | (#) Show Job-info | (E#P) Edit priority |          |
      |     |   __|   | |  |  |_|   |-------------------|-------------------|-------------------|---------------------|----------|
      | | | |   __| | | |  |  |_    | (L) Show All      | (E(#)) Edit Job   | (clear) Clear All | (RL/W/H) PDF-list   |          |
      |_|_|_|_____|_|___|_____|_|   |-------------------|-------------------|-------------------|---------------------|----------|
                                    | (W) Show Waiting  | (D) Delete Job    | (H) Show History  | (gh) Restore Job    | (Q) Quit |
                                    \\--------------------------------------------------------------------------------------------/
                                                                                                         """)
        elif n.isdigit():
            int_n = int(n)
            RUNNING_LIST.show_job_info(int_n)
        else:
            print("\n    {} is not a valid input.".format(n))

        RUNNING_LIST.write_pickle_file()

# Pistetään ohjelma pyörimään
RUNNING_LIST = JobList()
RUNNING_LIST.get_job_list_from_file()

while True:
    Interface.interface()
