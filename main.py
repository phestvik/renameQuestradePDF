#from PyPDF2 import PdfFileReader
from pdfminer.high_level import extract_text
from pathlib import Path
from dateutil.parser import parse
import unicodedata
import re
from statistics import mode 

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

pdf_list = Path.cwd().glob('*.pdf')

count = 0
for pdf_file in pdf_list:
    if (pdf_file.is_file == True) and (count == 0):
        Print("There are no pdf files in the folder for processing")
    else:
        print(pdf_file.name)
        
        # This code is to get the year of the statement 
        pdf_text_utf = extract_text(pdf_file, page_numbers=[0])
        pdf_text = unicodedata.normalize("NFKD", pdf_text_utf)
        #year_re = re.findall(r"\b(20)\d{2}\b", pdf_text_utf) #this worked better in the browser application but not in python
        year_re = re.findall(r"\b[2]\d{3}\b", pdf_text)
        year = int(mode(year_re))

        if year < 2014:
            # Account Holder's First Name
            str = """USD \n\n"""
            i = pdf_text.find(str)+len(str)
            j = pdf_text.find(" ",i)
            acct_name = pdf_text[i:j]
            acct_name = re.sub("[^a-zA-Z]+", "", acct_name) #remove all the non alphabet characters          

            # Get remaining information form PDF page 1
            pdf_text_utf = extract_text(pdf_file, page_numbers=[1])
            pdf_text = unicodedata.normalize("NFKD", pdf_text_utf)

            # Account Number
            str = "Account"
            i = pdf_text.find(str)+len(str)
            j = pdf_text.find("""\n""",i)
            acct_no = pdf_text[i:j]
            acct_no = re.sub("[^0-9]", "", acct_no)

            # Statement Date
            str = "Period"
            i = pdf_text.find(str)+len(str)
            j = pdf_text.find("""\n""",i)
            acct_date = pdf_text[i:j]
            acct_date = re.sub("[^a-zA-Z]+", "", acct_date) #remove all the non alphabet characters

        else:
            # Account Holder's First Name
            str = """)\n\n"""
            i = find_nth(pdf_text, str, 2) +len(str)
            #i = pdf_text.find(str)+len(str)
            j = pdf_text.find(" ",i)
            acct_name = pdf_text[i:j]
            acct_name = re.sub("[^a-zA-Z]+", "", acct_name) #remove all the non alphabet characters 

            # Account Number
            str = "Account #"
            i = pdf_text.find(str)+len(str)
            j = pdf_text.find("""\n""",i)
            acct_no = pdf_text[i:j]
            acct_no = re.sub("[^0-9]", "", acct_no)

            # Statement Date
            str = "month:"
            i = pdf_text.find(str)+len(str)
            j = pdf_text.find("""\n""",i)
            acct_date = pdf_text[i:j]
            acct_date = re.sub("[^a-zA-Z]+", "", acct_date) #remove all the non alphabet characters

        if "TFSA".lower() in pdf_text.lower():
            acct_type = "TFSA"
        elif "RRSP".lower() in pdf_text.lower():
            acct_type = "RRSP"
        elif "RESP".lower() in pdf_text.lower():
            acct_type = "RESP"
        else:
            acct_type = "Margin"

        #Convert MMM to MM
        datetime = parse(acct_date)
        # if month isn't 01 or 02 (instead of 11), add a '0' to the newfilename
        if len("{}".format(datetime.month))<2:
            newfilename = "{}0{}_{}_{}_{}.pdf".format(datetime.year,datetime.month,acct_no,acct_type,acct_name)
        else:
            newfilename = "{}{}_{}_{}_{}.pdf".format(datetime.year,datetime.month,acct_no,acct_type,acct_name)
        
        pdf_file = Path(pdf_file)
        pdf_file.rename(newfilename)