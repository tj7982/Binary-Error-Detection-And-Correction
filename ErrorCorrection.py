# Name: PUT YOUR NAME HERE


import math
import random
import copy

class ErrorCorrection:
    def __init__(self, m, r):
        '''
        This is the constructor
        :param m: int: Number of message bits
        :param r: int: Number of check bits
        '''

        self.__m = m
        self.__r = r
    def prepareMessage(self, message):
        '''
        Takes a string containing a single character and converts its binary code into
        a list of integers, with additional elements included for check bits set to 0.
        :param message: a string containing a single character
        :return codeword: a list of integers, either 1 or 0, with element 0 set to None
        '''
        asciiCode = ord(message)
        codeword = []

        # Convert the Ascii code of the message to a list of zeros and ones.

        # This will only work if we have atmost 7 significant bits (i.e. the
        # message is in the ASCII table and least than 128).
        for bitNum in range(7):
            # Because we are inserting, we will have the most significant bit be in
            # position 0, but that's ok as long as we convert it back to ascii in
            # the same order.
            codeword.insert(0, asciiCode % 2) # Insert the least significant bit.
            asciiCode = asciiCode >> 1         # Shift the bits
            bitNum += 1

        # Put a None in position zero so that the bits start numbering at 1 instead of 0.
        codeword.insert(0, None)

        # Add the checkbits at the positions of powers of two.
        checkBitNum = 1
        for i in range(self.__r):
            codeword.insert(checkBitNum, 0)
            checkBitNum = checkBitNum << 1


        return codeword


    def extractMessage(self, codeword):
        '''
        Takes a list comprised of elements equal to None, 0, or 1. Removes the elements
        in position of checkbits, and turns the remaining elements into a binary representation
        of a character. It then turns the binary into a unicode character.
        :param codeword: a list of integers, either 1 or 0, with element 0 set to None
        :return chr(asciiCode): a unicode representation of a character.
        '''
        asciiCode = 0

        # Remove the checkbits at the positions of powers of two.
        # We need to go backwards so that the indexes don't get off.
        # If we delete index 1, then index 2 will become the new 1.
        # But if we go backward, e.g. delete index 8, then index 2
        # is still the same one.
        checkBitNum = 1 << (self.__r - 1)
        while checkBitNum > 0:
            del codeword[checkBitNum]
            checkBitNum = checkBitNum >> 1

        # delete the None that was put into position 0.
        del codeword[checkBitNum]

        # Convert the list back to an integer
        for i in range(len(codeword)):
            asciiCode = asciiCode * 2 + codeword[i]

        # Finally, return the character
        return chr(asciiCode)


    def encodeMessage(self, message, parity):
        '''
        Takes a list of integers, set to either None, 0, or 1. Identifies which elements
        represent checkbits, and calculates their value according to given parity, replacing
        their value with the appropriate 0 or 1.
        :param message: a string containing a single character
        :param parity: 0 for even, 1 for odd
        :return newMessage: a list of integers, either None, 0, or 1, with proper values in checkbit
        locations.
        '''

        newMessage = self.prepareMessage(message)

        # calculates parity in positions 1, 3, 5, 7, 9, and 11
        checkBitOne = newMessage[1]+newMessage[3]+newMessage[5]+newMessage[7]+newMessage[9]+newMessage[11]
        # flips checkbit to 1 if parity is not correct
        if checkBitOne%2 != parity:
            newMessage[1] = 1

        # calculates the parity in positions 2, 3, 6, 7, 10, 11
        checkBitTwo = newMessage[2]+newMessage[3]+newMessage[6]+newMessage[7]+newMessage[10]+newMessage[11]
        # flips checkbit to 1 if parity is not correct
        if checkBitTwo%2 != parity:
            newMessage[2] = 1

        # calculates the parity  in positions 4, 5, 6, 7
        checkBitThree = newMessage[4]+newMessage[5]+newMessage[6]+newMessage[7]
        # flips checkbit to 1 if parity is not correct
        if checkBitThree%2 != parity:
            newMessage[4] = 1

        # calculates the parity in positions 8, 9, 10, 11
        checkBitFour = newMessage[8]+newMessage[9]+newMessage[10]+newMessage[11]
        # flips checkbit to 1 if parity is not correct
        if checkBitFour%2 != parity:
            newMessage[8] = 1

        return newMessage




    def correctMessage(self, codeword, parity):
        '''
        Calculates the checkbit parities and determines if there is an error. If there is an error,
        the incorrect bit is located and flipped. It then calls upon extractMessage() to extract
        the character from the valid codeword.
        :param codeword: a list of integers, either 1 or 0, with element 0 set to None
        :param parity: 0 for even, 1 for odd
        :return validMessage: a single character string
        '''

        # variable used to identify what position a 1-bit error will be in
        incorrectCheckBitSum = 0

        checkBitOne = codeword[1] + codeword[3] + codeword[5] + codeword[7] + codeword[9] + codeword[11]
        if checkBitOne%2 != parity:
            incorrectCheckBitSum += 1

        checkBitTwo = codeword[2] + codeword[3] + codeword[6] + codeword[7] + codeword[10] + codeword[11]
        if checkBitTwo%2 != parity:
            incorrectCheckBitSum += 2

        checkBitThree = codeword[4] + codeword[5] + codeword[6] + codeword[7]
        if checkBitThree %2 != parity:
            incorrectCheckBitSum += 4

        checkBitFour = codeword[8] + codeword[9] + codeword[10] + codeword[11]
        if checkBitFour%2 != parity:
            incorrectCheckBitSum += 8

        # checks if an error has indeed occured - if 0, all parities from checkbits were correct
        if incorrectCheckBitSum != 0:
            # flips a bit from 0 to 1
            if codeword[incorrectCheckBitSum] == 0:
                codeword[incorrectCheckBitSum] = 1
            # flips a bit from 1 to 0
            else:
                codeword[incorrectCheckBitSum] = 0

        # turns list back into character string
        validMessage= self.extractMessage(codeword)

        return validMessage


