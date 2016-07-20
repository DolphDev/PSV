import csv

def outputfile(fileloc, rows, columnnames):
    with open(fileloc, 'w', encoding="LATIN-1", newline='') as csvfile:
        fieldnames = columnnames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for x in rows:
            writer.writerow(x.longcolumn)

