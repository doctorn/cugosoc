// reikai.js
// License GPL v2.0

var boxSize = 25;

function render(board, data) {
  board.innerHTML = "";

  if (data.size != 9 && data.size != 13 && data.size != 19)
    throw "Only 9x9, 13x13 and 19x19 boards are permitted";

  var canvas = document.createElement("canvas");
  var gridWidth = Math.min((data.end.x - data.start.x) + 1, data.size);
  var gridHeight = Math.min((data.end.y - data.start.y) + 1, data.size);

  canvas.setAttribute("width", (gridWidth * boxSize) + "px");
  canvas.setAttribute("height", (gridHeight * boxSize) + "px");
  canvas.style["box-shadow"] = "0px 2px 2px 0px rgba(0, 0, 0, 0.1)";

  board.style.width = (gridWidth * boxSize) + "px";
  board.style.height = (gridHeight * boxSize) + "px";
  board.appendChild(canvas);
  var ctx = canvas.getContext("2d");

  ctx.fillStyle = "#DEB887";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "#000000";
  ctx.font = "bold " + (boxSize / 2) + "px Arial";
  ctx.lineWidth = 1;
  ctx.translate(-boxSize * data.start.x, -boxSize * data.start.y);

  for (var i = 0; i < data.size; i++) {
    ctx.moveTo((boxSize / 2), (boxSize / 2) + boxSize * i);
    ctx.lineTo(boxSize * data.size - (boxSize / 2),
               (boxSize / 2) + boxSize * i);
    ctx.stroke();
    ctx.moveTo((boxSize / 2) + boxSize * i, (boxSize / 2));
    ctx.lineTo((boxSize / 2) + boxSize * i,
               boxSize * data.size - (boxSize / 2));
    ctx.stroke();
  }

  var offset = 4;
  if (data.size === 9)
    offset = 2;
  else if (data.size == 13)
    offset = 3;

  var midways = false;
  if (data.size == 19)
    midways = true;

  ctx.beginPath();
  ctx.arc((boxSize / 2) + offset * boxSize, (boxSize / 2) + offset * boxSize, 3,
          0, 2 * Math.PI);
  ctx.fill();
  ctx.beginPath();
  ctx.arc(boxSize * (data.size - offset) - (boxSize / 2),
          (boxSize / 2) + offset * boxSize, 3, 0, 2 * Math.PI);
  ctx.fill();
  ctx.beginPath();
  ctx.arc(boxSize * (data.size - offset) - (boxSize / 2),
          boxSize * (data.size - offset) - (boxSize / 2), 3, 0, 2 * Math.PI);
  ctx.fill();
  ctx.beginPath();
  ctx.arc((boxSize / 2) + offset * boxSize,
          boxSize * (data.size - offset) - (boxSize / 2), 3, 0, 2 * Math.PI);
  ctx.fill();

  if (midways) {
    ctx.beginPath();
    ctx.arc((boxSize / 2) * data.size, (boxSize / 2) + offset * boxSize, 3, 0,
            2 * Math.PI);
    ctx.fill();
    ctx.beginPath();
    ctx.arc((boxSize / 2) * data.size,
            boxSize * (data.size - offset) - (boxSize / 2), 3, 0, 2 * Math.PI);
    ctx.fill();
    ctx.beginPath();
    ctx.arc((boxSize / 2) + offset * boxSize, (boxSize / 2) * data.size, 3, 0,
            2 * Math.PI);
    ctx.fill();
    ctx.beginPath();
    ctx.arc(boxSize * (data.size - offset) - (boxSize / 2),
            (boxSize / 2) * data.size, 3, 0, 2 * Math.PI);
    ctx.fill();
  }

  ctx.beginPath();
  ctx.arc(data.size * (boxSize / 2), data.size * (boxSize / 2), 3, 0,
          2 * Math.PI);
  ctx.fill();

  ctx.shadowBlur = 1;
  ctx.shadowColor = "#000000";
  for (var stone of data.stones) {
    ctx.beginPath();
    ctx.arc((boxSize / 2) + boxSize * stone.x,
            (boxSize / 2) + boxSize * stone.y, boxSize / 2 - 2, 0, 2 * Math.PI);
    if (stone.black)
      ctx.fillStyle = "#000000";
    else
      ctx.fillStyle = "#FFFFFF";
    ctx.fill();
  }

  ctx.shadowBlur = 0;
  for (var stone of data.stones) {
    if (stone.label !== undefined) {
      if (stone.black)
        ctx.fillStyle = "#FFFFFF";
      else
        ctx.fillStyle = "#000000";
      ctx.textAlign = "center";
      ctx.fillText(stone.label, (boxSize / 2) + stone.x * boxSize,
                   (2 * boxSize / 3) + stone.y * boxSize);
    }
  }
}

function init() {
  for (var board of document.querySelectorAll(".reikai_board")) {
    var boardJSON = board.getAttribute("data_board");
    var boardData = {
      size : 19,
      start : {x : 0, y : 0},
      end : {x : 18, y : 18},
      stones : []
    };
    if (boardJSON !== null) {
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        boardData = JSON.parse(this.responseText);
        render(board, boardData);
      };
      xhttp.open("GET", boardJSON, false);
      xhttp.setRequestHeader("Content-type", "application/json");
      xhttp.send();
    } else
      render(board, boardData);
  }
}

var reikai = {init : init, render : render};
