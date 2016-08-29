##How to install 

In your terminal type:
    
    pip3 install git+https://github.com/RedFunnel/FatStax-CSV.git

If your usings a windows machine `pip3` may be simply `pip` depending on your setup.

You will be prompted for you github username/password or ssh key password.

##Usage:

To open the file yourself, it is best to use python's `with` statement. You also can use the libraries bundled file loader
    
    import psv
    import csv
    
    with open('dataset/example-dataset.csv', encoding="utf-8", newline='') as csvfile:
        rows = csv.DictReader(csvfile, delimiter=",")
        api = psv.Api(rows)

    api = psv.load(fatstax.load("dataset/example-dataset.csv", newline="", encoding="utf-8"))

This will put all of yours rows in memory.

FatStax object supports indexing:

    api[0] #First row
    api[::-1] #Rows in reverse order
    api[:5] # First five rows, all other list slicing is supported
    api["SKU"] #List of all the SKUs
    api[("SKU", "Name")] # tuple of specified fields



The `Api` object stores the rows in the `rows` attribute. These rows are represented by the `BaseRow` object.

You can loop over this attribute and interact with the rows. `BaseRow` allows you to simply type a condensed version of the column name to access it.
    
    for row in api.rows:
        print(row.sku) #psv supports getting column by column name
        print(row.getcolumn("SKU")) #To get the column by the original column name use .getcolumn()
        row.sku = row.sku + row.companyname #Can change column data 
        row.addcolumn("Brand", row.companyname) #You can add columns using the addcolumn method
        del row.brand #(You can delete rows by using the del keyword)
        if row.sku[:3] == "abc":
            -row #This tells the row to not output. Use +row to set a row to output (this is the default).
            # ~row is also supported. This applies the `not` keyword to the row output boolean.
            
            


When you are ready to output a dataset, you can use the `Api` object's `output` method. 

    api.output("dataset-output/Example-Output.csv", columns=columns, encoding="utf-8", quote_all=True)

Note the columns argument, this wrapper needs an ordered list of the columns to be outputed to the file (Depending on how you loaded the data in psv, it may be able to use the columns given to it during initialization). The easiest way to get current file's columns yourself is the `with` keyword.

    with open('dataset/example-dataset.csv', encoding="utf-8", newline='') as csvfile:
        columns = next(csv.reader(csvfile, delimiter=',', quotechar='|'))
        
    #psv includes a function for this.
    psv.column_names('dataset/example-dataset.csv')

You also can specifiy your own list if you want to intentionally add/remove columns. 

Note: if you use `addcolumn` make sure you add it to the list if you intend for it to be added to the output.



##Using BaseRow

BaseRow is a barebones row object, if you would want to use something more advanced (such as an object with computed attributes) you can inherit BaseRow.

    class SpecialRow(fatstax.BaseRow):

        #__init__ is used internally, if you want to simply setup attributes use constructs. 
        #Please note construct can only accept *args and **kwargs. 
        def construct(self, *args, **kwargs):
            self.exampleattribute = False

        #By using the @property python feature, you can add computed attributes.
        #These allow operations to be done with multiple columns at once
        @property
        def mastersku(self):
            return self.sku + " " + self.name


Specify this class when importing the data.

    with open('dataset/example-dataset.csv', encoding="utf-8", newline='') as csvfile:
        row = csv.DictReader(csvfile, delimiter=",")
        api = fatstax.FatStax(master, cls=SpecialRow)


Now when interacting with the rows you will have access to these properties and methods

    for row in api.rows:
        print(row.mastersku)
        print(row.exampleattribute)

