##How to install 

In your terminal type:
    
    pip3 install git+https://github.com/RedFunnel/FatStax-CSV.git

If your usings a windows machine `pip3` may be simply `pip` depending on your setup.

You will be prompted for you github username/password or ssh key password.

##Usage:

To open the file, it is best to use python's `with` statement
    
    import fatstax
    
    with open('dataset/example-dataset.csv', encoding="utf-8", newline='') as csvfile:
        rows = csv.DictReader(csvfile, delimiter=",")
        api = fatstax.FatStax(rows)

This will put all of yours rows in memory.

The `FatStax` object stores the rows in the `rows` attribute. These rows are represented by the `BaseRow` object.

You can loop over this attribute and interact with the rows. `BaseRow` allows you to simply type a condensed version of the column name to access it.

for row in api.rows:
    print(row.sku) #Supports getting column by column name
    row.sku = row.sku + row.companyname #Can change column data
    row.addcolumn("Brand", row.companyname) #You can add columns using the addcolumn method


When you are ready to output a dataset, you can use the `FatStax` object's `output` method. 

    api.output("dataset-output/Example-Output.csv", columns=columns, encoding="utf-8", quote_all=True)

Note the columns argument, this wrapper needs an ordered list of the columns to be outputed to the file. The easiest way to get current file's columns is the `with` keyword.

    with open('dataset/example-dataset.csv', encoding="utf-8", newline='') as csvfile:
        columns = next(csv.reader(csvfile, delimiter=',', quotechar='|'))

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


Specify this class it importing the data.

    with open('dataset/example-dataset.csv', encoding="utf-8", newline='') as csvfile:
        row = csv.DictReader(csvfile, delimiter=",")
        api = fatstax.FatStax(master, cls=SpecialRow)


Now when interacting with the rows you will have access to these properties and methods

    for row in api.rows:
        print(row.mastersku)
        print(row.exampleattribute)

