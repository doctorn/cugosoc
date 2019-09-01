##A 9x9 Game
I will now give a more realistic example game and show you the conventional way of counting the score at the end.

<div class="reikai_board" data_board="/static/boards/board_6_1.json"></div>

<div class="reikai_board" data_board="/static/boards/board_6_2.json"></div>

<div class="reikai_board" data_board="/static/boards/board_6_3.json"></div>

Move 30: white passes; move 31: black passes. The game is now over. The result is that black has made territory on the left side of the board and white has made territory on the right side. The one black stone inside white's territory is dead. Notice that neither white nor black have actually made groups with 2 eyes. Instead, being experienced players they know that if the opponent tries to invade they can easily make 2 eyes. This is just as good. I will now describe the usual way of counting the score. This may seem unnecessarily complicated on a small board like this, but on a 19x19 board with lots of prisoners it is much easier.

Step 1: fill in the neutral points. There is 1 empty space between the black and the white groups that does not belong to either player. It does not matter who plays these points, but they should be filled in, e.g.:

<div class="reikai_board" data_board="/static/boards/board_6_4.json"></div>

Step 2: Removing the prisoners, i.e. pick up any of your opponent's dead stones that are inside your territory.

<div class="reikai_board" data_board="/static/boards/board_6_5.json"></div>

Step 3: Fill in territory with prisoners. Your opponent loses 1 point of territory for each prisoner you have captured. The usual way to do this is to use the prisoners you have captured to fill in your opponent's territory on the board, like this:

<div class="reikai_board" data_board="/static/boards/board_6_6.json"></div>

Step 4: Rearrange the territories. Just moving stones around within the territories does not change the score and can make it easier to count. For example:

<div class="reikai_board" data_board="/static/boards/board_6_7.json"></div>

Step 5: Count up. We now count and see that black has 26 points and white has 25 points. Black has won by 1 point.
