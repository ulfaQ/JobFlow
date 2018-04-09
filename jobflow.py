import time, datetime, os, pickle, sys, re
# Own modules:
from tools import Tools, JobNotFoundError, ActionCancelledError
from files import Files
from pdf_generator import MakePDF
import auth
import traceback

Files.check_files()

print(""" 
      ______   __         ______     __     __    
     /\  ___\ /\ \       /\  __ \   /\ \  _ \ \   
     \ \  __\ \ \ \____  \ \ \/\ \  \ \ \/ ".\ \  
      \ \_\    \ (c)Aku\  \ \_____\  \ \__/".~\_\ 
       \///     \///////   \///////   \///   \/// 
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
                job_to_move = Tools().get_job_by_id(id_to_move, cur_jobs[1:])
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
        self.status = prompted_info.get("status")
        self.comment = prompted_info.get("comment")
        self.addedDate = prompted_info.get("addedDate")
        self.job_id = prompted_info.get("job_id")
        self.priority = prompted_info.get("priority") 
        
# Interface:
class Interface:
    def interface(username=None):
        if not permission_manager.authenticator.is_logged_in(username):
            username = None

        n = input("\n{}Enter command\n>>> ".format("<"+username+"> " if username else ""))
        n = n.lower()

        try:
            if len(n) == 0:
                return

            # Making report-pdf's
            if n[0] == "r" and len(n) == 2:
                if n[1] == "o":
                    MakePDF().make_report(Tools().gimme_my_todo_list(RUNNING_LIST.current_job_list[1:]), "Acceccible Jobs")
                    print("\n    Created a PDF report of all accessible jobs.")
                elif n[1] == "l":
                    MakePDF().make_report(RUNNING_LIST.current_job_list[1:], "All Jobs")
                    print("\n    Created a PDF report of all jobs.")
                elif n[1] == "w":
                    current_list = RUNNING_LIST.current_job_list[1:]
                    MakePDF().make_report([x for x in current_list if "Waiting" in x.status], "Waiting Jobs")
                    print("\n    Created a PDF report of all waiting jobs.")
            # End report-pdf's

            elif n == "a":
                permission_manager.authorizor.check_permission("use", username)
                RUNNING_LIST.add_job()

            elif n == "d":
                permission_manager.authorizor.check_permission("use", username)
                RUNNING_LIST.delete_job()

            elif n[0] == "e":
                permission_manager.authorizor.check_permission("use", username)
                RUNNING_LIST.edit_job(n)
                
            elif n == "q":
                print("\n    Thank you for using Flow. See you soon!")
                sys.exit()

            elif n == "clear":
                permission_manager.authorizor.check_permission("use", username)
                RUNNING_LIST._clear_job_list()

            elif n == "gh":
                permission_manager.authorizor.check_permission("use", username)
                RUNNING_LIST.restore_from_history()           

            elif n == "m":
                print("""
                                        
           _____ _____ _____ _____ _     (O) Show Flow      (A) Add new Job   (#) Show Job-info   (E#P) Edit priority   (MU/D#[N]) Move Up/Down[By]   (admin) Administration
          |     |   __|   | |  |  |_|   
          | | | |   __| | | |  |  |_     (L) Show All       (E(#)) Edit Job   (clear) Clear All   (RL/W/H) PDF-list     (login) Login                 (Q) Quit             
          |_|_|_|_____|_|___|_____|_|  
                                         (W) Show Waiting   (D) Delete Job    (H) Show History    (GH) Restore Job      (logout) Logout                              
                                      
                                                                                                             """)

            elif n[0] == "m":
                permission_manager.authorizor.check_permission("use", username)
                RUNNING_LIST.move(n)

            elif n == "l":
                print("""
           ___                _     _         _    _    _   _             _ 
          / __|___ _ __  _ __| |___| |_ ___  | |  (_)__| |_(_)_ _  __ _  (_)
         | (__/ _ \ '  \| '_ \ / -_)  _/ -_) | |__| (_-<  _| | ' \/ _` |  _ 
          \___\___/_|_|_| .__/_\___|\__\___| |____|_/__/\__|_|_||_\__, | (_)
                        |_|                                       |___/     """)      
                RUNNING_LIST.show_list(RUNNING_LIST.current_job_list[1:])
                return
         
            elif n == "o":
                print("""
                                      _ _     _      
           __ _  ___ ___ ___  ___ ___(_) |__ | | ___  _ 
          / _` |/ __/ __/ _ \/ __/ __| | '_ \| |/ _ \(_)
         | (_| | (_| (_|  __/\__ \__ \ | |_) | |  __/ _ 
          \__,_|\___\___\___||___/___/_|_.__/|_|\___|(_) """)
                RUNNING_LIST.show_list(Tools().gimme_my_todo_list(RUNNING_LIST.current_job_list[1:]))
                return

            elif n == "w":
                print("""
                         .__  __  .__                
         __  _  _______  |__|/  |_|__| ____    ____  
         \ \/ \/ /\__  \ |  \   __\  |/    \  / ___\ 
          \     /  / __ \|  ||  | |  |   |  \/ /_/  > _  _  _ 
           \/\_/  (____  /__||__| |__|___|  /\___  / (_)(_)(_)
                       \/                 \//_____/           """)
                RUNNING_LIST.show_list([x for x in RUNNING_LIST.current_job_list[1:] if "Waiting" in x.status])
                return

            elif n == "h":
                with open("hist_log.txt", "rb") as f:
                    hist = pickle.load(f, fix_imports=False, encoding="ASCII", errors="strict")
                    print("""
                 __  ___  __   __      
         |__| | /__`  |  /  \ |__) \ / o
         |  | | .__/  |  \__/ |  \  |  o                   
                                        """)
                RUNNING_LIST.show_list(hist[1:])
                return

            elif n.isdigit():
                int_n = int(n)
                RUNNING_LIST.show_job_info(int_n)
                return

            elif n == "login":
                login(username)

            elif n == "admin":
                permission_manager.authorizor.check_permission("admin", username)
                admin_menu(username)

            elif n == "logout":
                permission_manager.authenticator.logout(username)

            else:
                print("\n    {} is not a valid command. See (m) for Menu.".format(n))
                return

        except auth.NotPermittedError:
            print("\n    You are not permitted to do that")
        except auth.NotLoggedInError:
            print("\n    You must be logged in to modify list")
        except ActionCancelledError:
            print("\n    Job editing cancelled")
        except Exception as ex:
            print("Some weird exception raised")
            print(traceback.print_exc())
        else:
            RUNNING_LIST.write_pickle_file()
        finally:
            Interface.interface(username)

# Pistetään ohjelma pyörimään
RUNNING_LIST = JobList()
RUNNING_LIST.get_job_list_from_file()

# prompt login
# Check if user is authorized
# If user is authorized, let them use the program 

class PermissionManager:
    def __init__(self, authenticator, authorizor):
        self.authenticator = authenticator
        self.authorizor = authorizor

permission_manager = None

with open("permissions.txt", "rb") as f:
    loaded_file = pickle.load(f, fix_imports=False, encoding="ASCII", errors="strict")
    permission_manager = PermissionManager(loaded_file[0], loaded_file[1])

def write_perm_file():
    with open("permissions.txt", "wb") as f:
        pickle.dump([permission_manager.authenticator, permission_manager.authorizor], f, protocol=4, fix_imports=False)

def login(username=None):
    if not username:
        try:
            username = input("Username: ")
            password = input("Password: ")
            permission_manager.authenticator.login(username, password)
        except auth.InvalidUsername as e:
            print("Invalid username", e)
            login()
        except auth.InvalidPassword as e:
            print("Invalid password")
            login()
        else:
            try:
                permission_manager.authenticator.is_logged_in(username)
            except auth.NotLoggedInError as e:
                print("\n    NotLoggedInError raised", e)
            except auth.PermissionError as e:
                print("PermissionError raised", e)
            else:
                print("\n    Login succesful")
                Interface.interface(username)
    else:
        print("\n    You are currently logged in as", username)

def admin_menu(username):
    n = Tools().get_valid_input("""
    ADMIN MENU: 

    add user         = au
    del user         = de
    add permission   = ap
    permit user      = pu
    view users       = vu
    view permissions = vp
    log user out     = lo
    quit admin menu  = qu

<{}> Enter command:
>>> ADMIN >>> """.format(username), ("au", "de", "ap", "pu", "vu", "vp", "lo", "qu"))

    if n == "au":
        permission_manager.authenticator.add_user(input("\nNEW USER - Username: "), input("\nNEW USER - Password: "))
    elif n == "ap":
        permission_manager.authorizor.add_permission(input("\nNEW PERMISSION - Permission name: "))
    elif n == "pu":
        permission_manager.authorizor.permit_user(input("\nPERMIT USER - perm_name: "), input("\nPERMIT USER - Username: "))
    elif n == "vu":
        permission_manager.authenticator.view_users()
    elif n == "lo":
        permission_manager.authenticator.logout(input("\nType username you wan't to logout: "))
    elif n == "qu":
        Interface.interface(username)
    elif n == "vp":
        permission_manager.authorizor.view_permissions()
    elif n == "de":
        user_to_del = input("\nType username you wan't to delete: ")
        sure = Tools().get_valid_input("\nAre you sure you wan't to delete user: {}".format(user_to_del), ("y", "n"))

        permission_manager.authenticator.del_user(user_to_del) if sure == "y" else admin_menu(username)

    write_perm_file()
    admin_menu(username)

#   # for making a initial admin user:
#   permission_manager.authenticator.add_user("alfa", "billion")
#   permission_manager.authorizor.add_permission("admin")
#   permission_manager.authorizor.add_permission("use")
#   permission_manager.authorizor.permit_user("admin", "alfa")
#   write_perm_file()

def start():
    try:
        login_or_view = Tools().get_valid_input("\n   (l)ogin or (v)iew?", ("l", "v"))
        if login_or_view == "l":
            login()
        elif login_or_view == "v":
            Interface.interface()
    except ActionCancelledError:
        start()
        
start()
