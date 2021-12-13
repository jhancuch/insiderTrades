import pandas as pd
import numpy as np
import re
import requests
import builtins
from time import sleep
from insiderTrades.utils.formFilterDerivativeHoldings import formFilterDerivativeHoldings
from insiderTrades.utils.transactionFilterDerivativeHoldings import transactionFilterDerivativeHoldings
from insiderTrades.utils.transactionScrape import transactionScrape
from insiderTrades.utils.footnoteScrape import footnoteScrape

def derivativeHoldingsScrape(index, form, name, email, footnoteKeywords = None, issuerKeywords = None, issuerTradingSymbol = None, rptOwnerKeywords = None):
    """
    Takes parameters and wrangles transactions that meet the parameters into a DataFrame.
    Parameters:
        index (DataFrame): the return object from secUrlDownload function
        form (int): integar with valid options being 4 or 5
        name (string): string consisting of the user's name for database access purposes
        email (string): string consisting of the user's email for database access purposes
        footnoteKeywords (list): list containing desired keywords located in footnotes
        issuerKeywords (list): list containing desired keywords located in the issuer's section
        issuerTradingSymbol (list): list containing desired trading symbols
        rptOwnerKeywords (list): list containing desired keywords located in the reporting owner's section
    Returns:
        dat5 (DataFrame): DataFrame containing the transactions that met the parameters
    """

    form = str(form)

    builtins.a1 = '<'
    builtins.a2 = '>.*?(</'
    builtins.a3 = '>)'
    builtins.e1 = '<'
    builtins.e2 = '>'
    builtins.e3 = '</'

    counter = 0
    statusCounter = 0
    totalRecords = len(index)

    headers = {'user-agent': str(name + ' ' + email)}

    columnNames = ["periodOfReport", "issuerCik", "issuerName", "rptOwnerCik", "rptOwnerName", "rptOwnerState", "rptOwnerZipCode", "isDirector", "isOfficer", "isTenPercentOwner", "isOther", "officerTitle", "securityTitle", "conversionOrExercisePrice", "exerciseDate", "expirationDate", "underlyingSecurityTitle", "underlyingSecurityShares", "sharesOwnedFollowingTransaction", "directOrIndirectOwnership", "natureOfOwnership", "footnote1", "footnote2", "footnote3", "footnote4", "footnote5", "footnote6", "footnote7", "footnote8", "footnote9", "footnote10", "footnote11", "footnote12", "footnote13", "footnote14", "footnote15", "footnote16", "footnote17", "footnote18", "footnote19", "footnote20", "footnote21", "footnote22", "footnote23", "footnote24", "footnote25", "footnote26", "footnote27", "footnote28", "footnote29", "footnote30", "URL", "manyPeopleManyTransactions", "Notes"]
    dat = pd.DataFrame(index=np.arange(len(index)*20), columns = columnNames)

    """
    The loop takes each url, pulls down the filing, checks for key words (or lack there of), and pulls the information into a relational dataset if the key word conditions are satisfied
    """
    
    for i in index:
        try:
            response = requests.get(i, headers=headers, allow_redirects = False)
            response.encoding = 'utf-8'
            filing = response.text
        # If an error occurs, it is likely because the SEC has blocked the IP address. The scraper waits 15 minutes before sending another request.
        except:
            print("error occured while accessing the filing, the scraper has paused for 15 minutes")
            sleep(900)
            response = requests.get(i, headers=headers, allow_redirects = False)
            response.encoding = 'utf-8'
            filing = response.text
        
        try:
            check = re.search(r'<documentType>.*?<ownerSignature>', filing, flags = re.MULTILINE | re.DOTALL)[0]
        
        except:
            print("error occured while accessing the filing, the scraper has paused for 15 minutes")
            sleep(900)
            response = requests.get(i, headers=headers, allow_redirects = False)
            response.encoding = 'utf-8'
            filing = response.text
        
        statusCounter += 1
        if statusCounter % 100 == 0:
            currentPct = str(round((statusCounter/totalRecords)*100, 2))
            print(currentPct + " % Complete")
        
        # Limit program to 3 to 4 requests to the SEC server every second
        sleep(.05)
        
        # These following lines clean the document of uncessary characters and limits us to just the non-derivitive section
        filingExtract = re.search(r'<documentType>.*?<ownerSignature>', filing, flags = re.MULTILINE | re.DOTALL)[0]
        filingCleaned = re.sub(r'<nonDerivativeTable.*?</nonDerivativeTable>|<derivativeTransaction.*?</derivativeTransaction>|<value>|</value>',
                                "", filingExtract, flags = re.MULTILINE | re.DOTALL)
       
        # the function is the first filter. It counts of the number of keywords a form has. If it is greater than zero, it moves onto the switch which determines how many reporting owners
        # it has and how many transactions. Once that has been determined, the form goes through a second filter at the individual transaction level to ensure that only transactions that
        # meet the keyword criteria are scraped. By having this first filter, it cuts down on computation (thus resources and time)

        # now called formFilterNonderivativeTransaction
        keyCount = formFilterDerivativeHoldings(filing = filingCleaned, footnoteKeywords = footnoteKeywords, issuerKeywords = issuerKeywords, issuerTradingSymbol = issuerTradingSymbol, rptOwnerKeywords = rptOwnerKeywords)

        if keyCount > 0 or (footnoteKeywords is None and issuerKeywords is None and issuerTradingSymbol is None and rptOwnerKeywords is None):

            # This determines the amount of people in the filing and the number of filings in the record. This then dictates which loop will clean the document
            filingCount = len(re.findall("<securityTitle>", filingCleaned, flags = re.MULTILINE | re.DOTALL))
            peopleCount = len(re.findall("<reportingOwner>", filingCleaned, flags = re.MULTILINE | re.DOTALL))

            if filingCount == 1 and peopleCount == 1:
                """
                One person/entity and one transaction loop
                """

                # Second filter at the transaction level checking to see if the transaction satisfies the keyword criteria. If it does, the information is scraped. If it doesn't, a new transaction from the form is pulled
                keyTransactionCount = transactionFilterDerivativeHoldings(filing = filingCleaned, footnoteKeywords = footnoteKeywords, issuerKeywords = issuerKeywords, issuerTradingSymbol = issuerTradingSymbol, rptOwnerKeywords = rptOwnerKeywords)
                
                if keyTransactionCount > 0 or (footnoteKeywords is None and issuerKeywords is None and issuerTradingSymbol is None and rptOwnerKeywords is None):

                    dat = transactionScrape(filing = filingCleaned, counter = counter, dat = dat, n = 0, k = 20, columnNumber = 0, columnNames = columnNames)
                    dat = footnoteScrape(filing = filingCleaned, counter = counter, dat = dat, n = 21, k = 51, footnoteNumber = 1, columnNumber = 21, transactionType = "derivativeHolding", columnNames = columnNames)
                    dat.iloc[counter, 51] = i

                    counter += 1
            
            elif filingCount > 1 and peopleCount == 1:
                """
                One person/entity and multiple transactions loop
                """

                transactionCount = len(re.findall("<securityTitle>", filingCleaned, flags = re.MULTILINE | re.DOTALL))

                while transactionCount >= 1:

                    keyTransactionCount = transactionFilterDerivativeHoldings(filing = filingCleaned, footnoteKeywords = footnoteKeywords, issuerKeywords = issuerKeywords, issuerTradingSymbol = issuerTradingSymbol, rptOwnerKeywords = rptOwnerKeywords)
                
                    if keyTransactionCount > 0 or (footnoteKeywords is None and issuerKeywords is None and issuerTradingSymbol is None and rptOwnerKeywords is None):

                        dat = transactionScrape(filing = filingCleaned, counter = counter, dat = dat, n = 0, k = 20, columnNumber = 0, columnNames = columnNames)
                        dat = footnoteScrape(filing = filingCleaned, counter = counter, dat = dat, n = 21, k = 51, footnoteNumber = 1, columnNumber = 21, transactionType = "derivativeHolding", columnNames = columnNames)
                        dat.iloc[counter, 51] = i

                        counter += 1

                    filingCleaned = re.sub("<derivativeHolding>.*?</derivativeHolding>", "", filingCleaned, count = 1, flags = re.MULTILINE | re.DOTALL)
                    transactionCount = len(re.findall("<securityTitle>", filingCleaned, flags = re.MULTILINE | re.DOTALL))
            
                    
            elif filingCount == 1 and peopleCount > 1:
                """
                Multiple people/entities and one transaction loop
                """

                peopleCountTwo = len(re.findall("<reportingOwner>", filingCleaned, flags = re.MULTILINE | re.DOTALL))

                while peopleCountTwo >= 1:

                    keyTransactionCount = transactionFilterDerivativeHoldings(filing = filingCleaned, footnoteKeywords = footnoteKeywords, issuerKeywords = issuerKeywords, issuerTradingSymbol = issuerTradingSymbol, rptOwnerKeywords = rptOwnerKeywords)
                
                    if keyTransactionCount > 0 or (footnoteKeywords is None and issuerKeywords is None and issuerTradingSymbol is None and rptOwnerKeywords is None):

                        # This section scrapes the information for the columns associated with transaction details. 
                        dat = transactionScrape(filing = filingCleaned, counter = counter, dat = dat, n = 0, k = 20, columnNumber = 0, columnNames = columnNames)

                        # This section is for the reporting individuals
                        individualFootnotes = re.search(r'<reportingOwner>.*?</reportingOwner>', filingCleaned, flags = re.MULTILINE | re.DOTALL)[0]

                        columnCountTwo = 21
                        footnoteCount = 1

                        for columnName in columnNames[21:51]:
                            countTotal = len(re.findall('footnoteId id="F' + str(footnoteCount) + '"', individualFootnotes, flags = re.MULTILINE | re.DOTALL))

                            if countTotal > 0:
                                filterOne = a1 + 'footnote id="F' + footnoteCount + '"' + a2 + 'footnote' + a3
                                filterTwo = e1 + 'footnote id="F' + footnoteCount + '"' + e2
                                filterThree = e3 + 'footnote' + e2

                                valueOne = re.search(filterOne, filingCleaned, flags = re.MULTILINE | re.DOTALL)[0]
                                valueTwo = re.sub(filterTwo, "", valueOne)
                                valueThree = re.sub(filterThree, "", valueTwo)
            
                                dat.iloc[counter, columnCountTwo] = valueThree

                            columnCountTwo += 1
                            footnoteCount += 1

                        # this section is for the transaction
                        dat = footnoteScrape(filing = filingCleaned, counter = counter, dat = dat, n = 21, k = 51, footnoteNumber = 1, columnNumber = 21, transactionType = "derivativeHolding", columnNames = columnNames)
                        dat.iloc[counter, 51] = i
                        dat.iloc[counter, 53] = "The holding values in this observation is an aggregate amount that is shared by the other observations that share the same URL"
                        
                        counter += 1

                    filingCleaned = re.sub("<reportingOwner>.*?</reportingOwner>", "", filingCleaned, count = 1, flags = re.MULTILINE | re.DOTALL)
                    peopleCountTwo = len(re.findall("<reportingOwner>", filingCleaned, flags = re.MULTILINE | re.DOTALL))


            elif filingCount > 1 and peopleCount > 1:
                """
                Multiple people/entities and multiple transactions loop
                """

                transactionCount = len(re.findall("<securityTitle>", filingCleaned, flags = re.MULTILINE | re.DOTALL))

                while transactionCount >= 1:
                    keyTransactionCount = transactionFilterDerivativeHoldings(filing = filingCleaned, footnoteKeywords = footnoteKeywords, issuerKeywords = issuerKeywords, issuerTradingSymbol = issuerTradingSymbol, rptOwnerKeywords = rptOwnerKeywords)

                    if keyTransactionCount > 0 or (footnoteKeywords is None and issuerKeywords is None and issuerTradingSymbol is None and rptOwnerKeywords is None):
                        dat = transactionScrape(filing = filingCleaned, counter = counter, dat = dat, n = 0, k = 3, columnNumber = 0, columnNames = columnNames)
                        dat = transactionScrape(filing = filingCleaned, counter = counter, dat = dat, n = 11, k = 20, columnNumber = 11, columnNames = columnNames)

                        dat = footnoteScrape(filing = filingCleaned, counter = counter, dat = dat, n = 21, k = 51, footnoteNumber = 1, columnNumber = 21, transactionType = "derivativeHolding", columnNames = columnNames)
                        dat.iloc[counter, 52] = i
                        dat.iloc[counter, 53] = "This transaction may not be a valid to key word conditions based upon the structure of many reporting owners. This holding must be checked by hand."

                        counter += 1

                    filingCleaned = re.sub("<derivativeHolding>.*?</derivativeHolding>", "", filingCleaned, count = 1, flags = re.MULTILINE | re.DOTALL)
                    transactionCount = len(re.findall("<securityTitle>", filingCleaned, flags = re.MULTILINE | re.DOTALL))


    dat2 = dat.dropna(axis = 0, how = 'all')
    dat3 = dat2.replace(to_replace = '<footnoteId id="F([1-9]|[1-9][0-9])"/>', value = "", regex = True)
    dat4 = dat3.replace(to_replace = '&quot;', value = "", regex = True)
    dat5 = dat4.replace(to_replace = '&amp;', value = "&", regex = True)


    for i in columnNames:
        if dat5[i].dtype == 'object':
            dat5[i] = dat5[i].str.strip()
        else:
            pass
    
    return(dat5)
