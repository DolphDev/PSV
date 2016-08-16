#Selections

##Creating Selections

Selections are mainly created by methods and operations.

Selections are created when the `Api` object does an operation that returns only a part of the csv document. 

They nearly identical to the `Api` object, except:

* They don't support outputting in any way (You can loop over them, or use the appropriate methods to change the output flag for the rows within the selection)
* Selections implement `__getattr__`  that allows Selections to use attributes like they are an `__getitem__` call. For example `selection.price` is equivalent to `selection["price"]`.
* `getcell` is not supported

Selections are meant to allow easy group interaction with a subgroup of the csv table.
    