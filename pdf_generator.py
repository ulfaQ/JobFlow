from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Rect
from reportlab.lib.colors import HexColor, black
from tools import Tools
import datetime
import os

class MakePDF:
    def __init__(self):
        self.line = 790
        self.c = None

    def make_report(self, input_list, input_header):

        # Check if output-directory exists. If not, create one
        if not os.path.exists("reports"):
            os.makedirs("reports")
        """ A function to make a pdf. Can be inputted eg a list returned from gimme_my_todo_list()"""

        # Define pdf-name with path to save output to.
        pdf_name = "Report_" + datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + ".pdf"
        save_name = os.path.join("reports/", pdf_name)

        # Create canvas
        self.c = canvas.Canvas(save_name)

        # Write header to canvas
        self.c.setFont("Helvetica-Bold", 17, leading=None)
        self.c.drawString(30, self.line, input_header + " " + datetime.datetime.now().strftime("%d.%m.%Y @ %H:%M"))
        self.line -= 30

        # Roll trough the list and write jobs to canvas with _generate_job_info function.
        for job in input_list:
            self._generate_job_info(job.customer, \
                    job.product, \
                    job.amount, \
                    job.material, \
                    job.printing_sheet_size, \
                    job.status, \
                    job.comment, \
                    job.addedDate, \
                    job.job_id, \
                    job.priority, \
                    ) 

        # Save the canvas after all jobs have been written
        self.c.save()

    def _generate_job_info(self, customer, \
                    product, \
                    amount, \
                    material, \
                    printing_sheet_size, \
                    status, \
                    comment, \
                    addedDate, \
                    job_id, \
                    priority, \
                    ): #Takes arguments from make_report()

        # Continue on the next page if there is too little space left in the current page.
        if self.line < 130:
            self.c.drawString(30, self.line - 15, "More jobs on the next page >>")
            self.line = 790
            self.c.showPage()

        #Draw a fucking rectangle
        color1 = HexColor("#DDDDCC")
        self.c.setFillColor(color1)
        self.c.rect(25,self.line - 2,550,12, fill=True, stroke=False) 

        # Write details of job on canvas in rectangle
        self.c.setFillColor(black)
        self.c.setFont("Helvetica-Bold", 11, leading=None)
        self.c.drawString(30, self.line, customer + " : " + product + " : " + addedDate)
        self.c.drawString(500, self.line, "PR {} : ID {}".format(priority, job_id))
        self.line -= 14

        # Writing rest of the info under rectangle
        self.c.setFont("Helvetica", 11, leading=None)
        self.c.drawString(30, self.line, "Amount: ")
        self.c.drawString(96, self.line, amount)
        self.line -= 12
        self.c.drawString(30, self.line, "Material: ")
        self.c.drawString(96, self.line, material)
        self.line -= 12
        self.c.drawString(30, self.line, "Sheet: ")
        self.c.drawString(96, self.line, printing_sheet_size)
        self.line -= 12
        self.c.drawString(30, self.line, "Status: ")
        self.c.drawString(96, self.line, status)
        self.line -= 12

        # Write Comment of job on separate lines on canvas
        comment_rows = Tools.rivitetty(comment, 70)
        self.c.drawString(30, self.line, "Comment: ")
        for i in comment_rows:
            self.c.drawString(96, self.line, i)
            self.line -= 12

        self.line -= 12
