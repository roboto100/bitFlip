import random

class bits:

    def __init__(self):
        self.lst = []
        for i in range(100):
            self.lst.append(random.randint(0,1))

        self.guesses = 0

    def guess(self, sequence):
        count = 0
        for i in range(100):
            if self.lst[i]==sequence[i]:
                count+=1
        self.guesses += 1
        return count


def naive():
    '''
    Performs a naive algorithm to solve the problem
    :return: Number of guesses taken
    '''

    # Have 2 lists. One to guess with and one to store the bits we're confident about
    myStorage = [0]*100
    myGuess = [0] * 100

    # Take a guess that all bits are 0
    AllZeros = myBits.guess(myGuess)

    # For every bit
    for i in range(100):
        # Flip that bit
        myGuess[i] = 1
        # Decide if that's improved our number of correct bits
        correct = myBits.guess(myGuess)
        # If it has improved the count
        if correct>AllZeros:
            # That bit must be a 1
            myStorage[i] = 1
        # Change that guess back to a 0, so we're constant with our guesses
        myGuess[i] = 0

    # Get how many guesses were required to find a solution
    guessesRequired = myBits.guesses
    # Check the solution is correct, and return how many guesses we took
    assert myBits.guess(myStorage) == 100, "A naive approach resulted in an incorrect answer"
    return guessesRequired

def chunking2():
    '''
    Performs a chunking approach. Groups bits into groups of 2, guessing both bits at once, reducing number of guesses
    :return: Number of guesses
    '''

    # Have 2 lists, one for guessing and one for storing our known bits
    myStorage = [0] * 100
    myGuess = [0] * 100

    # Start out with a guess of all 0's
    AllZeros = myBits.guess(myGuess)

    # For every 2 bit pair from (0,1) - (98,99) (0-49 inclusive)
    for i in range(50):
        # Calculate the first index
        index = i*2

        # Change the two indices
        myGuess[index] = 1
        myGuess[index+1] = 1

        # Guess the new bit string
        correct = myBits.guess(myGuess)

        # If we've gone up by 2, both bits must be 1
        if correct>AllZeros:
            # Store both bits
            myStorage[index] = 1
            myStorage[index+1] = 1
        # If we've gone down by 2, both bits were originally correct as 0
        elif correct<AllZeros:
            # Bits are already stored as 0's
            pass
        # We've stayed at the same number of correct bits. Either a 01 or a 10
        else:
            # 01 or 10
            # Guess 01. If this is wrong we'll get -2, otherwise +2
            myGuess[index] = 0
            correct = myBits.guess(myGuess)
            if correct>AllZeros:
                myStorage[index+1]=1
            else:
                myStorage[index] = 1
        # Reset the guess, prepare to move to next bit pair
        myGuess[index] = 0
        myGuess[index+1] = 0

    # Get how many guesses were required to find a solution
    guessesRequired = myBits.guesses
    # Check the solution is correct, and return how many guesses we took
    assert myBits.guess(myStorage) == 100, "A chunking approach (2 chunking) resulted in an incorrect answer"
    return guessesRequired

def chunking3():
    '''
    Performs a chunking approach. Groups bits into groups of 3, guessing all bits at once. If the guess doesn't get a
    111 or 000, we've split the remaining 6 options into 2 groups [001,010,100] & [110,101,011] use a second guess
    (depending on which group it's in) to reduce to 2 in each group, and use one last guess if we require it.
    Should take 1(2/8)+2(2/8)+3(4/8)=2.25 guesses to guess 3 bits; ~75% efficiency
    :return: Number of guesses
    '''

    # Have 2 lists, one for guessing and one for storing our known bits
    myStorage = [0] * 100
    myGuess = [0] * 100

    # Guess all 0's to begin with
    AllZeros = myBits.guess(myGuess)

    # Solve the first bit so we can divide the remaining 99 by 3 equal bits
    myGuess[0] = 1
    correct = myBits.guess(myGuess)
    if correct>AllZeros:
        myStorage[0] = 1
    myGuess[0] = 0

    # For all the remaining 33 groups
    for i in range(33):
        # Calculate the index of the first bit
        index = i*3+1

        # Update our guess, get the number of correct bits
        myGuess[index] = 1
        myGuess[index+1] = 1
        myGuess[index+2] = 1
        correct = myBits.guess(myGuess)

        # If we've gone up or down by 0; update the storage
        if correct-AllZeros==-3:
            #000
            pass
        elif correct-AllZeros==3:
            #111
            myStorage[index] = 1
            myStorage[index + 1] = 1
            myStorage[index + 2] = 1
        # If we've gone down by 1, we have one of [001,010,100]
        elif correct-AllZeros==-1:
            # Guess 001
            myGuess[index] = 0
            myGuess[index + 1] = 0
            myGuess[index + 2] = 1
            correct = myBits.guess(myGuess)
            # If we go up by 1 point, we were right. Update storage
            if correct-AllZeros==1:
                myStorage[index] = 0
                myStorage[index + 1] = 0
                myStorage[index + 2] = 1
            # If we didn't go up by 1, we were wrong. Either 010 or 100
            else:
                # Guess 010, and get the new points
                myGuess[index] = 0
                myGuess[index + 1] = 1
                myGuess[index + 2] = 0
                correct = myBits.guess(myGuess)
                # If we went up by 1, we got it right. Update storage
                if correct-AllZeros==1:
                    myStorage[index] = 0
                    myStorage[index + 1] = 1
                    myStorage[index + 2] = 0
                # Otherwise, we have 100, so update storage
                else:
                    myStorage[index] = 1
                    myStorage[index + 1] = 0
                    myStorage[index + 2] = 0
        # Otherwise, we have one of [110,101,011]
        elif correct-AllZeros==1:
            # Guess 110
            myGuess[index] = 1
            myGuess[index + 1] = 1
            myGuess[index + 2] = 0
            correct = myBits.guess(myGuess)
            # If we go up by 2 points, we got it right; update storage
            if correct - AllZeros == 2:
                myStorage[index] = 1
                myStorage[index + 1] = 1
                myStorage[index + 2] = 0
            # Otherwise, either 101 or 011
            else:
                # Guess 101
                myGuess[index] = 1
                myGuess[index + 1] = 0
                myGuess[index + 2] = 1
                correct = myBits.guess(myGuess)
                # If we go up by 2 points, we're right. Update storage
                if correct - AllZeros == 2:
                    myStorage[index] = 1
                    myStorage[index + 1] = 0
                    myStorage[index + 2] = 1
                # Otherwise, it must have been 011. Update storage
                else:
                    myStorage[index] = 0
                    myStorage[index + 1] = 1
                    myStorage[index + 2] = 1
        # Reset guesses for next pass
        myGuess[index] = 0
        myGuess[index + 1] = 0
        myGuess[index + 2] = 0

    # Get how many guesses were required to find a solution
    guessesRequired = myBits.guesses
    # Check the solution is correct, and return how many guesses we took
    assert myBits.guess(myStorage) == 100, "A chunking approach (3 chunking) resulted in an incorrect answer"
    return guessesRequired

def divide(index1, index2, zerosSection, allZeros):
    '''
    Take in some variables about the bit sequence, along with some indices. Flip half the bits between those indices to
    calculate how many 0's are in the first half, and how many are in the second half of this range
    :param index1: Beginning of bits that are being flipped
    :param index2: End of bits that are being flipped (inclusive)
    :param zerosSection: How many 0's are in this section
    :param allZeros: How many 0's are in the whole bitstring
    :return: List, [Zeros in section 1, Zeros in section 2]. Section 1 is from [index1,(index1+index2)//2]
    '''

    # Start of with a full set of 0's
    myGuess = [0]*100

    # Flip the bits from half of the range
    for i in range(index1, ((index2+index1)//2)):
        myGuess[i] = 1

    # Calculate how many bits are correct with the new string, and how many were correct with all 0's
    n2 = myBits.guess(myGuess)
    n1 = allZeros

    # Caclualte the size of the region we're flipping
    size = (index2-index1)//2

    # Calculate how many 0's are in the first section
    rhs = size+n1-n2
    x = rhs/2

    # Round this number to the nearest integer, so we don't deal with weird floating point maths.
    x = round(x)

    return [x, zerosSection-x]

def subDivide():
    '''
    Performs a divide and conquer approach. Calculates how many 0's are in the next n bits; then splits that into the
    next n//2 bits. Repeats for all bits; until we have either 0 0's in the next n bits, or n 0's in the next n bits.
    :return: Number of guesses it takes
    '''

    # Start off by guessing all 0's
    myGuess = [0] * 100
    allZeros = myBits.guess(myGuess)

    # Create 2 lists. One stores the number of 0's in the next k bits, and the other stores the values of k
    numZeros = [allZeros]
    distance = [100]

    # Until we can't split the lists anymore
    i = 0
    while (i<len(numZeros)):
        # While we can split the current number being looked at
        while ((numZeros[i]!=distance[i])&(numZeros[i]!=0)):
            # Calculate how far into the string we are
            index1 = 0
            for k in range(0,i):
                index1 += distance[k]

            # Split the current index being looked at into 2
            getData = divide(index1,index1+distance[i], numZeros[i], allZeros)

            # Insert the new information we gained into the two lists
            numZeros = numZeros = numZeros[0:i] + getData + numZeros[(i+1):]
            distance = distance[0:i] + [distance[i]//2, distance[i]//2 + distance[i]%2] + distance[(i+1):]
        # Move up one section, try splitting the next section
        i+=1

    # Using the two lists we've been building, create the bitstring we must have been working with
    myGuess = []
    for index in range(len(distance)):
        if numZeros[index]==0:
            myGuess = myGuess + [1] * distance[index]
        else:
            myGuess = myGuess + [0] * distance[index]

    # Get how many guesses were required to find a solution
    guessesRequired = myBits.guesses
    # Check the solution is correct, and return how many guesses we took
    assert myBits.guess(myGuess) == 100, "A divide and conquer approach resulted in an incorrect answer"
    return guessesRequired

totalGuesses = 0
maxTests = 4000

for test in range(maxTests):
    myBits = bits()
    totalGuesses += subDivide()

print(totalGuesses/maxTests)