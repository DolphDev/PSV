.. _apidoc:

Api Object
===================================

The API Object
--------------

This document goes over the API of this modules ``Api`` object.

For these examples, this table is used.

+-------------+---------+-------------+-------------------------+
| Name        | Price   | Available   | Company                 |
+=============+=========+=============+=========================+
| Product 1   | 10      | 1           | Yahoo                   |
+-------------+---------+-------------+-------------------------+
| Product 2   | 15      | 0           | Microsoft               |
+-------------+---------+-------------+-------------------------+
| Product 3   | 1       | 1           | Google                  |
+-------------+---------+-------------+-------------------------+
| Product 4   | 20      | 0           | Yahoo                   |
+-------------+---------+-------------+-------------------------+
| Product 5   | 25      | 1           | Yahoo                   |
+-------------+---------+-------------+-------------------------+
| Product 6   | 30      | 1           | Google                  |
+-------------+---------+-------------+-------------------------+
| Product 7   | 10      | 0           | Yahoo                   |
+-------------+---------+-------------+-------------------------+

Loading the CSV document
------------------------

This library includes in the ``load`` function, which takes care of
importing the csv document.

::

    import psv

    api = psv.load("filename", encoding="utf-8")
    columns = psv.column_names("filename", encoding="utf-8")

Interacting with the entire csv spreadsheet.
--------------------------------------------

To get the entire list companies (use ``set`` to get rid of repeats and
iterate over the generator)

::

    >>> set(api["Company"])
    {'Microsoft', 'Yahoo', 'Google'}

You can grab mulitple fields

::

    >>> list(api["Name", "Company"])
    [('Product 1', 'Yahoo'), ('Product 2', 'Microsoft'), ('Product 3', 'Google'), ('Product 4', 'Yahoo'), ('Product 5', 'Yahoo'), ('Product 6', 'Google'), ('Product 7', 'Yahoo')]

To grab entire row with this, use the string ``"ROW_OBJ"``

::

    >>> tuple(api["Name", "Company", "ROW_OBJ"])
    (('Product 1', 'Yahoo', <'BaseRow':4'>), ('Product 2', 'Microsoft', <'BaseRow':4'>), ('Product 3', 'Google', <'BaseRow':4'>), ('Product 4', 'Yahoo', <'BaseRow':4'>), ('Product 5', 'Yahoo', <'BaseRow':4'>), ('Product 6', 'Google', <'BaseRow':4'>), ('Product 7', 'Yahoo', <'BaseRow':4'>))

``Api`` also supports regular interger indexing

::

    >>> api[0]
    (('Product 1', 'Yahoo', <'BaseRow':4'>), ('Product 2', 'Microsoft', <'BaseRow':4'>), ('Product 3', 'Google', <'BaseRow':4'>), ('Product 4', 'Yahoo', <'BaseRow':4'>), ('Product 5', 'Yahoo', <'BaseRow':4'>), ('Product 6', 'Google', <'BaseRow':4'>), ('Product 7', 'Yahoo', <'BaseRow':4'>))

Api also supports mass setting of rows to output (or not output).

::

    >>> api.no_output()
    >>> api.enable(lambda x : x.company == "Yahoo")
    >>> api.lenoutput() #This method returns the lengh of all rows that will be outputed
    4

when outputed, the CSV document will look something like this.

+-------------+---------+-------------+-----------+
| Name        | Price   | Available   | Company   |
+=============+=========+=============+===========+
| Product 1   | 10      | 1           | Yahoo     |
+-------------+---------+-------------+-----------+
| Product 4   | 20      | 0           | Yahoo     |
+-------------+---------+-------------+-----------+
| Product 5   | 25      | 1           | Yahoo     |
+-------------+---------+-------------+-----------+
| Product 7   | 10      | 0           | Yahoo     |
+-------------+---------+-------------+-----------+

This code sets all rows to not output (``no_output`` method sets the
output flag to False for all rows it has access to.). The ``enable``