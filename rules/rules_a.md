## Appendix 2: Seki
Consider the situation below:

<div class="reikai_board" data_board="/static/boards/board_10_1.json"></div>

This situation is called a seki. Neither player wants to play another move in this area. Let's see why.

Firstly, it is clear that Black does not want to play:

<div class="reikai_board" data_board="/static/boards/board_10_2.json"></div>

Adding another stone costs Black a liberty and White captures all the Black stones immediately.

However, what if white plays first?

<div class="reikai_board" data_board="/static/boards/board_10_3.json"></div>

Black captures the White stones and now wherever White plays Black can make a living shape:

<div class="reikai_board" data_board="/static/boards/board_10_4.json"></div>

Neither player wants to play again so this set of stones will remain until the end of the game (presuming the white stones on the outside live).

When counting territory, this seki situation scores no points for either side. No stones are taken off and the surrounded intersections are ignored.

Sekis occur infrequently but playing inside what your opponent thought was his territory and turning it into a seki can be a game winning move.
