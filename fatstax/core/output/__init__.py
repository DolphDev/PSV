import csv

def outputfile(fileloc, rows, columnnames, quote_all=True, encoding="utf-8"):
    if not (isinstance(columnnames, list) or isinstance(columnnames, tuple)):
        raise ValueError("Provided Columns must be a list was {}".format(type(columnnames)))
    with open(fileloc, 'w', encoding=encoding, newline='') as csvfile:
        fieldnames = columnnames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL if quote_all else 0)
        writer.writeheader()
        for x in rows:
            if x.__hasformulas__:
                for formulaname in x.__formulas__:
                    x.setcolumn(formulaname, x.getcolumn(formulaname).call(x))
            if x.outputrow:
                writer.writerow(x.longcolumn)

