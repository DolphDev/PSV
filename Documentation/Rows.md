# Rows

Rows are represented in the module with a heavly specialized `dict`. They do not necessary have same exact properties as regular dictionaries.


##Accessing/Setting/Deleting columns

There are a few ways to access columns.

The first way is through attributes. Attributes are cruched downed versions of the column names. All letters are lower case, and spaces (or any character that breaks python syntax) are removed.

For this example, say this csv document had columns called `Name` and "SKU". `GetCompanyBySKU` is an example and not included in this module.

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



##Setting the output flag

All rows will be outputed by default. (Though the API object has method to change this).

There are 3 operations to change the status 

Fatstax-CSV co-opts unary positive, negation, and inversion.

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

