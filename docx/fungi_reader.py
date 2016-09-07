# -*- coding: utf-8 -*-
from docx import Document
import csv
import pudb
import string

def find_nearest_bold_text(text, bold_texts, idx):
    bold_text = bold_texts[idx]
    if len(("").join(bold_text)) > 35:
        return bold_text
    else:
        return find_nearest_bold_text(text, bold_texts, idx - 1)


doc = Document('fungiconference2016.docx')

bold_texts = [[run.text for run in p.runs if run.bold] for p in doc.paragraphs]
paragraphs = doc.paragraphs

printable = set(string.printable)
emails_and_abstracts = []
for idx, paragraph in enumerate(paragraphs):
    if '@' in paragraph.text:
        # get email
        text = paragraph.text
        text_list = text.split(" ")
        for word in text_list:
            if '@' in word:
                email =  filter(lambda x: x in printable, word)
                if email.endswith('.'):
                    email = email[:-1]
                if email[0] == '.':
                    email = email[1:]
        bold_text = find_nearest_bold_text(text, bold_texts, idx)
        
        bold_text = "".join([my_str.encode('utf-8') for my_str in bold_text])
        bold_text = filter(lambda x: x in printable, bold_text)
        


        emails_and_abstracts.append((email, bold_text))


with open('mydata.csv', 'w') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile)
    for el in emails_and_abstracts:
        thedatawriter.writerow(el)


