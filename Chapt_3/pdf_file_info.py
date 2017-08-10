#!/usr/bin/env python3
''' Retrieves Document information of the provided PDF and prints to the
screen.
'''
from pprint import pprint
import argparse
import PyPDF2

def get_pdf_props(pdf_fname):
    '''Returns a Dictionary containing PDF properties.
    '''
    try:
        pdf_reader = PyPDF2.pdf.PdfFileReader(pdf_fname)
        pdf_props = pdf_reader.getDocumentInfo()
    except FileNotFoundError:
        raise SystemExit('ERROR: File {} not found'.format(pdf_fname))
    except PyPDF2.utils.PdfReadError:
        raise SystemExit('''ERROR: File {} is either not a PDF file or it's 
              damaged'''.format(pdf_fname))
    return pdf_props

def main():
    parser = argparse.ArgumentParser(description='''Returns Document
                                     Properties of the provided PDF file.''')
    parser.add_argument('-f', '--file', help="""PDF file to retrieve properties
                        from.""", required=True)
    args = parser.parse_args()
    pdf_fname = args.file
    pdf_props = get_pdf_props(pdf_fname)
    pprint(pdf_props)

if __name__ == '__main__':
    main()
