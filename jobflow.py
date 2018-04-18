import time, datetime, os, pickle, sys, re, traceback

# Own modules:
from tools import tools, JobNotFoundError, ActionCancelledError
from files import Files
from pdf_generator import MakePDF
from interface import interface, start
Files.check_files()

print(""" 
                          ______   __         ______     __     __    
                         /\  ___\ /\ \       /\  __ \   /\ \  _ \ \   
                         \ \  __\ \ \ \____  \ \ \/\ \  \ \ \/ ".\ \  
                          \ \_\    \ \     \  \ \_____\  \ \__/".~\_\ 
#####################################################################
---------------------------------------------------------------------
                     """)

class JobList:
    """ Class for managing jobs, Instance of this class is created in the last lines """

    # Tehdään lista jossa säilytetään Jobit ajon aikana.
    def __init__(self):
        self.current_job_list = []
        self.info = None # Tähän haetaan info-objekti tiedostosta. Sisältää muuta infoa joka halutaan säilyttää
        self.history = None

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

    def get_hist(self):
        with open("hist_log.txt", "rb") as f:
            hist = pickle.load(f, fix_imports=False, encoding="ASCII", errors="strict")
        return hist

    def copy_from_hist(self):
        hist = self.get_hist()
        job_to_copy = input("\nType the the id of the job you wan't to copy: ")
        temp_job = None
        if job_to_copy.isdigit():
            job_to_copy = int(job_to_copy)
        else:
            print("\n    {} is not valid input. ID can only contain integers.".format(id_to_remove))
            return

        for job in hist[1:]:
            if job.job_id == job_to_copy:
                temp_job = job
                temp_job.addedDate = datetime.datetime.now().strftime("%d-%m %H:%M")
                temp_job.status = tools.get_valid_input("\nGive new value for STATUS", ("1","2"))
                temp_job.job_id = self.info.current_id
                self.info.current_id += 1
                self.current_job_list.append(temp_job)
                break

    def write_hist(self, new_hist):
        with open("hist_log.txt", "wb") as f:
            pickle.dump(new_hist, f, protocol=4, fix_imports=False)

    # Funktio töiden lisäämiseen. 
    def add_job(self):

        print("\n    ENTERING NEW JOB\n")
        self.current_job_list.append(Job(tools.add_or_edit_job(None, self.info.current_id)))
        print("\n   Job {} added!".format(self.info.current_id))
        self.info.current_id += 1

    def delete_job(self):
        """ Poistaa id:n perusteella valitun työn. """
        id_to_remove = input("\nType the ID of the Job you wan't to delete: ")

        if id_to_remove.isdigit():
            id_to_remove = int(id_to_remove)
        else:
            print("\n    {} is not valid input. ID can only contain integers.".format(id_to_remove))
            return

        n = None
        for i in self.current_job_list[1:]:
            if i.job_id == id_to_remove:

                n = tools.get_valid_input("Are you sure you wan't to remove {} : {} : {} : {} : {} ?".format("ID: ", i.job_id, i.customer, i.product, i.amount), ("y", "n")).lower()

                if n == "y":
                    self.current_job_list.remove(i)
                    i.status = ("DELETED {}".format(datetime.datetime.now().strftime("%d-%m-%Y %H:%M")))
                    #Tallennetaan hist_logiin poistettu työ
                    temp_hist_log = self.get_hist()
                    temp_hist_log.append(i)
                    self.write_hist(temp_hist_log)
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
                self.current_job_list[index_of_the_job] = Job(tools.add_or_edit_job(i, None, parameter))
                return

        print("\n    ID {} NOT FOUND".format(input_id))
        
    def show_list(self, job_list):

        if job_list == []:
            print("\n    No jobs of this kind.")
            return

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
                rivitetty_comment = tools.rivitetty(i.comment, len(i.status) + 13)
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
        n = tools.get_valid_input("Are you sure you wan't to remove all jobs from current_job_list permanently. \
Jobs removed by 'clear' are not saved to history. ", ("y", "n"))
        if n == "y":
            self.current_job_list[1:] = []
        if n == "n":
            print("\n   CLEAR CANCELLED")

    def restore_from_history(self):
        n = input("\nType the ID of the job you wan't to restore: ")
        job_found = False
        temp_hist_log = self.get_hist()
        for job in temp_hist_log[1:]:
            if job.job_id == int(n):
                job_found = True
                job.status = tools.get_valid_input("Input a new STATUS for restored job:", ("1","2"))
                temp_hist_log.remove(job)
                self.current_job_list.append(job)
                self.write_hist(temp_hist_log)
                print("\n    Job {} succesfully restored from history!".format(n))
                return

        if not job_found:
            print("\n    Job id {} not found.".format(n))
    
    def move(self, usr_input):
        """ In the interface, user can input a string starting with mu or md, depending of direction of movement.
        Next in the string must come the ID of the job, that wan'ts to be moved.
        An optional third argument is the 'n', which indicates, that the user want's to move the item by
        a number of times. (this number is asked if the 'n' is detected """

        #Check if we can use that input. If we can, use it.
        if re.fullmatch("[m][u,d][\d]+[n]?", usr_input):

            # get direction from usr_input
            direction = usr_input[1]

            # get id from usr_input and if last character is n, then ask how many times user wants to move item
            id_to_move = None
            if usr_input[-1] == "n":
                while True:
                    how_many_times = input("\nMove {} by :".format("UP" if direction == "u" else "DOWN"))
                    if how_many_times.isdigit():
                        how_many_times = int(how_many_times)
                        break
                    else:
                        print("\n    Not a number.")

                id_to_move = int(usr_input[2:-1])
            else:
                id_to_move = int(usr_input[2:])
                how_many_times = 1

            cur_jobs = self.current_job_list
            try:
                job_to_move = tools.get_job_by_id(id_to_move, cur_jobs[1:])
            except JobNotFoundError:
                print("\n    Job {} not found".format(id_to_move))
                return

            index_of_target_position = None

            # Check if user is trying to move job too far (in place of the info object or over OR over the end of the list.) 
            # stop execution if this is the case

            if direction == "u":
                index_of_target_position = cur_jobs.index(job_to_move) - how_many_times

            if direction == "d":
                index_of_target_position = cur_jobs.index(job_to_move) + how_many_times

            if index_of_target_position < 1 or index_of_target_position > len(cur_jobs) - 1:
                print("\n    Cannot move {} by {}".format(id_to_move, how_many_times))
                return

            index_of_old_position = self.current_job_list.index(job_to_move)
            cur_jobs.insert(index_of_target_position, cur_jobs.pop(index_of_old_position))
            
            print("\n    Job {} succesfully moved {} by {}".format(id_to_move, 
                "UP" if direction == "u" else "DOWN", how_many_times))

        else:
            print("\n    move() can't use input:", usr_input)

class Job:
    def __init__(self, prompted_info):
        self.prompted_info = prompted_info
        self.customer = prompted_info.get("customer")
        self.product = prompted_info.get("product")
        self.amount = prompted_info.get("amount")
        self.material = prompted_info.get("material")
        self.printing_sheet_size = prompted_info.get("printing_sheet_size")
        # Status in prompted_info is always 1 or 2
        self._status = prompted_info.get("status")
        # Setting status to corresponding value with property (Ready../Waiting...)
        self.status = self._status
        self.comment = prompted_info.get("comment")
        self.addedDate = prompted_info.get("addedDate")
        self.job_id = prompted_info.get("job_id")
        self.priority = prompted_info.get("priority") 

    def _set_status(self, status_nro):
        if status_nro == "1":
            self._status = "Ready to Print"
        elif status_nro == "2":
            n = input("\nWaiting for what: ")
            self._status = "Waiting for: " + n

    def _get_status(self):
        return self._status

    status = property(_get_status, _set_status)

# Pistetään ohjelma pyörimään
RUNNING_LIST = JobList()
RUNNING_LIST.get_job_list_from_file()

start(RUNNING_LIST)
