'''
'id':child.id,\
'day':date1,\
'time':child.time.text,\
'duration':child.duration.text,\
'tag':tag,\
'job':job}
'''

from tinydb import TinyDB, Query
from tinydb.operations import increment, decrement

class DBDaytimeLog:
    db=None

    def __init__(self):
        self.db=TinyDB('includes/db.json')

    def Save(self,data):
        Record=Query()
        self.db.remove(Record.day==data[0]['day'])
        self.db.insert_multiple(data)

    def SearchDate(self,date):
        Log=Query()
        return self.db.search(Log.day==date.strftime("%Y%m%d"))
