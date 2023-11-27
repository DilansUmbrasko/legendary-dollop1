import PyPDF2
import pathlib
import pandas as pd

data = []

adrese = pathlib.Path('3LD/invoices')
visi_faili = list(adrese.glob('*.pdf'))

for f in range(len(visi_faili)):
    row = []
    pdf_file = PyPDF2.PdfReader(open(visi_faili[f], 'rb'))
    number_of_pages = len(pdf_file.pages)
    page1 = pdf_file.pages[0]
    page2 = pdf_file.pages[1]

    text1 = page1.extract_text()
    text2 = page2.extract_text()

    pos1 = text1.find('Apmaksai:')
    pos2 = text1.find('Elektroenerģijas patēriņš kopā:')

    summa = text1[pos1 + 10:pos2].replace(',', '').rstrip()
    row.append(float(summa))

    pos3 = text1.find('Elektroenerģijas patēriņš kopā:')
    pos4 = text1.find('Veicot rēķina apmaksu')
    paterins = text1[pos3 + 32:pos4 - 4].replace(' ', '').replace(',', '').rstrip()
    row.append(float(paterins))

    cenaparkwh = 0.1157
    row.append(cenaparkwh)
    data.append(row)

for i, invoice_info in enumerate(data):
    rekina_izm = invoice_info[0]
    izmantota_energ = invoice_info[1]
    nordpool_tarifs = invoice_info[2]

    paradzemas_izm = izmantota_energ * nordpool_tarifs

    parmaksa = rekina_izm - paradzemas_izm

    print(f"rēķins {i + 1}:")
    print(f"īstā izmaksa: {rekina_izm}")
    print(f"paradzemās izmaksas: {paradzemas_izm}")
    print(f"pārmaksa: {parmaksa}")
    print()
