def get_valid_input(input_string, valid_options):
    """ Ottaa inputin ja kattoo onko se toisena argumenttina annetussa listassa (tuplea käytetään näissä tapauksisssa) 
    kysyy uudelleen niin kauan kunnes inputti on validi
    palauttaa annetun inputin kun se on validi"""

    input_string += " ({}) ".format(", ".join(valid_options))
    response = input(input_string)
    while response.lower() not in valid_options:
        response = input(input_string)
    return response

def EditJob(job_list, job_id):

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
                  Amount  (3)  {}
                Material  (4)  {}
          PrintSheetSize  (5)  {}
                 Comment  (6)  {}
                  Status  (7)  {}
                 Urgency  (8)  {}

Choose the Parameter to Edit: """.format(i.id, i.addedDate, i.customer, i.product, i.amount, i.material, \
                        i.printing_sheet_size, i.comment, i.status, i.urgency), ("1", "2", "3", "4", "5", "6", "7", "8"))
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
                                                 
        elif parameter == "3":  # Amount
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
                                                 
        elif parameter == "6":  # Comment
            n = input("""
            Add new value for COMMENT: """)
            object_to_edit.comment = n                                
                                                 
        elif parameter == "7":  # Status
            n = get_valid_input("Add new value for STATUS: (1=ReadyToPrint, 2=Waiting)", ("1","2"))
            # Muokataan statusta siten että jos input on 2, kysytään syytä mitä odottaa,
            # Jos input on 1, laitetaan statukseksi ready to print
            if n == "2":
                waiting_for_what = input("Waiting for what?: ")
                object_to_edit.status = "Waiting for: " + waiting_for_what 
            elif n == "1":
                object_to_edit.status = "Ready to Print"

        elif parameter == "8":  # Urgency
            n = get_valid_input("""
            Add new value for URGENCY (1=Extremely Urgent, 2=Very Urgent, 3=Urgent, 0=Normal) """, ("1", "2", "3", "0"))
            object_to_edit.urgency = int(n)                               

    edit(temp_job_object, parameter)

def gimme_my_todo_list(list_of_jobs):

    urgency1_jobs = []
    urgency2_jobs = []
    urgency3_jobs = []
    urgency0_jobs = []
    
    for i in list_of_jobs[1:]:
        if i.status == "Ready to Print":
            if int(i.urgency) == 1:
                urgency1_jobs.append(i)
            elif int(i.urgency) == 2:
                urgency2_jobs.append(i)
            elif int(i.urgency) == 3:
                urgency3_jobs.append(i)
            elif int(i.urgency) == 0:
                urgency0_jobs.append(i)

    temp_list = []
    temp_list.append(list_of_jobs[0])

    for i in urgency1_jobs:
        temp_list.append(i)
    for i in urgency2_jobs:
        temp_list.append(i)
    for i in urgency3_jobs:
        temp_list.append(i)
    for i in urgency0_jobs:
        temp_list.append(i)
    
    return temp_list
