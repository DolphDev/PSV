#Formulas

This module supports a formula like system, which basically act as computed cells. Due to the way this module interally represents spreadsheet data, this should not be thought as an equivalent to excel's formulas. These act more like conventional python functions, with moderate support of refrencing other rows.

##Formula Object

All formulas are represented by the `Formula` object. This object is mainly used internally and doesn't have much usecases outside encapsulating functions.

##Row Objects

Row objects are where all interaction with formulas are done. 

###Creating Formulas

######Inherited Row objects should not overwrite `formula` method.

Formulas by default will have access to the current row, so in this example:

    row.formula("name", lambda r: r.fullname.split()[0])

`r` refers to the current row. This is possible to change.

    row.formula("name", lambda r: r.fullname.split()[0], OtherRow)

Now `r` will point to `OtherRow`.  If you want multiple rows (or any additional arguments) use `**kwargs`. 

    row.formula("name", lambda r, **kw: r.fullname.split()[0] + kw["sr"].name, sr=SecondRow)

Kwargs can also can be used to reference columns value before it was a formula (This avoids infinit recursion errors)

    row.formula("name", lambda r, **kw: kw["price"] * 2, price=row.price)

At this point the formula is starting to get a little big, so it might be time to make it `def` function.

    def frml(row, **kwargs):
        return row.fullname.split()[0] + kwargs["sr"].name


    row.formula("name", frml, sr=SecondRow)


Formulas are allowed to access other formulas. If they want the result of that formula, it need to use a special method to reurn result the computation result instead of the `Formula` object.
    
    row.formula("ExchangeRate", lambda r: GetExchangeRate())
    row.formula("name", lambda r: r.getformula("ExchangeRate")*r.price)

Make sure to advoid infinite recursion by creating a circular refrence in your formulas. As shown above, there is ways to refrence a value by using kwargs.

##Other Details and Gotchas

Using `str()` on a formula will return a `str` of the result. This is used mainly used for output. This can give the wrong impression when using `print` that a column isn't a formula. Use `repr` to check for formulas.


##Output

Row formulas are only computed when outputting, when refernced by an external row, or printed. 

