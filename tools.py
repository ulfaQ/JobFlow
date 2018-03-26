def get_valid_input(input_string, valid_options):
    """ Ottaa inputin ja kattoo onko se toisena argumenttina annetussa listassa (tuplea käytetään näissä tapauksisssa) 
    kysyy uudelleen niin kauan kunnes inputti on validi
    palauttaa annetun inputin kun se on validi"""

    input_string += " ({}) ".format(", ".join(valid_options))
    response = input(input_string)
    while response.lower() not in valid_options:
        response = input(input_string)
    return response

def edit_job(job_list, job_id):
    # Palauttaa prompted info objektin jota käytetään luomaan uusi Job vanhan tilalle (sama objekti mutta vain yhdellä muokatulla parametrillä. 
    # if input == "n" kohdassa jobflow.py:n loppupuolella. Kutsutaan tätä funktiota.

    temp_prompted_info = None
    temp_job_object = None
    parameter = None

    #etsitään listasta oikea Job-objekti --> temp_job_object, ja kysytään mitä parametria halutaan muokata --> parameter
    for i in job_list:
        print("For i in job list")
       
        if i.id == int(job_id):
            temp_job_object = i
            temp_prompted_info = i.prompted_info
            print("Customer is: ", i.prompted_info["customer"])

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

 Choose the Parameter to Edit: """.format(i.id, i.addedDate, i.customer, i.product, i.amount, i.material, \
                                i.printing_sheet_size, i.comment, i.status, i.priority), ("1", "2", "3", "4", "5", "6", "7", "8", "a", "c", "s", "p"))
        
            break

    def edit(temp_prompted_info, parameter):    
        print("parameter is: ", parameter)
        if   parameter == "1":  # Customer
            n = input("""
            Add new value for CUSTOMER: """)
            temp_prompted_info["customer"] = n                                
                                                 
        elif parameter == "2":  # Product 
            n = input("""
            Add new value for PRODUCT: """)
            temp_prompted_info["product"] = n                                
                                                 
        elif parameter == "3" or parameter.lower() == "a":  # Amount
            n = input("""
            Add new value for AMOUNT: """)
            temp_prompted_info["amount"] = n                                
                                                 
        elif parameter == "4":  # Material
            n = input("""
            Add new value for MATERIAL: """)
            temp_prompted_info["material"] = n                                
                                                 
        elif parameter == "5":  # PrintSheetSize
            n = input("""
            Add new value for PrintSheetSize: """)
            temp_prompted_info["printing_sheet_size"] = n                                
                                                 
        elif parameter == "6" or parameter.lower() == "c":  # Comment
            n = input("""
            Add new value for COMMENT: """)
            temp_prompted_info["comment"] = n                                
                                                 
        elif parameter == "7" or parameter.lower() == "s":  # Status
            n = get_valid_input("Add new value for STATUS: (1=ReadyToPrint, 2=Waiting)", ("1","2"))
            # Muokataan statusta siten että jos input on 2, kysytään syytä mitä odottaa,
            # Jos input on 1, laitetaan statukseksi ready to print
            if n == "2":
                waiting_for_what = input("Waiting for what?: ")
                temp_prompted_info["status"] = "Waiting for: " + waiting_for_what 
            elif n == "1":
                temp_prompted_info["status"] = "Ready to Print"

        elif parameter == "8" or parameter.lower() == "p":  # Priority
            n = get_valid_input("""
            Add new value for PRIORITY (1=Extremely Urgent, 2=Very Urgent, 3=Urgent, 0=Normal priority) """, ("1", "2", "3", "0"))
            temp_prompted_info["priority"] = int(n)                               

    edit(temp_prompted_info, parameter)
    return temp_prompted_info

def gimme_waiting_jobs(list_of_jobs):
    """ This give a list of all jobs with status: Waiting (2) """

    temp_list = []
    for i in list_of_jobs:
        if "Waiting" in i.status:
            temp_list.append(i)
    return temp_list

def gimme_my_todo_list(list_of_jobs):
    """ At the moment this only takes out all "Waiting"-jobs and arranges all urgent jobs to the top by priority."""

    priority1_jobs = []
    priority2_jobs = []
    priority3_jobs = []
    priority0_jobs = []
    
    for i in list_of_jobs:
        if i.status == "Ready to Print":
            if int(i.priority) == 1:
                priority1_jobs.append(i)
            elif int(i.priority) == 2:
                priority2_jobs.append(i)
            elif int(i.priority) == 3:
                priority3_jobs.append(i)
            elif int(i.priority) == 0:
                priority0_jobs.append(i)

    temp_list = []

    for i in priority1_jobs:
        temp_list.append(i)
    for i in priority2_jobs:
        temp_list.append(i)
    for i in priority3_jobs:
        temp_list.append(i)
    for i in priority0_jobs:
        temp_list.append(i)
    
    return temp_list
