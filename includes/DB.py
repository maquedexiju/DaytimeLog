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

    def __init__(self,BASEPATH):
        self.db=TinyDB(BASEPATH+'db.json')

    def Save(self,data):
        Record=Query()
        date=None
        if not data:
            return
        for datum in data:
            if datum['day']!=date:
                date=datum['day']
                self.db.remove(Record.day==datum['day'])
            if datum['id']!='NULL':
                self.db.insert(datum)

    def SearchDate(self,date):
        Log=Query()
        return self.db.search(Log.day==date.strftime("%Y-%m-%d"))
