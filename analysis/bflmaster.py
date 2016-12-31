"""
Defines the classes for the master table
uses separate classes for fields in that table
"""
from bflmasterfields import MasterFields
import time

class Master:
        """
        class that takes care of adding games to a master table
        """
        def __init__(self, controller):
                """
                controller uses an instance of this class
                to add a game to a master table
                the db member is the db module to use
                the db module should have a dictconn() function
                as the field processors need to find fields in a row based
                on the field name
                table refers to the master table to be updated
                """
                self.db = controller.db
                self.table = controller.tables['master']
                self.pacmeta = controller.pacmeta

        def add(self, game, start):
                """
                using the game metadata in game 
                generate all the field data for a game
                based on the data in a given events table
                and add it to the master table
                """

                self.start = start
                conn = self.db.dictconn()
                print "master elapsed",(time.time()-self.start)

                # do all our db processing here once
                events = game.events(conn)
                print "master elapsed",(time.time()-self.start)

                # this represents a set of objects that do all the data crunching
                fields = MasterFields(self.table, {'game':game, 'events':events, 'pacmeta':self.pacmeta})
                print "master elapsed",(time.time()-self.start)

                # check if the output table exists
                needstable = False
                createtb = conn.cursor()
                try:
                        createtb.execute("show tables like '{}'".format(self.table))
                        if createtb.rowcount == 0: needstable = True
                except:
                        pass
                if needstable: createtb.execute(fields.create_table())
                createtb.close()
                print "master elapsed",(time.time()-self.start)

                # create our save query
                query = fields.save_query()
                # then calculate all our stats
                data = fields.update_all()
                print "master elapsed",(time.time()-self.start)

                # save result to table
                save = conn.cursor()
                save.execute(query, data)
                conn.commit()
                # print query
                # print data
                print game
                print fields
                print "master elapsed",(time.time()-self.start)
                save.close()
                conn.close()
        
        
