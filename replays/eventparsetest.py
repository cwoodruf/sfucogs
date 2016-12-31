#!/usr/bin/env python
"""
this script can be used to test the ouput of eventparse.py

each test case is encapsulated in a method that returns 
True = pass
False = fail

there are two classes of tests:
        1) tests that check single event records
        2) tests that check game parameters

Date: Sat Apr  9 16:49:11 2016
Author: Cal Woodruff cwoodruf@sfu.ca
Reviewed: Adam Bignell, August 19, 2016
Verified:
"""
import eventparse as ep
import gametests as gt
import bfldb
import testdb
import re
import sys
import traceback

verbose = False

def game_metadata(player, game):
        """
        grab the game metadata
        for whole game tests the game is 
        compared against this information
        """
        conn = testdb.dictconn()
        cur = conn.cursor()
        cur.execute("select * from whoisfiles where player=%s and game=%s limit 1", (player, game))
        metadata = cur.fetchone()
        cur.close()
        conn.close()
        return metadata

def read_game(table, game):
        """
        find all events for a specific game
        and return these as a list
        tests either accept a single element in the list
        or the whole list
        """
        conn = bfldb.dictconn()
        cur = conn.cursor()
        cur.execute("select * from {} where gameid=%s order by rowid".format(table), (game,))
        events = []
        for row in cur:
                events.append(row)
        cur.close()
        conn.close()
        return events

def get_games(player):
        """
        find all gameids from a given table
        assumes table is in format defined by 
        template_replaylevel
        """
        table = ep.get_table(player)
        conn = bfldb.conn()
        cur = conn.cursor()
        games = []
        cur.execute("select distinct gameid from {} order by gameid".format(table))
        for row in cur:
            games.append(row[0])
        cur.close()
        conn.close()
        return games

def passed(results):
        """
        check the results from test_game
        for "passed" - will fail if passed 
        does not exist in the results for a 
        given test
        """
        ok = True
        for test, data in results.iteritems():
                try:
                        if not data['passed']: 
                                ok = False
                                return ok
                except Exception as e:
                        sys.stderr.write("passed failed! test '{}' data '{}': {}\n".format(test, data, e))
                        ok = None
        return ok

def print_results(player, game, results):
        """
        print the raw results and indicated whether the game passed overall
        """
        print "player",player,"game",game,"results",results
        if passed(results):
                print "passed"
        else:
                print "failed"

def test_game(player, game, gametests=None, callback=None):
        """
        run a given set of tests for a specific game
        by default run a preset group of tests
        a test is an instance of GameTest
        """
        table = ep.get_table(player)
        metadata = game_metadata(player, game)
        events = read_game(table, game)
        if len(events) == 0:
                return {"error":"game {} not found for player {}".format(game, player)}
        results = {}

        if gametests == None:
                gametests = [
                        gt.MonotonicTest(), 
                        gt.LengthTest(), 
                        gt.CharacterTest(), 
                        gt.CoordsTest(), 
                        gt.EventsTest()
                ]

        for test in gametests:
                try:
                        test.run(metadata, events)
                        res = test.results()
                        results[test.name] = {'passed': res[0], 'data': res[1]}
                except Exception as e:
                        sys.stderr.write("test_game error for player {} game {}: {}\n".format(
                                player, game, e))
                        traceback.print_tb(sys.exc_traceback)

        if callback != None:
                callback(player, game, events, results)

        return results

def test_player(player, gametests=None, callback=None):
        """
        grab all games for a player by number
        then test them with the given tests
        by default aggregate results 
        if given a callback run callback using
        player, game and results as arguments
        """
        games = get_games(player)
        allresults = {}
        for game in games:
                results = test_game(player, game, gametests, callback)
                if callback == None:
                        if verbose: 
                                print_results(player, game, results)
                        allresults[game] = results
        if callback == None:
                return allresults

if __name__ == '__main__':
        # test code for testing single game or player
        verbose = gt.verbose = True
        if len(sys.argv) == 3:
                results = test_game(sys.argv[1], sys.argv[2])
                print_results(sys.argv[1],sys.argv[2],results)
        elif len(sys.argv) == 2:
                allresults = test_player(sys.argv[1])

                

