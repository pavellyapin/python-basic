##My Mad Lib project
import random

##Step 1: Create lists of words and sentences

noun_list = ['Batman' , 'bro', 'gentleman', 'pablo','building','bag','shark']
verb_list = ['text' , 'run','look','kick', 'drop']
adj_list = ['slippery','strong', 'flexible','burned']
sentence_list = []
sentence_list.append('The {adj} girl told {noun} he should {verb}')
sentence_list.append("Don't {verb} next to the {adj} {noun}!")
sentence_list.append("A {noun} can {verb} in a {adj} way")

complete_sentences = []
keep_playing = 'y'
LONGEST_LIST = len(noun_list)

while keep_playing == 'y' or keep_playing == 'Y':

    print('Choose a number between 0 and ' + str(LONGEST_LIST) + ' inclusive:')

    start = True
    user_num = -1

    ##Step 2: Validate Input

    while start or (user_num > 7 or user_num < 0):

        try:
            user_num = int(input())
        except ValueError:
           print("Value must be an integer")
        else:
            user_num = user_num

        if user_num > 7 or user_num < 0 :
             print("Value must be in the range specified")
        elif user_num < 8 and user_num >= 0 :
            start = False
            break

    ##Step 3: Get random words and a sentence

    random_noun = random.randint(user_num,99)
    random_noun = random_noun % 7
    random_noun = noun_list[random_noun]

    random_verb = random.randint(user_num,99)
    random_verb = random_verb % 5
    random_verb = verb_list[random_verb]

    random_adj = random.randint(user_num,99)
    random_adj = random_adj % 4
    random_adj = adj_list[random_adj]

    random_sentence = random.randint(user_num,99)
    random_sentence = random_sentence % 3
    random_sentence = sentence_list[random_sentence]

    random_sentence = random_sentence.format(noun = random_noun , adj = random_adj , verb = random_verb)

    ##Step 4: Check if sentence was already generated

    if random_sentence in complete_sentences:
        print("*********************************************")
        print("**Generated sentence already exists in list**")
        print("*********************************************")
    else:
        complete_sentences.append(random_sentence)

    ##Step 5: Print Mad Lib list
    for i in range (0 , len(complete_sentences)):
        print(str(i+1) + ". " + complete_sentences[i])

    print("\nKeep playing? y/n")
    keep_playing = input()










