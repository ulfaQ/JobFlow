import pickle

class Files:
    """ Class for initial setting of pickle-formatted txt files (current job list and history) and setting their info-objects"""
    class Info:
        def __init__(self):
           self.current_id = 0

    def check_files():
        """ Called from jobflow.py check if current_job_list.txt exist, if not, create it. """
        
        try:
            with open("current_job_list.txt", "rb") as f:
                pass
        except:
            with open("current_job_list.txt", "wb") as f:
                pickle.dump([Files.Info()], f, protocol=4, fix_imports=False)
        # check if hist_log.txt exist, if not, create it.
        try:
            with open("hist_log.txt", "rb") as f:
                pass
        except: # Info object is in hist_log only to fill the first object. No other use
            with open("hist_log.txt", "wb") as f:
                pickle.dump([Files.Info()], f, protocol=4, fix_imports=False)
