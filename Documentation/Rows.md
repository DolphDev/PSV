# Rows

Rows are represented in the module via a heavly specialized `dict`. They do not necessary have same exact properties an regular dictionary.


##Accessing/Setting/Deleting columns

There are a few ways to access columns.

The first way is through attributes. Attributes are cruched downed versions of the column names. All letters are lower case, and spaces (or any character that breaks python syntax) are removed.

For this example, say this csv document had columns called `Name` and "SKU". 

######Note: `GetCompanyBySKU` is an example and not included in this module.

    for row in api.rows:
        print(row.name)
        #If you want to delete the column
        del row.name 
        #Note: This only sets the column to a empty string internally.
    
        #You also can set values
        #Since Delete only sets columns to a empty string, this is supported
        row.name = GetCompanyBySku(row.sku)

If you want to get a column by its original name, use `getcolumn` Method. `getcolumn` and its twins `setcolumn` and `delcolumn` accept both the original column name and the crunched down version.

    for row in api.rows:
        #Both short and original column names supproted
        print(row.getcolumn("Name"))
        print(row.getcolumn("name"))
    
        #If you want to delete the column
        row.delcolumn("Name")
        #Note: This only sets the column to a empty string internally.
    
        #You also can set values
        #Since Delete only sets columns to a empty string, this is supported
        row.setcolumn("Name", GetCompanyBySku(row.sku))

##Formulas

This module supports computed row columns called "formulas". Why formulas allow behavior similar to excel like formulas (Granted, they are somewhat limited in this degree), formulas are more for leverage outside python code with your rows. Formulas are represented by functions that accept 1 argument and kwargs. Formulas will not be ran until output. 



    #Example Function
    def ex_formula(row, *kw):
        return row.sku + row.name

The `row` argument, if not specified will be supplied with the row this formula is on. This can be specified differently in the `.formula` method. This is simply a default for common usecases. If you wish to send more than 1 row to the function (or any other kind of data) kwargs is supported. 

for row in api.rows:
    row.formula('name', lam) 

##Setting the output flag

All rows will be outputed by default. (Though the API object has methods to change this).

There are 3 operations to change the outout flag. 

There are 3 operations to change the outout flag as Fatstax-CSV co-opts unary positive, negation, and inversion operations.

So to enable a row to output

    for row in api.rows:
        +row

To set a row to not output:

    for row in api.rows:
        -row

To flip a row to the opposite of current output flag 

    for row in api.rows:
        -row

You also can set the property `outputrow` to a boolean to set the output flag.

    for row in api.rows:
        row.outputrow = True #Equivalent to +row
        row.outputrow = False #Equivalent to -row
        row.outputrow = not row.outputrow #Equivalent to ~row

##Other Methods and Features

###`.addcolumn(columnname, columndata="")`:
    
This method adds a column to the row. `columnname` should be the long version (For example "Name"); `columndata` is the what the column data will be. Its defaults to an empty string.

###`.longcolumn`

This computed attribute (property) returns a dictionary with the original column names as the keys and the text in the columns as the values. This is mainly used in output, but may have some other usecases.

