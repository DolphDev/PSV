#Selections

##Creating Selections

Selections are mainly created by methods and operations. They usau

Selections are created when the `Api` object does an operation that returns only a part of the csv document. 

Selections are nearly identical to the `Api` object (`Api` itself inherits `Selection` class), except:

* Selections don't support outputting in any way (You can loop over them, or use the appropriate methods to change the output flag for the rows within the selection)
* `getcell` and its family of methods are not supported

Selections are meant to allow easy group interaction with a subgroup of the csv table.




    
