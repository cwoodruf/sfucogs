"""

handle fields for master table

this module should not do any direct db processing
although it does make sql statements that can be used
by bflmaster to interact with a database table

specifically this module makes create and update statments
so the data it knows about can be stored externally to
a given output table

the bflfields family of modules can and should be
replaced depending on what is required 

change which fields show up in the output table 
by adding and removing modules from the bflfields/__init__.py 
__all__ list.

"""
import bflfields as fields
import bflfields.time as tm
import bflfields.filter as ft
from bflfields import *
from pacshift import PACShift

class MasterFields:
        """
        manages updating master table given what we know about fields
        """
        def __init__(self, table, data):
                """
                table is the output table for save_query
                inherit game metadata, PAC shifts and position data from table
                want to do those calculations only once per game
                """
                self.table = table
                self.game = data['game']
                self.events = data['events']
                self.filter = ft.instance()

                PAC = PACShift(data['pacmeta'].dispersion, data['pacmeta'].duration)
                PAC.generate_stats(self.events)
                self.PAC = PAC

                # many statistics require the use of time divided bins
                # since our concept of time is specific to our statistics
                # make the bins here and also get the game minutes
                self.minutes = tm.game_minutes(self.game)

                # for output table create db statement
                self.tablekeys = fields.keys()
                self.tableprops = fields.props()

                # one way to make instances of each field type
                # - not so simple in python -
                # these objects are then used to make table definitions
                # and calculate field data
                self.state = {}
                self.fields = []
                for fieldmod in fields.__all__:
                        self.fields.append((globals()[fieldmod]).instance(self))

        def update_all(self):
                """
                go through our list of fields and update each with data from 
                self.PAC and self.rows
                """
                data = []
                self.state = {}
                for c in self.fields:
                        data.append(c.set())
                        self.state[c.name] = c.value

                return tuple(data)

        def __str__(self):
                state = []
                i = 0
                for f in self.fields:
                        i += 1
                        state.append("{:4} {:64} {}".format(i, f.name, f.value))
                return "{} fields\nstate:\n{}".format(len(self.fields),"\n".join(state))

        def create_table(self):
                """
                returns the CREATE TABLE db statement
                for this group of fields
                """
                fieldstrs = []

                for c in self.fields:
                        fieldstrs.append("{} {}".format(c.name, c.datatype))

                stmt = "CREATE TABLE `{}` ({} {}) {}".format(
                        self.table,
                        ','.join(fieldstrs), 
                        self.tablekeys,
                        self.tableprops
                )
                return stmt

        def save_query(self):
                """
                build a row for the game identified in gamemeta
                then update table with this row data
                """
                fieldstrs = []
                placeholders = []
                for c in self.fields:
                        fieldstrs.append("{}".format(c.name))
                        placeholders.append('%s')
                return "replace into {} ({}) values ({})".format(
                        self.table, ','.join(fieldstrs), ','.join(placeholders))

