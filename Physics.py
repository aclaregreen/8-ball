import phylib;
import sqlite3
import os
import math
################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;

# add more here
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH

SIM_RATE = phylib.PHYLIB_SIM_RATE
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON
DRAG = phylib.PHYLIB_DRAG
MAX_TIME = phylib.PHYLIB_MAX_TIME
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" id="table"/>""";
FOOTER = """</svg>\n""";

FRAME_INTERVAL = 0.01

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN"
    # "LIGHTYELLOW",
    # "LIGHTBLUE",
    # "PINK",             # no LIGHTRED
    # "MEDIUMPURPLE",     # no LIGHTPURPLE
    # "LIGHTSALMON",      # no LIGHTORANGE
    # "LIGHTGREEN",
    # "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here
    def svg(self):
        string = """ <circle cx="%d" cy="%d" r="%.1lf" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])
        if (self.obj.still_ball.number > 8):
            string += """<circle cx="%d" cy="%d" r="%.1lf" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS - 10, "GHOSTWHITE")
            string += """<circle cx="%d" cy="%d" r="%.1lf" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS - 20, BALL_COLOURS[self.obj.still_ball.number])
        return string

################################################################################
class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos, vel, acc ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = RollingBall;

    def svg(self):
        string =  """ <circle cx="%d" cy="%d" r="%lf" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])
        if (self.obj.rolling_ball.number > 8):
            string += """<circle cx="%d" cy="%d" r="%lf" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS - 10, "GHOSTWHITE")
            string += """<circle cx="%d" cy="%d" r="%lf" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS - 20, BALL_COLOURS[self.obj.rolling_ball.number])
        return string
##################################################################################
class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, pos ):
        """
        Constructor function. hole
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                        None, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = Hole;
    def svg (self):
        string = """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)
        return string
##########################################################################
class VCushion( phylib.phylib_object ):
    """
    Python vcushion class.
    """

    def __init__( self, x ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       None, 
                                       None, None, None, 
                                       x, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = VCushion;
    def svg(self):
        if self.obj.vcushion.x == 0.0:
            x_value = -25
        else:
            x_value = 1350
        string = """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (x_value)
        return string
#################################################################
class HCushion( phylib.phylib_object ):
    """
    Python hcushion class.
    """

    def __init__( self, y):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       None, 
                                       None, None, None, 
                                       0.0, y );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = HCushion;

    def svg(self):
        if self.obj.hcushion.y == 0.0:
            y_value = -25
        else:
            y_value = 2700
        string = """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (y_value)
        return string
############################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    def svg( self ):
        result = HEADER
        for i in range(MAX_OBJECTS):
            if self[i]:
                result+= self[i].svg()
        result += FOOTER
        return result
    
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                Coordinate( ball.obj.still_ball.pos.x,
                ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;

    def cueBall(self, table, velx, vely):
        for object in table:
            if object is not None and object.type == phylib.PHYLIB_STILL_BALL:
                if object.obj.still_ball.number == 0:
                    x = object.obj.still_ball.pos.x
                    y = object.obj.still_ball.pos.y
                    object.type = phylib.PHYLIB_ROLLING_BALL
                    object.obj.rolling_ball.pos.x = x
                    object.obj.rolling_ball.pos.y = y
                    object.obj.rolling_ball.number = 0
                    object.obj.rolling_ball.vel.x = velx
                    object.obj.rolling_ball.vel.y = vely
                    speed = math.sqrt((velx * velx) + (vely * vely))
                    if speed > VEL_EPSILON:
                        object.obj.rolling_ball.acc.x = velx / speed * DRAG * (-1)
                        object.obj.rolling_ball.acc.y = vely / speed * DRAG * (-1)
    def cueBallSearch(self):
        found = False
        for object in self:
            if object is not None and object.type == phylib.PHYLIB_STILL_BALL:
                if object.obj.still_ball.number == 0:
                    found = True
        if not found:
            pos = Coordinate( TABLE_WIDTH/2.0,
                                TABLE_LENGTH - TABLE_WIDTH/2.0 )
            sb  = StillBall( 0, pos )
            self += sb


class Database:
    def __init__(self, reset=False):
        if reset:
            if os.path.exists("phylib.db"):
                os.remove('phylib.db')
        self.conn = sqlite3.connect('phylib.db')
        self.cursor = self.conn.cursor()

    def createDB(self):
        self.cursor = self.conn.cursor()
        ball = """CREATE TABLE IF NOT EXISTS
        Ball(BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, BALLNO INTEGER NOT NULL,
        XPOS FLOAT NOT NULL, YPOS FLOAT NOT NULL, XVEL FLOAT, YVEL FLOAT)"""
        self.cursor.execute(ball)

        tTable = """CREATE TABLE IF NOT EXISTS
        TTable(TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, TIME FLOAT NOT NULL)"""
        self.cursor.execute(tTable)

        ballTable = """CREATE TABLE IF NOT EXISTS
        BallTable(BALLID INTEGER NOT NULL, TABLEID INTEGER NOT NULL,
        FOREIGN KEY (BALLID) REFERENCES Ball(BALLID),
        FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID))"""
        self.cursor.execute(ballTable)

        shot = """CREATE TABLE IF NOT EXISTS
        Shot(SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        PLAYERID INTEGER NOT NULL, GAMEID INTEGER NOT NULL,
        FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID),
        FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID))"""
        self.cursor.execute(shot)

        tableShot = """CREATE TABLE IF NOT EXISTS
        TableShot(TABLEID INTEGER NOT NULL, SHOTID INTEGER NOT NULL,
        FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID),
        FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID))"""
        self.cursor.execute(tableShot)

        game = """CREATE TABLE IF NOT EXISTS
        Game(GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        TABLEID INTEGER NOT NULL,
        GAMENAME VARCHAR(64) NOT NULL,
        FOREIGN KEY(TABLEID) REFERENCES TTable(TABLEID))"""
        self.cursor.execute(game)

        player = """CREATE TABLE IF NOT EXISTS
        Player(PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        GAMEID INTEGER NOT NULL, PLAYERNAME VARCHAR(64) NOT NULL,
        FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID))"""
        self.cursor.execute(player)

        self.cursor.close()
        self.conn.commit()
    
    def readTable(self, tableID):
        self.cursor = self.conn.cursor()
        table = Table()
        query = """SELECT * FROM (Ball INNER JOIN BallTable ON BallTable.BALLID=Ball.BALLID)
        WHERE BallTable.TABLEID = ?"""
        self.cursor.execute(query, (tableID+1,))
        balls = self.cursor.fetchall()
        if not balls:
            return None
        for ball in balls:
            if ball[4] == None and ball[5] == None:
                pos = Coordinate(ball[2], ball[3])
                sb = StillBall(ball[1], pos)
                table += sb
            else:
                pos = Coordinate(ball[2], ball[3])
                vel = Coordinate(ball[4], ball[5])
                speed = math.sqrt((vel.x * vel.x) + (vel.y * vel.y))
                acc = Coordinate(0,0)
                if speed > VEL_EPSILON:
                    acc.x = vel.x / speed * DRAG
                    acc.y = vel.y / speed * DRAG
                rb = RollingBall(ball[1], pos, vel, acc)
                table += rb
        query = """SELECT TIME FROM TTable WHERE TABLEID = ?"""
        self.cursor.execute(query, (tableID+1,))
        time = self.cursor.fetchone()
        time = time[0]
        table.time = time

        self.cursor.close()
        self.conn.commit()

        return table
    
    def writeTable(self, table):
        self.cursor = self.conn.cursor()
        query = """INSERT INTO TTable (TIME) VALUES (?)"""
        self.cursor.execute(query, (table.time,))
        table_id = self.cursor.lastrowid
        for object in table:
            if object:
                if object.type == phylib.PHYLIB_STILL_BALL:
                    query = """INSERT INTO Ball (BALLNO, XPOS, YPOS) VALUES (?, ?, ?)"""
                    ball_num = object.obj.still_ball.number
                    pos_x = object.obj.still_ball.pos.x
                    pos_y = object.obj.still_ball.pos.y
                    self.cursor.execute(query, (ball_num, pos_x, pos_y))
                    ball_id = self.cursor.lastrowid
                    query = """INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)"""
                    self.cursor.execute(query, (ball_id, table_id))
                elif object.type == phylib.PHYLIB_ROLLING_BALL:
                    query = """INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?)"""
                    ball_num = object.obj.rolling_ball.number
                    pos_x = object.obj.rolling_ball.pos.x
                    pos_y = object.obj.rolling_ball.pos.y
                    vel_x = object.obj.rolling_ball.vel.x
                    vel_y = object.obj.rolling_ball.vel.y
                    self.cursor.execute(query, (ball_num, pos_x, pos_y, vel_x, vel_y))
                    ball_id = self.cursor.lastrowid
                    query = """INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)"""
                    self.cursor.execute(query, (ball_id, table_id))
        self.cursor.close()
        self.conn.commit()
        return table_id - 1

    def close(self):
        self.conn.commit()
        self.conn.close()

    def getGame(self, id):
        self.cursor = self.conn.cursor()


        query = f"""SELECT PLAYERNAME, GAMENAME 
                FROM Player 
                INNER JOIN Game ON Game.GAMEID = Player.GAMEID
                WHERE Player.GAMEID = ?
                ORDER BY PLAYERID"""
        self.cursor.execute(query, (id,))


        #self.cursor.execute(query)
        game = self.cursor.fetchall()
        query = f"""SELECT TABLEID FROM Game WHERE GAMEID = {id}"""
        self.cursor.execute(query)
        tableId = int(self.cursor.fetchone()[0])
        self.cursor.close()
        self.conn.commit()
        return (game, tableId)
    def setGame(self, game, player1, player2, tableID):
        #figure out the game id still
        self.cursor = self.conn.cursor()
        query = """INSERT INTO Game (GAMENAME, TABLEID) VALUES (?, ?)"""
        self.cursor.execute(query, (game, tableID))
        id = self.cursor.lastrowid
        query = """INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)"""
        self.cursor.execute(query, (id, player1))
        self.cursor.execute(query, (id, player2))
        self.cursor.close()
        self.conn.commit()
        return id - 1
    def updateGame(self, gameId, tableId):
        self.cursor = self.conn.cursor()
        query = """UPDATE Game SET TABLEID = ? WHERE GAMEID = ?"""
        self.cursor.execute(query, (tableId, gameId))
        self.conn.commit()

    def newShot(self, playerName, game_id):
        self.cursor = self.conn.cursor()
        query = """SELECT PLAYERID, GAMEID FROM Player WHERE PLAYERNAME = ?"""
        self.cursor.execute(query, (playerName,))
        id = self.cursor.fetchall()
        player_id, game_id = id[0]
        query = """INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?,?)"""
        self.cursor.execute(query, (player_id, game_id))
        self.cursor.close()
        self.conn.commit()
        return self.cursor.lastrowid
    
    def addToTableShot(self, table_id, shot_id):
        self.cursor = self.conn.cursor()
        query = """INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)"""
        self.cursor.execute(query, (table_id, shot_id))
        self.cursor.close()
        self.conn.commit()

    def createTable(self):
        table = Table()

        pos = Coordinate( 
                TABLE_WIDTH / 2.0,
                TABLE_WIDTH / 2.0,
                );

        sb = StillBall( 1, pos );
        table += sb;

        # 5 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 - (BALL_DIAMETER+4.0)/2.0,
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)
                        );
        sb = StillBall( 5, pos );
        table += sb;

        # 11 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 + (BALL_DIAMETER+4.0)/2.0,
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)
                        );
        sb = StillBall( 11, pos );
        table += sb;

        #10 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 - (BALL_DIAMETER+4.0)/2.0 -
                        (BALL_DIAMETER+4.0)/2.0,
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)
                        );
        
        sb = StillBall( 10, pos );
        table += sb;

        #8 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0,
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)
                        );
        
        sb = StillBall( 8, pos );
        table += sb;

        #2 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 + (BALL_DIAMETER+4.0)/2.0 +
                        (BALL_DIAMETER+4.0)/2.0,
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)
                        );
        
        sb = StillBall( 2, pos );
        table += sb;

        #4 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 - (BALL_DIAMETER+4.0)/2.0 -
                        (BALL_DIAMETER+4.0)/2.0 - (BALL_DIAMETER+4.0)/2.0,
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)  -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)
                        );
        
        sb = StillBall( 4, pos );
        table += sb;

        #14 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 - (BALL_DIAMETER+4.0)/2.0,
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)  -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)
                        );
        
        sb = StillBall( 14, pos );
        table += sb;
        #7 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 + (BALL_DIAMETER+4.0)/2.0,
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)  -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)
                        );
        
        sb = StillBall( 7, pos );
        table += sb;
        #9 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 + (BALL_DIAMETER+4.0)/2.0 +
                        (BALL_DIAMETER+4.0)/2.0 + (BALL_DIAMETER+4.0)/2.0,
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)  -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)
                        );
        
        sb = StillBall( 9, pos );
        table += sb;
        #12 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 - (BALL_DIAMETER+4.0)/2.0 -
                        (BALL_DIAMETER+4.0)/2.0 - (BALL_DIAMETER+4.0)/2.0 -
                        (BALL_DIAMETER+4.0)/2.0,
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)
                        );
        
        sb = StillBall( 12, pos );
        table += sb;
        #3 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 - (BALL_DIAMETER+4.0)/2.0 -
                        (BALL_DIAMETER+4.0)/2.0,
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)
                        );
        
        sb = StillBall( 3, pos );
        table += sb;
        #13 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0,
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)
                        );
        
        sb = StillBall( 13, pos );
        table += sb;
        #15 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 + (BALL_DIAMETER+4.0)/2.0 +
                        (BALL_DIAMETER+4.0)/2.0,
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)
                        );
        
        sb = StillBall( 15, pos );
        table += sb;
        #6 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 + (BALL_DIAMETER+4.0)/2.0 +
                        (BALL_DIAMETER+4.0)/2.0 + (BALL_DIAMETER+4.0)/2.0 +
                        (BALL_DIAMETER+4.0)/2.0,
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) -
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)
                        );
        
        sb = StillBall( 6, pos );
        table += sb;
        # cue ball also still
        pos = Coordinate( TABLE_WIDTH/2.0,
                                TABLE_LENGTH - TABLE_WIDTH/2.0 );
        sb  = StillBall( 0, pos );

        table += sb;
        file = []
        f = open("table.svg", "w")
        f.write(table.svg())
        file.append("table.svg")
        f.close()
        return table

class Game:
    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        #work here
        self.database = Database()
        self.database.createDB();
        self.tableID = 0
        if (gameID is not None and gameName is None and player1Name is None and player2Name is None):
            self.gameID = gameID
            game, self.tableID = self.database.getGame(gameID + 1)
            self.player1Name, self.gameName = game[0]
            self.player2Name = game[1][0]
            f = open("table.svg", "w")
            f.write(self.database.readTable(self.tableID).svg())
            f.close()
            
        elif (gameID is None and gameName is not None and player1Name is not None and player2Name is not None):
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name
            table = self.database.createTable()
            self.tableID = self.database.writeTable(table)
            self.gameID = self.database.setGame(gameName, player1Name, player2Name, self.tableID)
        else:
            raise TypeError("Invlaid arguments")
        
    def shoot(self, gameName, playerName, table, xvel, yvel):
        #work here
        #shot_id = self.database.newShot(playerName, self.gameID)

        self.t = Table()

        self.t.cueBall(table, xvel, yvel)

        files  = []

        while (table):
            old = table
            table = Table.segment(table)
            if table is not None:
                length = table.time - old.time
                result = math.floor(length / FRAME_INTERVAL)
                for i in range(result):
                    new_table = old.roll(i * FRAME_INTERVAL)
                    new_table.time = old.time + (i * FRAME_INTERVAL)
                    files.append(new_table)
                    #table_id = self.database.writeTable(new_table)
                    #self.database.addToTableShot(table_id, shot_id)
        old.cueBallSearch()
            
        files.append(old)
        newTableId = self.database.writeTable(old)
        self.database.updateGame(self.gameID + 1, newTableId)
        return files
