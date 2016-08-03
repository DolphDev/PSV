"""
This file contains rows that provide row objects commonly employed by FatStax
"""
import fatstax

class CloudStaxExportRow(fatstax.BaseRow):

    def _subdir(self, max_category):
        t = "Category {}"
        for x in range(max_category):
            try:
                resp = self.getcolumn(t.format(x+1))
                if resp:
                    yield resp
                else:
                    yield None
            except KeyError:
                yield None


    def category_dir(self, max_category):
        """Returns a list of the catagories in order"""
        return list(self._subdir(max_category))

        