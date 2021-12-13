import re
import numpy as np

def transactionScrape(filing, counter, dat, n, k, columnNumber, columnNames):
    """
    takes a filing and loops through the text file allocating each transaction to the correct column
    Paramters:
        filing (string): the text file of the filing
        counter (int): row increment
        dat (DataFrame): current relational DataFrame
        n (int): start position of what columns to insert new values into
        k (int): end position of what columns to insert new values into
        columnNumber (int): column increment
        columnNames (list): list containing the column names
    Returns:
        dat (DataFrame): returns the DataFrame that just had new values inserted.
    """
    for columnName in columnNames[n:k]:
        try:
            filterOne = a1 + columnName + a2 + columnName + a3
            filterTwo = e1 + columnName + e2
            filterThree = e3 + columnName + e2

            valueOne = re.search(filterOne, filing, flags = re.MULTILINE | re.DOTALL)[0]
            valueTwo = re.sub(filterTwo, "", valueOne)
            valueThree = re.sub(filterThree, "", valueTwo)

            dat.iloc[counter, columnNumber] = valueThree
            
            columnNumber += 1

        except:
            columnNumber += 1

    return(dat)