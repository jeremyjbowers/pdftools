#!/usr/bin/env python
import ftfy
import glob
import os

from flanker.addresslib import address


class Scrape(object):
    file_list = None

    def __init__(self):
        self.load_files()
        self.parse_files()

    def load_files(self):
        self.file_list = glob.glob('*.pdf')

    def parse_files(self):
        for pdf in self.file_list:
            s = StringPdf()
            s.parse_pdf_file(pdf)
            s.find_emails()
            s.write_results()


class StringPdf(object):
    pdf_as_string = None
    filename = None
    emails = []

    def parse_pdf_file(self, pdf):
        filename = pdf.split('.pdf')[0]
        self.filename = filename
        os.system('pdf2txt.py -o %s.txt %s' % (filename, pdf))
        with open('%s.txt' % filename, 'r') as readfile:
            self.pdf_as_string = readfile.read()

    def find_emails(self):
        for line in self.pdf_as_string.split('\n'):
            for string in line.split(' '):
                possible_email = address.parse_list(string.strip())
                if possible_email:
                    if possible_email != []:
                        if possible_email != "":
                            if u"@" in unicode(possible_email):
                                 self.emails.append('%s\t%s' % (pdf, possible_email))
        return self.emails

    def write_results(self):
        with open('%s.tsv' % self.filename, 'w') as writefile:
            writefile.write("\n".join(self.emails))

if __name__ == "__main__":
    scrape = Scrape()