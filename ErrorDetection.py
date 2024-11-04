# Name: Trevor Justice

class ErrorDetection:


    def computeCheckSum(self, message, parity):
        '''
        Computes the parity of all characters in the message, and changes the most-significant bit of a
        character to 1 if it is not equal to the given parity.
        :param message: str: the message to compute the checksum for.
        :param parity: bin: 0 for even, 1 for odd.
        :return newString: str: the given message with correct parity amongst all characters.
        '''
        listOfInts = []
        newString = ""
        for i in range(0, len(message)):
            # populates listOfInts with each character in message, represented as integers
            listOfInts.append(ord(message[i]))

        for i in listOfInts:
            # calculates the number of 1's in each element of listOfInts
            count = i.bit_count()

            if count%2 != parity:
                # makes the most-significant bit 1 if parities do not align
                mask = 1 << 7
                i = i | mask

            newString += chr(i) # creates string with corrected parities of each character
        return newString


    def verifyCheckSum(self, message, parity):
        '''
        Verifies each character in message has the given parity, and flags an error before changing
         the most-significant bit of a character to 0.
        :param message: str: the message to compute the checksum for.
        :param parity: bin: 0 for even, 1 for odd.
        :return error: bool/ True if a parity error occurs, False if a parity error does not occur.
        :return newString: str/ the given message with the most-significant bit of each character
        reverted back to 0.
        '''
        listOfInts = []
        newString = ""
        error = False
        for i in range(0, len(message)):
            # populates listOfInts with each character in message, represented as integers
            listOfInts.append(ord(message[i]))

        for i in listOfInts:
            # calculates the number of 1's in each element of listOfInts
            count = i.bit_count()

            if count%2 != parity:
                # reports an error is parities do not align
                error = True

            # turns the most-significant bit to a 0
            mask = (1 << 7) - 1
            i = i & mask

            newString += chr(i) # creates string with corrected parities of each character

        return error, newString


