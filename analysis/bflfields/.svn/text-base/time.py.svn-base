"""
Some convenience stuff for time conversion
"""
from decimal import Decimal
TSRTsecond = Decimal(88.5347)
TSRTminute = Decimal(TSRTsecond*Decimal(60.0))

def ts2seconds(ts):
        """
        convert timestamps to seconds
        """
        return float(Decimal(ts)/TSRTsecond)

def ts2minutes(ts):
        """
        convert timestamps to minutes
        """
        return float(Decimal(ts)/TSRTminute)

def game_lasttick(game):
        """
        returns game_lasttick as a float
        """
        return Decimal(game.filemeta['game_lasttick'])

def game_seconds(game):
        """
        game seconds based on data for this field
        """
        seconds = ts2seconds(game_lasttick(game))
        return seconds

def game_minutes(game):
        """
        look at last row and convert timestamp to minutes
        """
        minutes = ts2minutes(game_lasttick(game))
        return minutes

