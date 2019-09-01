##Eyes and the Uncapturable
You might be asking, "but are there any groups that can avoid capture indefinitely?". The answer is yes, because of the next rule of go: "You may not commit suicide". That is, you may not play a move that causes one or more of your own stones to be captured. This needs to be thought about carefully. Consider the following 2 similar situations: 

<div class="reikai_board" data_board="/static/boards/board_4_1.json"></div>

The white group on the right has 1 liberty left. Black can remove it by playing in the middle which captures the white stones like this:

<div class="reikai_board" data_board="/static/boards/board_4_2.json"></div>

However the white group on the left has 10 liberties. Suppose that black tries to play in the middle of it like this:

<div class="reikai_board" data_board="/static/boards/board_4_3.json"></div>

This does not, of course, capture the white stones because they still have 9 liberties. Instead it is the black stone that have no liberties left and should be captured. This is a suicide move and is not allowed. You should compare the two moves 'black 1' in the previous 2 diagrams and make sure you understand why one is legal and the other is illegal. As a test why not try and work out which of the following black moves are legal.

<div class="reikai_board" data_board="/static/boards/board_4_4.json"></div>

_(Answer: Black 1 and 2 are illegal. Black 3 and 4 are legal.)_

Now that you understand the suicide rule have a look at this white group:

<div class="reikai_board" data_board="/static/boards/board_4_5.json"></div>

 The white stones have 2 liberties. There are only 2 moves that might reduce the number of liberties on the white stones, but both of them are illegal. Therefore the white stones will always have at least 2 liberties and so can never be captured. An area of surrounded space like this is called an eye. The important fact is that a group with 2 eyes is alive. That is, it can never be captured. (Well, it could be captured if white played inside one of his own eyes, but that would be a rather silly thing for white to do!)

Eyes can be bigger than a single space. For example:

<div class="reikai_board" data_board="/static/boards/board_4_6.json"></div>

This white group has two big eyes and so it is alive. Black could play 3 legal moves inside it like this:

<div class="reikai_board" data_board="/static/boards/board_4_7.json"></div>

But now black cannot reduce the liberties of the black group further. Again, the white group will always have at least 2 liberties. It has 2 eyes; it is alive; black can never capture it.

On the other hand this group:

<div class="reikai_board" data_board="/static/boards/board_4_8.json"></div>

has only got 1 eye. Black may have surrounded 2 points, but they are not separate, so black could capture the white stones like this:

<div class="reikai_board" data_board="/static/boards/board_4_9.json"></div>

<div class="reikai_board" data_board="/static/boards/board_4_10.json"></div>

Whilst there are 2-eyed groups that can never be captured there are also groups that you can be sure will get captured eventually. For example consider this black group:

<div class="reikai_board" data_board="/static/boards/board_4_11.json"></div>

Whatever black does this group can never get 2 eyes. Therefore white will be able to capture it whenever he likes. _(Question: how?)_. If there is a group like this left on the board when both players pass and the game ends then the rules say that white can just pick up the black stones off the board as prisoners.

So now you know how to capture groups of stones by surrounding them, you know how to stop your groups being captured by making 2 eyes, and you know that there are some groups that are doomed to die eventually. To familiarise yourself with the rules so far you might find it helpful to play a few games of so-called 'capture go'. Capture go is played according to the rules I have listed so far, and the winner is the first person to capture a predetermined number of stones. For example the first person to capture 3 stones, or 5 stones. Capture go is not very interesting however because (like noughts and crosses) it always ends in a draw when played well.
