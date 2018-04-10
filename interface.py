from tools import tools, JobNotFoundError, ActionCancelledError 
import auth, pickle, traceback, getpass
# Haetaan per_man objekti tiedostosta. Sisältää käytettävät authorizator ja authenticator objektit

per_man = None
RUNNING_LIST = None

def start(input_list):

    global per_man
    global RUNNING_LIST

    RUNNING_LIST = input_list

    try: 
        with open("permissions.txt", "rb") as f:
            per_man = pickle.load(f, fix_imports=False, encoding="ASCII", errors="strict")

    except FileNotFoundError:

        authenticator = auth.Authenticator()
        authorizor = auth.Authorizor(authenticator)
        per_man = PermissionManager(authenticator, authorizor)

        per_man.authenticator.add_user("alfa", "alllfa")
        per_man.authorizor.add_permission("use")
        per_man.authorizor.add_permission("admin")
        per_man.authorizor.permit_user("use", "alfa")
        per_man.authorizor.permit_user("admin", "alfa")

        per_man.write_perm_file()

    # Pistetään ohjelma pyörimään

    try:
        login_or_view = tools.get_valid_input("\n   (l)ogin or (v)iew?", ("l", "v"))
        if login_or_view == "l":
            per_man.login(RUNNING_LIST)                                                           
        elif login_or_view == "v":                                                        
            interface(RUNNING_LIST)                                                       

    except ActionCancelledError:                                                          
        start(RUNNING_LIST)                                                                           

def interface(RUNNING_LIST, username=None):

    global per_man

    n = input("\n{}Enter command\n>>> ".format("<"+username+"> " if username else ""))
    n = n.lower()

    if not per_man.authenticator.is_logged_in(username):
        username = None

    try:
        if len(n) == 0:
            return

        # Making report-pdf's
        if n[0] == "r" and len(n) == 2:
            if n[1] == "o":
                MakePDF().make_report(tools.gimme_my_todo_list(RUNNING_LIST.current_job_list[1:]), "Acceccible Jobs")
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
            per_man.authorizor.check_permission("use", username)
            RUNNING_LIST.add_job()

        elif n == "d":
            per_man.authorizor.check_permission("use", username)
            RUNNING_LIST.delete_job()

        elif n[0] == "e":
            per_man.authorizor.check_permission("use", username)
            RUNNING_LIST.edit_job(n)
            
        elif n == "q":
            print("\n    Thank you for using Flow. See you soon!")
            sys.exit()

        elif n == "clear":
            per_man.authorizor.check_permission("admin", username)
            RUNNING_LIST._clear_job_list()

        elif n == "gh":
            per_man.authorizor.check_permission("use", username)
            RUNNING_LIST.restore_from_history()           

        elif n == "ch":
            per_man.authorizor.check_permission("use", username)
            RUNNING_LIST.copy_from_hist()           

        elif n == "m":
            print("""
                                    
       :::::::::::::::::::::::::::   (O) Show Flow          (A) Add new Job      (E#P) Edit priority      (CH) Copy from hist.     (login) Login        
        _____ _____ _____ _____ _                                                                                                                             
       |     |   __|   | |  |  |_|   (L) Show All           (E(#)) Edit Job      (H) Show History         (GH) Restore from hist.  (logout) Logout                        
       | | | |   __| | | |  |  |_                                                                                                                             
       |_|_|_|_____|_|___|_____|_|   (W) Show Waiting       (D) Delete Job       (S[H]) Search[hist]      (RL/W/H) Print PDF-list  (admin) Admin-menu                          
       ___________________________                                                                                                               
       l_________________________l   (#) Show Job-info      (MU/D#[N]) Move \u25B2/\u25BC  (clear) Clear list       (Q) Quit                           

                                                                                                         
       """)

        elif n[0] == "m":
            per_man.authorizor.check_permission("use", username)
            RUNNING_LIST.move(n)

        elif n == "s":
            search_term = input("\n Search for: ")
            RUNNING_LIST.show_list(tools.search(RUNNING_LIST.current_job_list[1:], search_term))

        elif n == "sh":
            search_term = input("\n Search for: ")
            hist = RUNNING_LIST.get_hist()
            RUNNING_LIST.show_list(tools.search(hist[1:], search_term))

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
            RUNNING_LIST.show_list(tools.gimme_my_todo_list(RUNNING_LIST.current_job_list[1:]))
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
            per_man.login(RUNNING_LIST, username)
            return

        elif n == "admin":
            per_man.authorizor.check_permission("admin", username)
            per_man.admin_menu(username)
            return

        elif n == "logout":
            per_man.authenticator.logout(username)
            username = None
            return

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
        interface(RUNNING_LIST, username)

#Manage permissions

# prompt login
# Check if user is authorized
# If user is authorized, let them use the program 

class PermissionManager:
    def __init__(self, authenticator, authorizor):
        self.authenticator = authenticator
        self.authorizor = authorizor

    def write_perm_file(self):
        with open("permissions.txt", "wb") as f:
            pickle.dump(self, f, protocol=4, fix_imports=False)

    def login(self, RUNNING_LIST, username=None):
        if not username:
            try:
                username = input("Username: ")
                password = getpass.getpass("Password: ")
                self.authenticator.login(username, password)
            except auth.InvalidUsername as e:
                print("Invalid username", e)
                per_man.login(RUNNING_LIST)
            except auth.InvalidPassword as e:
                print("Invalid password")
                per_man.login(RUNNING_LIST)
            else:
                try:
                    self.authenticator.is_logged_in(username)
                except auth.NotLoggedInError as e:
                    print("\n    NotLoggedInError raised", e)
                except auth.PermissionError as e:
                    print("PermissionError raised", e)
                else:
                    print("\n    Login succesful")
                    interface(RUNNING_LIST, username)
        else:
            print("\n    You are currently logged in as", username)

    def admin_menu(self, username):

        n = tools.get_valid_input("""
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
            self.authenticator.add_user(input("\nNEW USER - Username: "), input("\nNEW USER - Password: "))
        elif n == "ap":
            self.authorizor.add_permission(input("\nNEW PERMISSION - Permission name: "))
        elif n == "pu":
            self.authorizor.permit_user(input("\nPERMIT USER - perm_name: "), input("\nPERMIT USER - Username: "))
        elif n == "vu":
            self.authenticator.view_users()
        elif n == "lo":
            self.authenticator.logout(input("\nType username you wan't to logout: "))
        elif n == "qu":
            interface(RUNNING_LIST, username)
        elif n == "vp":
            self.authorizor.view_permissions()
        elif n == "de":
            user_to_del = input("\nType username you wan't to delete: ")
            sure = tools.get_valid_input("\nAre you sure you wan't to delete user: {}".format(user_to_del), ("y", "n"))

            self.authenticator.del_user(user_to_del) if sure == "y" else self.admin_menu(username)

        self.write_perm_file()
        self.admin_menu(username)


