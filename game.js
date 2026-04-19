$(document).ready(function () {
  attachEventListeners();
  var numSolids = 0;
  var numStripes = 0;
  var colours = ["YELLOW", "BLUE", "RED", "PURPLE", "ORANGE", "GREEN", "BROWN"];
  setUpBallCount();
  var oldSolidCount = numSolids;
  var oldStripesCount = numStripes;
  var pTurn = 1;
  var namesArr = [];
  var name = $("#playerTurn").text();
  namesArr.push(name);
  name = $("#hidden").text();
  namesArr.push(name);
  var solids = 0;
  var stripes = 0;

  function attachEventListeners() {
    var ball = $("circle[fill='WHITE']");
    var svg = $("svg");
    var id = $("#variable_id").text();
    var x;
    var y;

    ball.on("mousedown touchstart", function (event) {
      if (event.type === "touchstart") event.preventDefault();
      var ballX = parseFloat(ball.attr("cx"));
      var ballY = parseFloat(ball.attr("cy"));

      var line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("x1", ballX);
      line.setAttribute("y1", ballY);
      line.setAttribute("x2", ballX);
      line.setAttribute("y2", ballY);
      line.setAttribute("stroke", "cornflowerblue");
      line.setAttribute("stroke-width", "10");

      // Append the line to the SVG container
      svg.append(line);

      // Update the line's end point as the mouse moves within the SVG container
      $(document).on("mousemove touchmove", function (event) {
        var touch = event.originalEvent.touches && event.originalEvent.touches[0];
        if (touch) { event.pageX = touch.pageX; event.pageY = touch.pageY; }
        var ballX = parseFloat($("circle[fill='WHITE']").attr("cx"));
        var ballY = parseFloat($("circle[fill='WHITE']").attr("cy"));

        var ballPx = $("circle[fill='WHITE']").offset().left;
        var ballPy = $("circle[fill='WHITE']").offset().top;

        var tablePageX = $("#table").offset().left;

        var r = ballX / (ballPx - tablePageX);
        x = (event.pageX - ballPx) * r + ballX;
        y = (event.pageY - ballPy) * r + ballY;

        var length = Math.sqrt(
          (x - ballX) * (x - ballX) + (y - ballY) * (y - ballY),
        );
        var minLength = 50;
        var maxLength = 200;
        if (length > maxLength) {
          var ratio = maxLength / length;
          x = ballX + (x - ballX) * ratio;
          y = ballY + (y - ballY) * ratio;
        } else if (length > 0 && length < minLength) {
          var ratio = minLength / length;
          x = ballX + (x - ballX) * ratio;
          y = ballY + (y - ballY) * ratio;
        }

        line.setAttribute("x2", x);
        line.setAttribute("y2", y);

        // Log the mouse coordinates for debugging
      });
      $(document).on("mouseup touchend", function (event) {
        var velx = (ballX - x) * 13;
        var vely = (ballY - y) * 13;
        shoot(velx, vely, id);

        line.remove();
        $(document).off("mousemove touchmove");
        $(document).off("mouseup touchend");
        //svg.empty();
      });
    });
  }

  function shoot(velx, vely, id) {
    $.post("shot", { velx: velx, vely: vely, id: id }, display);
  }

  function display(data, status) {
    var newTable = data.split(":,:");
    newTable.forEach(function (item, index) {
      setTimeout(
        function () {
          displayShot(item);
          if (index + 1 == newTable.length) {
            afterShot();
            attachEventListeners();
          }
        },
        10 * (index + 1),
      );
    });
  }
  function displayShot(frame) {
    $("#content").html(frame);
  }
  function setUpBallCount() {
    var balls = [];
    colours.forEach(function (item, index) {
      numBalls = $(`circle[fill='${item}']`).length;
      balls.push(numBalls);
      if (balls[index] == 3) {
        numSolids += 1;
        numStripes += 1;
      } else if (balls[index] == 2) {
        numStripes += 1;
      } else if (balls[index] == 1) {
        numSolids += 1;
      }
    });
    var eightBall = $("circle[r='28.5'][fill='BLACK']");
    if (eightBall.length == 0) {
      gameOver(pTurn);
    }
  }
  function afterShot() {
    oldSolidCount = numSolids;
    oldStripesCount = numStripes;
    numSolids = 0;
    numStripes = 0;
    setUpBallCount();
    if (oldSolidCount == 7 && oldStripesCount == 7) {
      if (numSolids < 7 || numStripes < 7) {
        if (numSolids < numStripes) {
          solids = pTurn;
          stripes = (pTurn % 2) + 1;
        } else {
          solids = (pTurn % 2) + 1;
          stripes = pTurn;
        }
      } else {
        pTurn = (pTurn % 2) + 1;
        switchPlayer();
      }
    }
    if (pTurn == solids) {
      if (oldSolidCount == numSolids) {
        pTurn = (pTurn % 2) + 1;
        switchPlayer();
      }
    } else if (pTurn == stripes) {
      if (oldStripesCount == numStripes) {
        pTurn = (pTurn % 2) + 1;
        switchPlayer();
      }
    }
    displayType();
  }
  function switchPlayer() {
    var playerTurn = $("#playerTurn").text();
    var hidden = $("#hidden").text();
    var temp = playerTurn;
    playerTurn = hidden;
    hidden = temp;
    $("#playerTurn").text(playerTurn);
    $("#hidden").text(hidden);
  }
  function displayType() {
    if (pTurn == solids) {
      $("#ballType").text("solids");
    } else if (pTurn == stripes) {
      $("#ballType").text("stripes");
    }
  }
  function gameOver(player) {
    var winner;
    if (player == solids && oldSolidCount == 0) {
      winner = pTurn;
    } else if (player == stripes && oldStripesCount == 0) {
      winner = pTurn;
    } else {
      winner = (pTurn % 2) + 1;
    }
    champ = namesArr[winner - 1];
    $("#winner").text(champ + " wins!!");
    // Store the text content of #winner
    var winnerText = $("#winner").text();

    // Store the back button element
    var backButton = $("#backButton").detach(); // Assuming your back button has an ID of "backButton"

    // Clear the entire body except for #winner and the back button
    $("body").children().not("#winner, #backButton").remove();

    // Set the text content of #winner back
    $("#winner").text(winnerText);

    // Append the back button back to the body
    $("body").append(backButton);

    return;
  }
});
