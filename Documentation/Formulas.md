#Formulas

This module supports a formula like system, which basically act as computed cells. Due to the way this module interally represents spreadsheet data, this should not be thought as an equivalent to excel's formulas. These act more like conventional python functions, with moderate support of refrencing other rows.

##Formula Object

All formulas are represented by the `Formula` object. This object is mainly used internally and doesn't have much usecases outside encapsulating functions.

##Row Objects

Row objects are where all interaction with formulas are done. 

###Creating Formulas

######Inherited Row objects should not overwrite `formula` method.

Formulas by default will have access to there current row, so in this example:

    row.formula("name", lambda r: r.fullname.split()[0])

`r` refers to the current row. This is possible to change.

    row.formula("name", lambda r: r.fullname.split()[0], OtherRow)

Now `r` will point to `OtherRow`.  If you want multiple rows (or simply any additional arguments) use **kwargs. 

    row.formula("name", lambda r, **kw: r.fullname.split()[0] + kw["sr"].name, sr=SecondRow)

At this point the formula is starting to get a little big, so it might be time to make it `def` function.

    def frml(row, **kwargs):
        return row.fullname.split()[0] + kwargs["sr"].name


    row.formula("name", frml, sr=SecondRow)


Formulas are allowed to access other formulas. If they want the result of that formula, it need to use a special to reurn result the computation result instead of the `Formula` object.
    
    row.formula("ExchangeRate", lambda r: GetExchangeRate())
    row.formula("name", lambda r: r.getformula("ExchangeRate")*r.price)

Make sure to advoid infinite recursion by creating a circular refrence.

