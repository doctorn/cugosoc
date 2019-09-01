## Appendix 1: Ko
Consider the situation below:

<div class="reikai_board" data_board="/static/boards/board_9_1.json"></div>

The centre black stone is in atari. White captures with his next turn:

<div class="reikai_board" data_board="/static/boards/board_9_2.json"></div>

But now the stone White 1 is in atari himself. If Black were to recapture immediately then White do the same the same board position would repeat itself forever.

In go, the ko rule prevents this situation. It may be stated as

> _In a position where one stone has just been captured the player with the turn may not take back to immediately to repeat the same position._

Hence, Black may not immediately take White 1 above, instead he must play elsewhere on the board first. Black will typically play somewhere that White cannot ignore without taking an unacceptable loss of points.

<div class="reikai_board" data_board="/static/boards/board_9_3.json"></div>

_(Black 2 and White 3 elsewhere on the board)_

White will now play elsewhere on the board making an important move to which Black must in turn respond. If no such move important enough exists, Black may ignore White's move and connect, ending the ko:

<div class="reikai_board" data_board="/static/boards/board_9_4.json"></div>

_(White 5 elsewhere on the board)_

Kos play an extremely important part of the game of go and can be extremely complicated. Play where kos are taken and lost and threating moves are made elsewhere on the board are known as ko fights.
