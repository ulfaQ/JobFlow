import datetime

def get_valid_input(input_string, valid_options):
    """ Ottaa inputin ja kattoo onko se toisena argumenttina annetussa listassa (tuplea käytetään näissä tapauksisssa) 
    kysyy uudelleen niin kauan kunnes inputti on validi
    palauttaa annetun inputin kun se on validi"""

    if valid_options:
        input_string += " ({}) ".format(", ".join(valid_options))
        response = input(input_string)

        while response.lower() not in valid_options:
            response = input(input_string)

    # Jos valid_options == None, kysyy vain kysymyksen(input_string) ja palauttaa vastauksen, sen kummempia validoimatta.
    else:
        response = input(input_string)

    return response

def get_status(number):

    if number == "2":
        number = "Waiting for: {}".format(input("Waiting for what?: "))

    elif number == "1":
        number = "Ready to Print"

    return number

def add_or_edit_job(job, id_input=None):

    # Palauttaa prompted info objektin jota käytetään luomaan uusi Job vanhan tilalle (sama objekti mutta vain yhdellä muokatulla parametrillä. 
    # if input == "e" kohdassa jobflow.py:n loppupuolella. Kutsutaan tätä funktiota.
    if job:

        parameter = get_valid_input("""
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

     Choose the Parameter to Edit: """.format(job.id, job.addedDate, job.customer, job.product, job.amount, job.material, \
                                    job.printing_sheet_size, job.comment, job.status, job.priority), \
                                    ("1", "2", "3", "4", "5", "6", "7", "8", "a", "c", "s", "p"))

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
                "7" : ["status", ("1" ,"2")],
                "s" : ["status", ("1" ,"2")],
                "8" : ["priority", ("1" ,"2", "3")],
                "p" : ["priority", ("1" ,"2", "3")],
                }

        job.prompted_info[inputs[parameter][0]] = get_valid_input("\nGive new value for {} : ".format(inputs[parameter][0]), inputs[parameter][1])
        job.prompted_info["status"] = get_status(job.prompted_info["status"])

        return job.prompted_info

    else:
        prompted_info = {
                "customer"             : input("Customer: "),         
                "product"              : input("Product: "),
                "amount"               : input("Amount: "),           
                "material"             : input("Material: "),         
                "comment"              : input("Comment: "),          
                "printing_sheet_size"  : input("Printing_sheet_size: "),
                "current_id"           : id_input, # self.info.current_id passed as a second (optional) parameter in jobflow.py add_job()
                "addedDate"            : datetime.datetime.now().strftime("%d-%m %H:%M"),
                "status"               : get_status(get_valid_input("Status 1=ReadyToPrint, 2=Waiting: ", ("1","2"))),
                "priority"             : "0"
                }

        return prompted_info

def gimme_my_todo_list(list_of_jobs):
    """ This arranges all priority-status 1-3 jobs by priority."""

    acceccible_jobs = [x for x in list_of_jobs if "Waiting" not in x.status]
    ordered_list = list()
    count = 0

    for item in acceccible_jobs:

        if item.priority == "1":
            ordered_list.insert(count, item)
            count += 1

        if item.priority == "2":
            ordered_list.append(item)

    for item in acceccible_jobs:

        if item.priority == "3":
            ordered_list.append(item)

    for item in acceccible_jobs:
        
        if int(item.priority) == 0:
            ordered_list.append(item)

    return ordered_list
