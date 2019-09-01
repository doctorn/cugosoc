##Territory and the End Game
I seem to have been babbling on for hours but I have not yet told you what the aim of the game is. Well, I'll tell you. The aim of the game is to make territory.

So, what is territory? You are used to the idea that groups of stones with 2 eyes can never be captured. Well, you get 1 point of territory for each empty space that that is inside one of your 2-eyed groups and you lose 1 point of territory for each one of your stones that the opponent captured during the game. For example, suppose that the game ended like this and that neither side has captured any prisoners:

<div class="reikai_board" data_board="/static/boards/board_5_1.json"></div>

In this position black and white have both made one group each and each group has exactly two eyes. The white group has surrounded 27 empty points. White has 27 points of territory. Black has surrounded 28 empty points, so black has 28 points of territory. At the end of the game the player with the most points of territory in the winner.

How do you know when you have reached the end of the game? The game ends when both players pass consecutively instead of playing a move. In the last diagram both players have played 13 stones so it must be black's turn to play next. Suppose that he decides not to pass. Then might play here:

<div class="reikai_board" data_board="/static/boards/board_5_2.json"></div>

Suppose that now both players pass. What is the score? Why don't you try counting it? You should find that both black and white have 27 points. So by playing an extra move black has thrown away his chance of winning and it is a tie. The Japanese call a tie like this 'jigo'. This points out a general principle: It is usually bad to play a move inside your own territory.

There is of course another option. Black could have played his move inside the white territory like this:

<div class="reikai_board" data_board="/static/boards/board_5_3.json"></div>

What effect does this have? You should be able to see that whatever happens this black stone can never be turned into a 2-eyed group. This stone is dead. As I explained before, if the game were to end now white could just take this stone off of the board. Now white has 1 prisoner and so black's score is (28 points on the board) - (1 prisoner held by white) = 27. White's score is still 27 and so it is jigo again - a tie. This points out another important idea. If you can't make 2 eyes then it is probably bad to play inside your opponent's territory.

There is 1 final possibility. Black could play in the larger half of white's territory like this:

<div class="reikai_board" data_board="/static/boards/board_5_4.json"></div>

In this case black might be able to make 2 eyes inside white's territory. That would destroy most of white's territory and so white will probably try and stop this. For example:

<div class="reikai_board" data_board="/static/boards/board_5_5.json"></div>

Suppose that black now realises that he can't possibly make 2 eyes here any more. What has happened to the the score? What do you think? (Answer: Black has 28 points - 3 prisoners = 25, white has 24 points, white loses by 1 point again). This illustrates a third point. If you play inside you opponent's territory in a way that threatens to live and so your opponent has to respond then it doesn't cost you anything. This means that you should feel free to have a go at invading your opponent's territory like this. On the other hand an experienced player would realise that a move like black 1 in the last diagram going to fail, and so wouldn't play it out and it would end up costing you points and possibly the game.
