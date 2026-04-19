import sys; # used to get argv
 # used to parse Mutlipart FormData 
            # this should be replace with multipart in the future
import Physics
import math
import os
import random

# web server parts
from http.server import HTTPServer, BaseHTTPRequestHandler;

# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qsl;


# handler for our web-server - handles both GET and POST requests
class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        # check if the web-pages matches the list
        if parsed.path in [ '/', '/shoot.html' ]:

            # retreive the HTML file
            fp = open( './shoot.html' if parsed.path == '/' else '.'+self.path );
            content = fp.read();

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();

        # check if the web-pages matches the list
        elif parsed.path.startswith("/table") and parsed.path.endswith(".svg"):
            # this one is different because its an image file
            # retreive the HTML file (binary, not text file)
            try:
                with open(parsed.path[1:]) as file:
                    content = file.read()
                    self.send_response( 200 ); # OK
                        # notice the change in Content-type
                    self.send_header( "Content-type", "image/svg+xml" );
                    self.send_header( "Content-length", len( content ) );
                    self.end_headers();
                    self.wfile.write(bytes(content, "utf-8"))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")

        elif parsed.path in ["/display.css", "/shoot.css"]:
            fp = open("."+ self.path)
            content = fp.read()
            self.send_response(200)
            self.send_header( "Content-type", "text/css" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();
            self.wfile.write(bytes(content, "utf-8"))
            fp.close()
        else:
            # generate 404 for GET requests that aren't the 3 files above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );


    def do_POST(self):
        # hanle post request
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        if parsed.path in [ '/display.html' ]:
            #receive data
            content_len = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_len).decode('utf-8')
            form_data = dict(parse_qsl(post_data))

            player1 = form_data.get("player1", None)
            player2 = form_data.get("player2", None)
            gameName = form_data.get("gameName", None)
            gameId = form_data.get("gameId", None)
            if (gameId is not None):
                gameId = int(gameId)

            if gameId is not None:
                try:
                    game = Physics.Game(gameId)
                except (TypeError, Exception):
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(b"""<!DOCTYPE html>
<html>
<head>
  <title>Game Not Found</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #0f0f0f;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #ffffff;
    }
    .card {
      background: #1a1a1a;
      border: 1px solid #2e2e2e;
      border-radius: 16px;
      padding: 2rem;
      width: 100%;
      max-width: 460px;
      text-align: center;
    }
    h1 { font-size: 28px; font-weight: 500; margin-bottom: 0.75rem; }
    p { color: #888888; font-size: 14px; margin-bottom: 1.5rem; }
    a {
      display: inline-block;
      height: 40px;
      line-height: 40px;
      padding: 0 24px;
      border-radius: 8px;
      border: 1px solid #3a3a3a;
      background: transparent;
      color: #ffffff;
      font-size: 14px;
      text-decoration: none;
      transition: background 0.15s;
    }
    a:hover { background: #2e2e2e; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Game not found</h1>
    <p>No game exists with that ID.</p>
    <a href="shoot.html">Back</a>
  </div>
</body>
</html>""")
                    return

            else:
                game = Physics.Game(None, gameName, player1, player2)
            id = game.gameID
            player1 = game.player1Name
            player2 = game.player2Name
            gameName = game.gameName
            randInt = random.randint(1, 2)
            if (randInt == 1):
                playerTurn = player1
                hidden = player2
            else:
                playerTurn = player2
                hidden = player1
            winner = ""
            ballType = ""

            for filename in os.listdir("."):
                if filename.startswith("table-") and filename.endswith(".svg"):
                    os.remove(filename)

            # Read the content of the SVG file
            with open("table.svg", "r") as svg_file:
                svg_content = svg_file.read()
                
            # Open the HTML file in write mode
            with open("display.html", "w") as fptr:
                # Write the HTML content
                fptr.write("<html>\n")
                fptr.write("<head>\n")
                fptr.write("<title>Shoot HTML</title>\n")
                fptr.write("<link rel='stylesheet' type='text/css' href='display.css'>")
                fptr.write("<script src='https://code.jquery.com/jquery-3.6.0.min.js'></script>")
                fptr.write("</head>\n")
                fptr.write("<body>\n")
                fptr.write("<h1>8 Ball</h1>\n")
                fptr.write("<span id='playerTurn'>{}</span>\n".format(playerTurn))
                fptr.write("<span id='ballType'>{}</span>\n".format(ballType))
                fptr.write("<span id='winner'>{}</span>\n".format(winner))
                fptr.write("<span id='hidden' style='display: none;'>{}</span>\n".format(hidden))
                fptr.write("<span>Game Id: </span>" + "<span id='variable_id'>{}</span><br>\n".format(id))
                fptr.write("<a href='shoot.html' id='backButton'>BACK</a>\n")
                fptr.write("<div id='content'>")
                fptr.write(svg_content)
                fptr.write("</svg>\n")
                fptr.write("</div>")
                # Include JavaScript code
                fptr.write("<script>\n")
                with open("game.js", "r") as js_file:
                    fptr.write(js_file.read())
                fptr.write("</script>\n")

                # Close the body and html tags
                fptr.write("</body>\n")
                fptr.write("</html>\n")

            with open("display.html", "r") as fptr:
                content = fptr.read()

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the browser
            self.wfile.write( bytes( content, "utf-8" ) );
        elif parsed.path == '/shot':

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = dict(parse_qsl(post_data))

            # Retrieve 'velx' and 'vely' from form data
            velx = float (form_data.get('velx'))
            vely = float (form_data.get('vely'))

            id = int (form_data.get('id'))

            game = Physics.Game(id)
            table = game.database.readTable(game.tableID)

            # Process the playerTurn value as needed
            
            files = game.shoot(game.gameName, game.player1Name, table, velx, vely)
            for i in range(len(files)):
                string = files[i].svg()
                files[i] = string
            content = ":,:".join(files)
            # Send the updated content as the response
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()
            self.wfile.write(bytes(content, "utf-8"))

        else:
            # generate 404 for POST requests that aren't the file above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );


if __name__ == "__main__":
    port = int(os.environ.get("PORT", sys.argv[1] if len(sys.argv) > 1 else 8080))
    httpd = HTTPServer( ( '0.0.0.0', port ), MyHandler );
    print( "Server listing in port:  ", port );
    print (f"http://localhost:{port}/shoot.html")
    httpd.serve_forever();
