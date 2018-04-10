import pickle
import auth

class Files:
    """ Class for initial setup of pickle-formatted txt-files 
        (current_job_list.txt and hist_log.txt) and setting 
        their info-objects
    """
    class Info:
        def __init__(self):
           self.current_id = 0

    def check_files():
        """ Called from jobflow.py check if current_job_list.txt exist, 
            if not, create it. 
        """
        try:
            with open("current_job_list.txt", "rb") as f:
                pass
        except FileNotFoundError:
            with open("current_job_list.txt", "wb") as f:
                pickle.dump([Files.Info()], f, protocol=4, fix_imports=False)

        # check if hist_log.txt exist, if not, create it.
        try:
            with open("hist_log.txt", "rb") as f:
                pass
        except FileNotFoundError: # Info object is in hist_log only to fill the first object. No other use
            with open("hist_log.txt", "wb") as f:
                pickle.dump([Files.Info()], f, protocol=4, fix_imports=False)

#       # Check if permissions.txt exists, if not, create it.
#       try:
#           with open("permissions.txt", "rb") as f:
#               pass
#       except FileNotFoundError:
#           authenticator = auth.Authenticator()
#           authorizor = auth.Authorizor(authenticator)
#           with open("permissions.txt", "wb") as f:
#               pickle.dump([authenticator, authorizor], f, protocol=4, fix_imports=False)
#
