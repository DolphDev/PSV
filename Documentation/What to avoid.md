#What to avoid and Gotachas.


##Implementation Details.

Rows are stored interally as a specialized `dict` that doesn't resemble a cell like structure. This allows very powerful interaction for some tasks, more traditional tasks (especially those you would find in excel) are only somewhat supported (This is a csv library, not an excel one).

This Library depends on mutablitity of rows, this allows most of the magic to happen with only moderate overhead. Messing with the internal operations will break the flow pretty quickly.

##Selection and Index Issues

Avoid code like this

    for row in api.rows:
        new_row = my_new_table.addrow(columns)
        new_row.market_share = row.market/sum(api["market"])

*This will recalculate the `sum` for all of the columns every loop*. This will be slow for even smaller spreadsheets. I suggest pre-calculating it, and referencing it instead of recalculating.

Selections have a similar caveat. 

    for row in api.rows:
        new_row = my_new_table.addrow(columns)
        new_row.market_share = row.market/sum(api.select(lambda x: x.available)["market"])

This will recreate the selection. This is very ineffienct for no reason. Only dynamically create selections when the selection is different every time. Doing the same selection over and over again will bog down your program for no reason. Instead precalculate the data (or if you want it to update while you loop through the table, the selection) and reference the result elsewhere in the program.



