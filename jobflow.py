import time, datetime, os, pickle
print(""" 
         Welcome to:
         ___.     ___.   __________.                  
        |   | ____\_ |__ \_  ____/ | ______  _  __.  
        |   |/  _ \| __ \ |   _)|  |/  _ \ \/ \/ / 
    /\__|   (  <_> ) \_\ \|   \ |  (  <_> )     /  
    \_______|\____/|___  /\_  / |__|\____/ \/\_/   
                       \/   \/  I'm Your brain now.

   """)

def get_valid_input(input_string, valid_options):
    """ Ottaa inputin ja kattoo onko se toisena argumenttina annetussa listassa (tuplea käytetään näissä tapauksisssa) """

    input_string += " ({}) ".format(", ".join(valid_options))
    response = input(input_string)
    while response.lower() not in valid_options:
        response = input(input_string)
    return response



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
            "addedDate"            : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status"               : get_valid_input("Status: (1=ReadyToPrint, 2=Waiting)", ("1","2"))
            }

        self.current_job_list.append(Job(**prompted_info))
        self.info.current_id += 1
        with open("current_job_list.txt", "wb") as f:
            pickle.dump(self.current_job_list, f, protocol=4, fix_imports=False)

    def remove_job(self, id_to_remove):
        """ Poistaa id:n perusteella valitun työn. """
        for i in self.current_job_list[1:]:
            if i.id == id_to_remove:
                n = input("Are you sure you wan't to remove {} : {} : {} : {} : {} \
                        - (y ,n): ".format(i.id, i.addedDate, i.customer, i.product, i.amount)).lower()
                if n == "y":
                    self.current_job_list.remove(i)

        with open("current_job_list.txt", "wb") as f:
            pickle.dump(self.current_job_list, f, protocol=4, fix_imports=False)

    def show_jobs(self):
        print("""
                -------------------------
                List of all jobs in queue
                -------------------------""")
        for i in self.current_job_list[1:]:
            print("               ", i.id, ":", i.addedDate, i.customer, i.product, i.amount)

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
                """.format(i.id, i.addedDate, i.customer, i.product, i.amount,\
                        i.material, i.printing_sheet_size, i.comment, i.status))
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
    print("Add Job: 1, Show all Jobs: 2, Delete Job: 3, Show details of a Job: 4")
    n = input("What you wanna do?: ")
    if n == "1":
        print("ADD JOB:\n")
        my_job_list.add_job()
    elif n == "2":
        print(my_job_list.show_jobs())
    elif n == "3":
        rm = int(input("Type the ID of the job you wan't to remove: "))
        my_job_list.remove_job(rm)
    elif n == "4":
        sh = int(input("Type the ID of the job you wan't to show details of: "))
        my_job_list.show_job(sh)
    elif n == "clear":
        my_job_list._clear_job_list()

