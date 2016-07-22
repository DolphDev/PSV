import csv

def outputfile(fileloc, rows, columnnames, quote_all=True):
    with open(fileloc, 'w', encoding="LATIN-1", newline='') as csvfile:
        fieldnames = columnnames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)

        writer.writeheader()
        for x in rows:
            writer.writerow(x.longcolumn)

