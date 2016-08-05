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

`Api` also supports regular interger indexing
    >>> api[0]
    {'available': {'org_name': 'Available', 'value': '1'}, 'company': {'org_name': 'Company', 'value': 'FatStax'}, 'name': {'org_name': 'Name', 'value': 'Product 1'}, 'price': {'org_name': 'Price', 'value': '10'}}

Note that output is simply the current `repr` of row objects. Row objects do have some differences with regular dictionaries.

Api also supports mass setting of rows to output (or not output).

    >>> api.flipoutput()
    >>> api[lambda x : x.company == "FatStax"]

This code sets all rows to not output (Flip output simply changes the rows output setting to the opposite of its current value). The `Api` object will detect the lambda and use it. If the function returns True (or a Truthy value) it will set the row to output.

For the opposite effect you can do this

    >>> del api[0] #This deletes the first row, no special behavior
    >>> api[lambda x : x.company = "FatStax" and int(x.price)]