##The API Object

This document goes over the API of this modules `Api` object.

For these examples, this table is used.

| Name       | Price | Available | Company               |
|------------|-------|-----------|-----------------------|
| Product 1  | 10    | 1         | FatStax               |
| Product 2  | 15    | 0         | Red Funnel Consulting |
| Product 3  | 1     | 1         | Google                |
| Product 4  | 20    | 0         | FatStax               |
| Product 5  | 25    | 1         | FatStax               |
| Product 6  | 30    | 1         | Google                |
| Product 7  | 10    | 0         | FatStax               |


##Loading the CSV document

This library includes in the `load` function, which takes care of importing the csv document.
    
    import fatstax

    api = fatstax.load("filename", encoding="utf-8")
    columns = fatstax.column_names("filename", "utf-8")

##Interacting with the entire csv spreadsheet.
  
To get the entire list companies (use `set` to get rid of repeats and iterate over the generator)
    
    >>> set(api["Company"])
    {'Red Funnel Consulting', 'FatStax', 'Google'}

You can grab mulitple fields

    >>> list(api["Name", "Company"])
    [('Product 1', 'FatStax'), ('Product 2', 'Red Funnel Consulting'), ('Product 3', 'Google'), ('Product 4', 'FatStax'), ('Product 5', 'FatStax'), ('Product 6', 'Google'), ('Product 7', 'FatStax')]

To grab the row object with this, use the string `"ROW_OBJ"`

    >>> list(api["Name", "Company", "ROW_OBJ"])
    [('Product 1', 'FatStax', {'available': {'org_name': 'Available', 'value': '1'}, 'name': {'org_name': 'Name', 'value': 'Product 1'}, 'company': {'org_name': 'Company', 'value': 'FatStax'}, 'price': {'org_name': 'Price', 'value': '10'}}), ('Product 2', 'Red Funnel Consulting', {'available': {'org_name': 'Available', 'value': '0'}, 'name': {'org_name': 'Name', 'value': 'Product 2'}, 'company': {'org_name': 'Company', 'value': 'Red Funnel Consulting'}, 'price': {'org_name': 'Price', 'value': '15'}}), ('Product 3', 'Google', {'available': {'org_name': 'Available', 'value': '1'}, 'name': {'org_name': 'Name', 'value': 'Product 3'}........



`Api` also supports regular interger indexing

    >>> api[0]
    (('Product 1', 'FatStax', <'BaseRow':4'>), ('Product 2', 'Red Funnel Consulting', <'BaseRow':4'>), ('Product 3', 'Google', <'BaseRow':4'>), ('Product 4', 'FatStax', <'BaseRow':4'>), ('Product 5', 'FatStax', <'BaseRow':4'>), ('Product 6', 'Google', <'BaseRow':4'>), ('Product 7', 'FatStax', <'BaseRow':4'>))

Api also supports mass setting of rows to output (or not output).

    >>> api.flipoutput()
    >>> api[lambda x : x.company == "FatStax"]
    >>> api.lenoutput() #This method returns the lengh of all rows that will be outputed
    4

when outputed, the CSV document will look something like this.

| Name       | Price | Available | Company               |
|------------|-------|-----------|-----------------------|
| Product 1  | 10    | 1         | FatStax               |
| Product 4  | 20    | 0         | FatStax               |
| Product 5  | 25    | 1         | FatStax               |
| Product 7  | 10    | 0         | FatStax               |


This code sets all rows to not output (`flipoutput` simply changes the rows output setting to the opposite of its current value). The `Api` object will detect the lambda and use it. If the function returns True (or a Truthy value) it will set the row to output.

For the opposite effect you can do this

    >>> del api[0] #This deletes the first row, no special behavior.
    >>> del api[lambda x : x.company == "FatStax"]
    >>> len(api)
    6
    >>> api.lenoutput() 
    3

When outputted

| Name       | Price | Available | Company               |
|------------|-------|-----------|-----------------------|
| Product 2  | 15    | 0         | Red Funnel Consulting |
| Product 3  | 1     | 1         | Google                |
| Product 6  | 30    | 1         | Google                |


##Other Methods

###`.addrow(columns, cls=fatstax.BaseRow)`:
    
This method adds a row to the csv table. `columns` should be the output (or an `dict` that follows the pattern) of `csv.DictWriter`.

###`.outputedrows()`

Returns a generator of listed rows 

##Outputing

Use the `.output()` method on the `Api` object to export the `Api` object to a file.

    >>> columns = fatstax.column_names("Example.csv")
    >>> api.output("dataset-output/Example.csv", encoding="utf-8", columns=columns)
