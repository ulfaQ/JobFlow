# 1 Tee kopiot hist_log ja current_job_list tiedostoista kaiken varalle
# 2 Kopsaa tää jobflow kansioon
# 3 aja
# 4 korvaa vanhat uusilla
# 5 profit !

import pickle

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

old_list = None
with open("current_job_list.txt","rb") as f:
    old_list = pickle.load(f, fix_imports=False, encoding="ASCII", errors="strict")

old_hist = None
with open("hist_log.txt","rb") as f:
    old_hist = pickle.load(f, fix_imports=False, encoding="ASCII", errors="strict")

class Job:
    def __init__(self, prompted_info):
        self.prompted_info = prompted_info
        self.customer = prompted_info.get("customer")
        self.product = prompted_info.get("product")
        self.amount = prompted_info.get("amount")
        self.material = prompted_info.get("material")
        self.printing_sheet_size = prompted_info.get("printing_sheet_size")

        self._status = prompted_info.get("status")
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

# For current_job_list:

new_list = list()
for i in old_list[1:]:
    print(i.job_id)
    prompted_info = {

            "customer"             : i.customer,
            "product"              : i.product,
            "amount"               : i.amount,
            "material"             : i.material,
            "comment"              : i.comment,
            "printing_sheet_size"  : i.printing_sheet_size,
            "job_id"               : i.job_id,
            "addedDate"            : i.addedDate,
            "status"               : i.status,
            "priority"             : i.priority
            }

    new_list.append(Job(prompted_info))

with open("current_job_list_NEW.txt", "wb") as f:
    pickle.dump(new_list, f, protocol=4, fix_imports=False)

# For hist_log:

new_hist = list()
for i in old_hist[1:]:
    print(i.job_id)
    prompted_info = {

            "customer"             : i.customer,
            "product"              : i.product,
            "amount"               : i.amount,
            "material"             : i.material,
            "comment"              : i.comment,
            "printing_sheet_size"  : i.printing_sheet_size,
            "job_id"               : i.job_id,
            "addedDate"            : i.addedDate,
            "status"               : i.status,
            "priority"             : i.priority
            }

    new_hist.append(Job(prompted_info))

new_list.insert(0, old_list[0])

with open("hist_log_NEW.txt", "wb") as f:
    pickle.dump(new_list, f, protocol=4, fix_imports=False)
