import datetime

class JobNotFoundError(Exception):
    pass

class ActionCancelledError(Exception):
    def __init__(self):
        self.string = "\n    Action Cancelled"

class Tools:
    def get_job_by_id(self, job_id, input_list):
        for job in input_list:
            if job.job_id == job_id:
                return job

        raise JobNotFoundError
        
    def get_valid_input(self, input_string, valid_options=None):
        """ Ottaa inputin ja kattoo onko se toisena argumenttina annetussa listassa
            (tuplea käytetään näissä tapauksisssa) 
            kysyy uudelleen niin kauan kunnes inputti on validi.
            Palauttaa validin inputin (string)
        """

        if valid_options:
            input_string += " ({}) ".format(", ".join(valid_options))
            response = input(input_string)

            if response == "q":
                raise ActionCancelledError

            while response.lower() not in valid_options:
                response = input(input_string)

        # Jos valid_options == None, kysyy vain kysymyksen(input_string) ja palauttaa vastauksen, sen kummempia validoimatta.

        elif valid_options == None:
            response = input(input_string)
            if response == "q":
                raise ActionCancelledError

        return response

#   def get_status(self, number):

#       if number == "2":
#           number = "Waiting for: {}".format(input("Waiting for what?: "))

#       elif number == "1":
#           number = "Ready to Print"

#       elif number == "q":
#           raise ActionCancelledError

#       return number

    def add_or_edit_job(self, job, id_input=None, parameter=None):
        """ Palauttaa prompted info objektin jota käytetään luomaan uusi Job vanhan tilalle 
            (sama objekti mutta vain yhdellä muokatulla parametrillä.
            if input == "e" kohdassa jobflow.py:n loppupuolella. Kutsutaan tätä funktiota. 
        """

        if job:
            if parameter == None:
                parameter = self.get_valid_input("""
                      -----------------------------------------
                      Which of the parameters you want to Edit?
                      -----------------------------------------
                      Job Id: {} - Added: {}
                      
                           Parameter (Num) Current value
                           --------- ----- -------------
                            Customer  (1)  {}
                             Product  (2)  {}
                              Amount (3,A) {}
                            Material  (4)  {}
                      PrintSheetSize  (5)  {}
                             Comment (6,C) {}
                              Status (7,S) {}
                            Priority (8,P) {}

                              Cancel  (Q)  



             Choose the Parameter to Edit: """.format(job.job_id, job.addedDate, job.customer, job.product, job.amount, job.material, \
                                            job.printing_sheet_size, job.comment, job.status, job.priority), \
                                            ("1", "2", "3", "4", "5", "6", "7", "8", "a", "c", "s", "p", "q"))
                
            # Luodaan dictionary josta katsotaan mitä parametria annetulla numerolla/kirjaimella tarkoitetaan
            # inputsissa ensin parametri, sitten get_valid_inputiin syötettävät validit inputit. Jos None, sitten validointia ei tehdä.
            inputs = {
                    "1" : ["customer", None],
                    "2" : ["product", None],
                    "3" : ["amount", None],
                    "a" : ["amount", None],
                    "4" : ["material", None],
                    "5" : ["printing_sheet_size", None],
                    "6" : ["comment", None],
                    "c" : ["comment", None],
                    "7" : ["status", ("1" ,"2", "q")],
                    "s" : ["status", ("1" ,"2")],
                    "8" : ["priority", ("1" ,"2", "3", "0")],
                    "p" : ["priority", ("1" ,"2", "3", "0")]
                    }

            job.prompted_info[inputs[parameter][0]] = self.get_valid_input("\nGive new value for {} : ".format(inputs[parameter][0]), inputs[parameter][1])
#            job.prompted_info["status"] = self.get_status(job.prompted_info["status"])

            print("\n   ", inputs[parameter][0].upper(), "succesfully updated!")

            return job.prompted_info

        else:
            prompted_info = {
                    "customer"             : self.get_valid_input("Customer: ", None),         
                    "product"              : self.get_valid_input("Product: ", None),
                    "amount"               : self.get_valid_input("Amount: ", None),           
                    "material"             : self.get_valid_input("Material: ", None),        
                    "comment"              : self.get_valid_input("Comment: ", None),          
                    "printing_sheet_size"  : self.get_valid_input("Printing_sheet_size: ", None),
                    "job_id"               : id_input,  # self.info.current_id passed as a 
                                                        # second (optional) parameter in 
                                                        # jobflow.py add_job()
                    "addedDate"            : datetime.datetime.now().strftime("%d-%m %H:%M"),
                    "status"               : self.get_valid_input("Status 1=ReadyToPrint, 2=Waiting: ", ("1","2","q")),
                    "priority"             : "0"
                    }

            return prompted_info

    def gimme_my_todo_list(self, list_of_jobs):
        """ This returns a list containing only "Ready to Print" jobs This arranges all priority-status 1-3 jobs by priority."""

        acceccible_jobs = [x for x in list_of_jobs if "Waiting" not in x.status]
        ordered_list = list()
        count = 0

        for item in acceccible_jobs:

            if item.priority == "1":
                ordered_list.insert(count, item)
                count += 1

            elif item.priority == "2":
                ordered_list.append(item)

        for item in acceccible_jobs:
            if item.priority == "3":
                ordered_list.append(item)

        for item in acceccible_jobs:
            if item.priority == "0":
                ordered_list.append(item)

        return ordered_list

    def search(self, input_list, search_term):
        temp_list = list()
        term_list = search_term.split(" ")
        for job in input_list:
            job_string = job.customer.lower() + " " + job.product.lower()
            terms_found = 0
            for term in term_list:
                if term in job_string:
                    terms_found += 1
            if terms_found == len(term_list):
                temp_list.append(job)

# Etsii työt jotka sisältää mitkä tahansa annetuista sanoista
#       temp_list = list()
#       for term in search_term.split(" "):
#           for job in input_list:
#               job_string = job.customer.lower() + " " + job.product.lower()
#               
#               if term in job_string:
#                   temp_list.append(job)

        return temp_list

    def rivitetty(self, long_string, row_length):
        """ Palauttaa lauseen sanat jaettuna listan elementteihin siten että yhdellä rivillä on aina maksimissaa row_length verran merkkejä."""
        words = long_string.rsplit()
        rows = [[]]
        count = 0
        for i in words:
            if len(" ".join(rows[count]) + i)  < row_length:
                rows[count].append(i)
            else:
                rows.append([])
                count += 1
                rows[count].append(i)

        joined_rows = []
        for i in rows:
            joined_rows.append(" ".join(i))
        return joined_rows

tools = Tools()
