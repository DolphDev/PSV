#Selections

##Creating Selections

Selections are created when the `Api` object does an operation that returns only a part of the csv document. 

They nearly identical to the `Api` object, except:

* They don't support outputting in any way (You can loop over them, or use the appropriate methods to change the output flag for the rows within the selection)
* It implement a `__getattr__` that allows it to use attributes like they are indexs. For example `selection.price` is equivalent to `selection["price"]

    