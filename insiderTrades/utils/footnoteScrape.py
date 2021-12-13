import re
import numpy as np

def footnoteScrape(filing, counter, dat, n, k, footnoteNumber, columnNumber, transactionType, columnNames):
    """
    takes a filing and loops through the text file allocating each footnote to the correct column
    Paramters:
        filing (string): the text file of the filing
        counter (int): row increment
        dat (DataFrame): current relational DataFrame
        n (int): start position of what columns to insert new values into
        k (int): end position of what columns to insert new values into
        footnoteNumber (int): start of the footnote number
        columnNumber (int): column increment
        transactionType (string): hard coded argument of what type of transaction
        columnNames (list): list containing the column names
    Returns:
        dat (DataFrame): returns the DataFrame that just had new values inserted.
    """
    query = r'<' + transactionType + '>.*?</' + transactionType + '>'
    transactionSection = re.search(query, filing, flags = re.MULTILINE | re.DOTALL)[0]

    try:
        footnoteSection = re.search(r'<footnotes>.*?</footnotes>', filing, flags = re.MULTILINE | re.DOTALL)[0]

        for columnName in columnNames[n:k]:
            countTotal = len(re.findall('footnoteId id="F' + str(footnoteNumber) + '"', transactionSection, flags = re.MULTILINE | re.DOTALL  | re.IGNORECASE))
            if countTotal > 0:
                filterOne = a1 + 'footnote id="F' + str(footnoteNumber) + '"' + a2 + 'footnote' + a3
                filterTwo = e1 + 'footnote id="F' + str(footnoteNumber) + '"' + e2
                filterThree = e3 + 'footnote' + e2

                valueOne = re.search(filterOne, footnoteSection, flags = re.MULTILINE | re.DOTALL)[0]
                valueTwo = re.sub(filterTwo, "", valueOne)
                valueThree = re.sub(filterThree, "", valueTwo)
            
                dat.iloc[counter, columnNumber] = valueThree

            columnNumber += 1
            footnoteNumber += 1

        return(dat)

    except:
        return(dat)


