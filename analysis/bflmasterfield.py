"""
base class for master table fields
"""
class MasterField(object):
        """
        template for fields in master table
        """
        def __init__(self, name, datatype, data):
                """
                events are raw events and PAC are Position Action Cycles based on movements
                """
                self.name = name
                self.datatype = datatype

                self.game = data.game
                self.events = data.events
                self.PAC = data.PAC
                self.minutes = data.minutes
                # filter allows us to share stats between fields, reducing work
                self.filter = data.filter

                self.value = None

        def set(self):
                """
                rewrites value for field based on calculation
                """
                self.value = self.calc()
                return self.value

        def calc(self):
                """
                does calculation/manipulation based on events or PAC
                returns the result without changing value
                every instance of MasterField should override this method
                output data is generally assumed to be a string
                as the purpose is to update a master table
                """
                return None

