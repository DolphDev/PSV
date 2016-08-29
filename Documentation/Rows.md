# Rows

Rows are represented in the module via a heavly specialized `dict`. They do not necessary have same exact properties as an regular dictionary.


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

This module supports computed cells called "formulas". While formulas allow behavior similar to excel formulas (they are somewhat limited in this degree), formulas are more for leverage python code with your rows. 

Formulas are represented by functions that accept 1 argument and `**kwargs`. Formulas will not be ran until output or if referenced by other formulas.


    #Example Function
    def ex_formula(row, **kw):
        return row.sku + row.name + kw["id"]

    #Example Lambda
    lambda row, **kw: row.sku + row.name


The `row` argument will be supplied with the row this formula is on. This can be specified differently in the `.formula` method. This is simply a default for common usecases. If you wish to send more than 1 row to the function (or any other kind of data) use `**kwargs`. 

for row in api.rows:
    row.formula('name', ex_formula, id=1)

See the full documentation to see other features.. 

##Setting the output flag

All rows will be outputed by default. (Though the API object has methods to change this).

There are 3 operations to change the output flag as psv co-opts unary positive, negation, and inversion operations.

So to enable a row to output

    for row in api.rows:
        +row

To set a row to not output:

    for row in api.rows:
        -row

To flip a row to the opposite of current output flag 

    for row in api.rows:
        ~row

You also can set the property `outputrow` to a boolean to set the output flag.

    for row in api.rows:
        row.outputrow = True #Equivalent to +row
        row.outputrow = False #Equivalent to -row
        row.outputrow = not row.outputrow #Equivalent to ~row

##Deleted Rows

Deleted Rows are replaced by a `DeletedRow` object. 

These rows replace rows that have been deleted by the `del` keyword. They have no practical use, and are simply a lightweight way to keep track of deleted rows.

Deleting rows is generally not recommended. If you do use `del`, you should know that checking the rows `is_deleted` property is pratically required.

Deleted rows are only ignored when indexing by string/tuple and selections. If using any other method like accessing the rows through indexing (ie. `api[1]`) or iterating over the rows, DeletedRows will be present. If using the `getcell` family of methods, it will return a `DeletedRow` exception.

Also note that deleted rows are not hunted down in memory onced deleted. If you created a selection (Or did anything that would cause python to not actually delete the row in memory) with a not-yet but soon to be deleted row, it will still be present in your program. The `DeletedRow` object simply takes the place of the previous row in the list, which may or may not be the only place the row is refrenced. 

If you wish to make sure some rows do not output, it is much easier and preferable to use the outputflag mentioned elsewhere in this documentation.


##Other Methods and Features

###`.addcolumn(columnname, columndata="")`:
    
This method adds a column to the row. `columnname` should be the long version (For example "Name"); `columndata` is the what the column data will be. Its defaults to an empty string.

###`.longcolumn(columns=None)`

This method returns a dictionary with the original column names as the keys and the text in the columns as the values. This is mainly used in output, but may have some other usecases. If columns is None, all columns are returned.

