import os
import random

# number of games that will be played
games = 1000

clear = lambda: os.system('cls')

def play_game(strategy):
    # randomly select which door is the winning door and which door the player first chooses
    win_door = random.randint(0, 2)
    first_choice = random.randint(0, 2)
    # make a list of the 3 potential doors to be opened and remove the one the player chose
    doors = [0, 1, 2]
    doors.remove(first_choice)
    # if the player chose the winning door, randomly remove one of the other ones from the list
    if first_choice == win_door:
        del doors[random.randint(0, 1)]
    # if the player did not choose the winning door, remove the non-winning one from the list
    else:
        windex = doors.index(win_door)
        if windex == 0:
            del doors[1]
        elif windex == 1:
            del doors[0]
    # note what the "unopened" door is
    second_choice = doors[0]

    # do whatever strategy is inputted
    if strategy == "random":
        if random.randint(0, 1) == 1:
            strategy = "stick"
        else:
            strategy = "switch"
    
    if strategy == "stick":
        final_choice = first_choice
    elif strategy == "switch":
        final_choice = second_choice
    
    # output the results
    if final_choice == win_door:
        return "1" # 1 means win
    else:
        return "0" # 0 means lose

def play(player, strategy):
    # play games number of games, and print the number of wins and losses
    wins = 0
    for i in range(games):
        result = play_game(strategy)
        wins += int(result)
    print(player + " win %: " + str(wins / games * 100))

clear()
# steve plays by always sticking with his original choice
#play("steve", "stick")
# bob plays by always switching his choice
#play("bob", "switch")
# mike plays by randomly either switching or sticking with his original choice
#play("mike", "random")
# according to math steve should win 1/3 of the time, bob should win 2/3 of the time
# mike on average will do each strategy 50% of the time, so he should win 1/2 of the time (the average of 1/3 and 2/3)

learning_games = 1000
options = ["stick", "switch", "random"]
winrate = [1.0, 1.0, 1.0]
gamesplayed = [0, 0, 0]
for i in range(learning_games):
    # he decides what strategy to use based on which has the highest previous win rate
    choice = winrate.index(max(winrate))
    # prevents getting stuck on a worse strategy because of early bad luck with a better one
    if gamesplayed[choice] == max(gamesplayed) and max(winrate) < 0.51:
        choice = random.randint(0, 2)
    # randomly picks a strategy if they all have the same winrate
    if max(winrate) == min(winrate):
        choice = random.randint(0, 2)
    strategy = options[choice]
    # he plays a game with that strategy
    result = int(play_game(strategy))
    # update win rate for that choice
    wins = winrate[choice] * gamesplayed[choice] + result
    gamesplayed[choice] += 1
    winrate[choice] = wins / gamesplayed[choice]
print("gamesplayed: " + str(gamesplayed))
print("winrate: " + str(winrate))
print("best strategy: " + options[winrate.index(max(winrate))])
print("games spent on other strategies: " + str(sum(gamesplayed, 0) - gamesplayed[winrate.index(max(winrate))]))



'''
This is the second attempt at making the learning bot.
This one learns by playing a set number of test games, comparing the win rates, and then playing the desired number of games
using the strategy with the best win rate.
The problem with this one is that it relies on a preset number of played games and will always have a chance of getting unlucky
and not picking the best strategy, especially with a low number of test games.
This one also doesn't continue to learn as it plays, it does its learning at the start and then just plays.
'''
'''
# jeff is a bot the learns the best strategy for the game
wins = [0, 0]
gamesplayed = [0, 0]
test_games = 1000

for i in range(test_games):
    # he will play "test_games" games of both strategies, and then choose the best strategy
    result = int(play_game("stick"))
    wins[0] += result
    gamesplayed[0] += 1

    result = int(play_game("switch"))
    wins[1] += result
    gamesplayed[1] += 1

stick_wr = wins[0] / gamesplayed[0]
switch_wr = wins[1] / gamesplayed[1]
if stick_wr > switch_wr:
    best_strategy = "stick"
elif switch_wr > stick_wr:
    best_strategy = "switch"
else:
    best_strategy = "random"
play("jeff", best_strategy)
'''


'''
This is the first attempt at making a bot that learns the best strategy.
The problem with this bot is that it has a bias to choose the first strategy it wins with.
This is because it picks the strategy with the highest win rate, and after losing the first game with a strategy,
the win rate for that strategy becomes zero, causing the bot to always choose the other strategy as long as it has
won at least 1 game with that strategy in the past.
'''
'''
# his experience is stored in winrate, index 0 is the win rate for the stick strategy, and index 1 is the switch strategy
winrate = [1.0, 1.0]
gamesplayed = [0, 0]
for i in range(games):
    # he decides what strategy to use based on which has the highest previous win rate
    choice = winrate.index(max(winrate))
    if max(winrate) == min(winrate):
        choice = random.randint(0, 1)
    if choice == 0:
        strategy = "stick"
    else:
        strategy = "switch"
    # he plays a game with that strategy
    result = int(play_game(strategy))
    # update win rate for that choice
    wins = winrate[choice] * gamesplayed[choice] + result
    gamesplayed[choice] += 1
    winrate[choice] = wins / gamesplayed[choice]
print("gamesplayed: " + str(gamesplayed))
print("winrate: " + str(winrate))
'''