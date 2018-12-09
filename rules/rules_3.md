##Liberties and Capturing
Once a stone has been put on the board it is never moved. It may, however, be removed by being captured. This is the subject of this section.

I would like you to look at this stone in the middle of the board:

<div class="reikai_board" data_board="/static/boards/board_3_1.json"></div>

You can see that there are 4 empty points next to it. It is said to have 4 'liberties'. If a stone is on the edge of the board like this:

<div class="reikai_board" data_board="/static/boards/board_3_2.json"></div>

 Then it only has 3 liberties. How many liberties does this stone have?

<div class="reikai_board" data_board="/static/boards/board_3_3.json"></div>

_(Answer: 2)_

If white plays next to a stone in the middle of the board like this:

<div class="reikai_board" data_board="/static/boards/board_3_4.json"></div>

 Then there are only 3 empty points next to it. It only has 3 liberties left. If black does not try to save his stone, and white keeps playing next to it like this:

<div class="reikai_board" data_board="/static/boards/board_3_5.json"></div>

Then eventually the white stone only has one liberty left. When a stone has only one liberty left it is said to be 'in atari'. (Atari is a Japanese word which doesn't really translate well.) If black continues to ignore his stone then with one more move white can remove its last liberty. At this point the black stone is captured. White removes it from the board and keeps it, usually in the lid of the pot his stones came in. The result of the capturing move looks like this:

<div class="reikai_board" data_board="/static/boards/board_3_6.json"></div>

 Question: how can a stone in the corner of the board be captured? 
 
 _(Answer: as illustrated)_

<div class="reikai_board" data_board="/static/boards/board_3_7.json"></div>
 
<div class="reikai_board" data_board="/static/boards/board_3_8.json"></div>

 When there are several black stones next to each other, connected by the lines of the board, then they form a group. Groups gets captured either all at once, or not at all. For example, black has 2 groups of stones here:

<div class="reikai_board" data_board="/static/boards/board_3_9.json"></div>

One group is made up of 5 stones, and the other is made up of 3 stones. How many liberties does each group have? (Answer: The 5 stone group has 10 liberties and the 3 stone group has 8 liberties.) If black does not intervene then white can capture the 3 stone group like this:

<div class="reikai_board" data_board="/static/boards/board_3_10.json"></div>

<div class="reikai_board" data_board="/static/boards/board_3_11.json"></div>

Of course black probably does not want to have his stones captured like this. After white plays his seventh attacking move (putting the black stones in atari) black could connect his stones together by playing here:

<div class="reikai_board" data_board="/static/boards/board_3_12.json"></div>

The black stones now form a single group with 10 liberties which will be difficult for white to capture.
