import csv

def outputfile(fileloc, rows, columnnames, quote_all=True, encoding="LATIN-1"):
    with open(fileloc, 'w', encoding=encoding, newline='') as csvfile:
        fieldnames = columnnames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL if quote_all else 0)

        writer.writeheader()
        for x in rows:
            writer.writerow(x.longcolumn)

