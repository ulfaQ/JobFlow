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

    temp_job_object = None
    parameter = None

    #etsitään listasta oikea Job-objekti --> temp_job_object, ja kysytään mitä parametria halutaan muokata --> parameter
    for i in job_list:
       
        if i.id == int(job_id):
            temp_job_object = i

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

    def edit(object_to_edit, parameter):    
        if   parameter == "1":  # Customer
            n = input("""
            Add new value for CUSTOMER: """)
            object_to_edit.customer = n                                
                                                 
        elif parameter == "2":  # Product 
            n = input("""
            Add new value for PRODUCT: """)
            object_to_edit.product = n                                
                                                 
        elif parameter == "3" or parameter.lower() == "a":  # Amount
            n = input("""
            Add new value for AMOUNT: """)
            object_to_edit.amount = n                                
                                                 
        elif parameter == "4":  # Material
            n = input("""
            Add new value for MATERIAL: """)
            object_to_edit.material = n                                
                                                 
        elif parameter == "5":  # PrintSheetSize
            n = input("""
            Add new value for PrintSheetSize: """)
            object_to_edit.printing_sheet_size = n                                
                                                 
        elif parameter == "6" or parameter.lower() == "c":  # Comment
            n = input("""
            Add new value for COMMENT: """)
            object_to_edit.comment = n                                
                                                 
        elif parameter == "7" or parameter.lower() == "s":  # Status
            n = get_valid_input("Add new value for STATUS: (1=ReadyToPrint, 2=Waiting)", ("1","2"))
            # Muokataan statusta siten että jos input on 2, kysytään syytä mitä odottaa,
            # Jos input on 1, laitetaan statukseksi ready to print
            if n == "2":
                waiting_for_what = input("Waiting for what?: ")
                object_to_edit.status = "Waiting for: " + waiting_for_what 
            elif n == "1":
                object_to_edit.status = "Ready to Print"

        elif parameter == "8" or parameter.lower() == "p":  # Priority
            n = get_valid_input("""
            Add new value for PRIORITY (1=Extremely Urgent, 2=Very Urgent, 3=Urgent, 0=Normal priotiry) """, ("1", "2", "3", "0"))
            object_to_edit.priority = int(n)                               

    edit(temp_job_object, parameter)

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
