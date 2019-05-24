from twitchobserver import Observer
import time

#Initialisation: create empty dict for scores, empty list for players, rules
#as an easily-gettable string, set timer to 300 seconds from initialisation

scores = {}
players = []
rules = "The rules: Jack will ask a question. From the point I send a message"
        "saying you have 20 seconds, that's how long you have to type a, b, "
        "c or d to commit your answer. Only your first answer will count!"
rule_timer = time.time() + 300

#function for user commands. "!rules" will send the rules string to the chat
#and then set the timer to 300 seconds from when this happens to prevent
#it occurring automatically before then - too many rules are annoying

def commands(event):
    global rule_timer
    if event.type == "TWITCHCHATMESSAGE":
        if event.message.lower() == "!rules":
            observer.send_message(rules, "jackdawdottv")
            rule_timer = time.time() + 300

#!quit will tell Observer to stop listening for further commands and leave the
#channel without a fuss.

    if event.type == "TWITCHCHATMESSAGE":
        if event.message.lower() == "!quit":
            observer.send_message("Thanks for playing!", "jackdawdottv")
            observer.unsubscribe(commands)
            observer.leave_channel("jackdawdottv")
            observer.stop()

#function for parsing answers. This checks all messages in the chat to see if
#they exactly match the correct answer when both are lowercased. If they do,
#and the chatter's username is not already in the player list, the name is
#added and the answer recorded. If the user already has a score of 1 or more
#in the scores dict, increment by 1, otherwise add to dict with a score of 1.
            
def receive_answer(event):
    global players
    if event.type == "TWITCHCHATMESSAGE":
        if event.nickname not in players:
            if event.message.lower() == correct.lower():
                if event.nickname in scores:
                    scores[event.nickname] += 1
                else:
                    scores[event.nickname] = 1
            players.append(event.nickname)

#bot initialisation. Give Observer a username and OAuth key, start the bot,
#join the twitch channel, send a welcome message and start listening for
#commands listed in the commands function

observer = observer("JackScore", "oauth:**************************")

observer.start()
observer.join_channel("jackdawdottv")

observer.send_message("Let the game begin!", "jackdawdottv")
observer.subscribe(commands)

#While the bot is running, if the current time is equal to or greater than
#that stored in the timer variable, send the rules and reset the timer to
#300 seconds from trigger

while True:

    if time.time() >= rule_timer:
        observer.send_message(rules, "jackdawdottv")
        rule_timer = time.time() + 300

#This is the answering section. Initialise the players list so nobody gets
#prevented from answering, ask host to input the correct answer. Once correct
#answer has been entered, warn chat that they have 20 seconds to answer. Start
#using the receive_answer function and begin a timer (sleep). Once the timer is
#over, stop listening for answers and send the correct answer.

    try:
        players = []
        correct = input("correct answer is: ")
        observer.send_message("You have 20 seconds, type your answer now!",
                              "jackdawdottv")
        observer.subscribe(receive_answer)
        time.sleep(10)
        observer.send_message("Ten seconds left!", "jackdawdottv")
        time.sleep(10)
        observer.unsubscribe(receive_answer)
        observer.send_message("Time's up! the correct answer was " + correct, 
                              "jackdawdottv")
#emergency break

    except KeyboardInterrupt:
        observer.unsubscribe(commands)
        observer.leave_channel("jackdawdottv")
        break

#list scores in console for the host to track

    print(scores)
