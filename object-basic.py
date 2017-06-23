import random

class Pet:

    def speak(self):
        print(self.speakSound)


class Dog(Pet):

    def sit(self):
        print("The dog sits")

class BigDog(Dog):

    def __init__(self):
        self.speakSound = "Woof"
        self.description = "A large, muscular dog"

class SmallDog(Dog):

    def __init__(self):
        self.speakSound = "Yip"
        self.description = "A tiny, cute dog"

class Cat(Pet):
    speakSound = "Meow"


class HouseCat(Cat):

    def __init__(self):
        self.description = "A cat with fluffy, white fur"
    def purr(self):
        print("Purrr")

class StrayCat(Cat):

    def __init__(self):
        self.description = "A cat with tousled, striped fur"



petClasses = [BigDog, SmallDog, HouseCat, StrayCat]



print('Choose a number greater then 0')


numberOfPets = 0

while numberOfPets < 1:

    try:
        numberOfPets = int(input())
    except ValueError:
        print("Value must be an integer greater then 0")
    else:
        numberOfPets = numberOfPets

    if numberOfPets < 1:
        print("Value must be an integer greater then 0")





for petCount in range(0, numberOfPets):

    pet = petClasses[random.randrange(4)]()
    # Print the info for part 3 of the assignment description here
    print('~~~~~~~~~~')
    print('Pet number',petCount+1)
    print('----------')
    print(pet.description)
    pet.speak()
    if  isinstance(pet,Dog):
        pet.sit()
    if isinstance(pet,HouseCat):
        pet.purr()
    print('~~~~~~~~~~')
