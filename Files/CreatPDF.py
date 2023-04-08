# Created by Abhishek.A.Khatri

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.units import mm
from tkinter import filedialog, Tk


class GeneratePDF():
    """
    This class creates a pdf 
    of the current dataList of the bundle
    """

    def __init__(self, DBname, TbName, totalMarks, passingMarks, dataList) -> None:
        """
        The constructor can take all the inputs required to create a PDF of the given Bundle
        """
        dataList.insert(0, ['StudentID', 'Attendance', 'Examiner\n Marks',
                        'Moderator 1\n Marks', 'Moderator 2\n Marks', 'Final\n Marks'])

        # Create a PDF
        pdf_file = "my_pdf.pdf"
        pdf = SimpleDocTemplate(pdf_file, pagesize=letter)

        # Create a list of flowables (elements that can be added to a PDF)
        flowables = []

        # Add a title to the PDF
        title_style = getSampleStyleSheet()["Title"]
        flowables.append(Spacer(1, -20*mm))  # Add a spacer of 10 mm
        flowables.append(Paragraph(DBname, title_style))

        # Define the font size of the details paragraph
        details_font_size = 14

        # Create a new ParagraphStyle with the desired font size
        details_style = ParagraphStyle(
            name="Details",
            parent=getSampleStyleSheet()["Normal"],
            fontSize=details_font_size,
            splitLongWords=True,
        )

        # Add a spacer of 5 mm
        flowables.append(Spacer(5, 2.5*mm))

        # Add the details paragraph with the new style
        flowables.append(Paragraph(TbName, details_style))
        flowables.append(Spacer(1, 2.5*mm))
        flowables.append(Paragraph("Total Marks: "+totalMarks+", Passing Marks: " +
                         passingMarks, details_style))
        flowables.append(Spacer(1, 2.5*mm))

        # Add a table to the PDF
        table = Table(dataList)
        # Create a table style
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 13),  # font size of heading row
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TEXTCOLOR', (-1, 1), (-1, -1), colors.blue),
            ('ALIGN', (-1, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),  # font size of dataList rows
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 14),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
        ])

        # Loop through the dataList rows and change the text color based on the last column value
        for i in range(1, len(dataList)):
            if dataList[i][-1] != "-" and (dataList[i][-1] == "AB" or float(dataList[i][-1]) < float(passingMarks)):
                table_style.add('TEXTCOLOR', (-1, i), (-1, i), colors.red)
            else:
                table_style.add('TEXTCOLOR', (-1, i), (-1, i), colors.blue)

        # Create the table and set the style
        table = Table(dataList)
        table.setStyle(table_style)

        # Add the table to the flowables list
        flowables.append(table)

        # Add watermark to every page

        class Watermark:
            def __init__(self, text):
                self.text = text

            def __call__(self, canvas, doc):
                canvas.saveState()
                canvas.setFont('Helvetica', 200)
                canvas.setFillGray(0.8)
                canvas.rotate(45)
                canvas.drawCentredString(7.0*inch, 0*inch, self.text)
                canvas.restoreState()

        watermark = Watermark("MGMU")

        root = Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        
        # Check if the file is created or the process is been cancelled
        if file_path == ():
            raise Exception("PDF creation cancelled")
        
        # else creating a pdf of the below properties
        else:
            pdf_file = file_path
            pdf = SimpleDocTemplate(
                pdf_file, pagesize=letter, title="MarkSheet")
            pdf.build(flowables, onFirstPage=watermark, onLaterPages=watermark)


# data = [['TotalMarks:100', '-', '-', '-', '-', '-'],
#         ['2023B1', 'P', '40', '3', '-', '50.235'],
#         ['2023B2', 'AB', '-', '-', '-', 'AB'],
#         ['2023B3', 'AB', '-', '-', '-', 'AB'],
#         ['2023B4', 'P', '-', '-', '-', '-'],
#         ['2023B5', 'P', '-', '-', '-', '-'],
#         ['2023B6', 'P', '-', '-', '-', '-'],
#         ['2023B7', 'P', '-', '-', '-', '-'],
#         ['2023B8', 'P', '-', '-', '-', '-'],
#         ['2023B9', 'P', '-', '-', '-', '-'],
#         ['2023B10', 'P', '-', '-', '-', '-']]
# g1 = GeneratePDF("tb", "db", "60", "24", data)
