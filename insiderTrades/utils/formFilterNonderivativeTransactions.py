import re

def formFilterNonderivativeTransactions(filing, footnoteKeywords = None, issuerKeywords = None, issuerTradingSymbol = None, rptOwnerKeywords = None, transactionType = None):
    """
    This function checks if any transactions on the form contain any of the keywords
    Parameters:
        filing (string): the text file of the filing
        footnoteKeywords (list): list containing desired keywords located in footnotes
        issuerKeywords (list): list containing desired keywords located in the issuer's section
        issuerTradingSymbol (list): list containing desired trading symbols
        rptOwnerKeywords (list): list containing desired keywords located in the reporting owner's section
    Returns:
        keyCount (int): value of the number of keywords found within the filing
    """

    # This section checks if any transactions on the form contain any of the footnote keywords. For each key word identified, a value of 1 is added to the score. Any form with a
    # score above 1 is then examined by the rest of the script.

    # Extract the section of the form with the transactions and also extract the footnote section
    if footnoteKeywords is not None:
        footnoteKeywordsCount = 0
        filingTransactionSection = re.search(r'<nonDerivativeTable>.*?</nonDerivativeTable>', filing, flags = re.MULTILINE | re.DOTALL)[0]
        filingFootnoteSection = re.search(r'<footnotes>.*?</footnotes>', filing, flags = re.MULTILINE | re.DOTALL)[0]

        # Check if a transaction has a footnote
        for footnote in range(1,30):
            footnote = str(footnote)
            footnoteIdText = 'footnoteId id="F' + footnote + '"'
            footnoteCitationIdentified = len(re.findall(footnoteIdText, filingTransactionSection, flags = re.MULTILINE | re.DOTALL))

            # if a footnote is identified with the transaction, we then check the footnote section for what the footnote contains. If the footnote contains a key word, the number
            # is added the tempValue.
            # this clause is for if there are more than 1 key words
            if footnoteCitationIdentified > 0 and len(footnoteKeywords) > 1:
                footnoteKeywordsJoined = "|".join(footnoteKeywords)
                specificFootnote = re.search(r'<footnote id="F' + footnote + '"' + '>.*?</footnote>', filingFootnoteSection, flags = re.MULTILINE | re.DOTALL  | re.IGNORECASE)[0]
                tempValue = len(re.findall(footnoteKeywordsJoined, specificFootnote, flags = re.MULTILINE | re.DOTALL  | re.IGNORECASE))

            # this clause is for if there is only 1 key word
            elif footnoteCitationIdentified > 0 and len(footnoteKeywords) == 1:
                footnoteKeywordsJoined = "".join(footnoteKeywords)
                specificFootnote = re.search(r'<footnote id="F' + footnote + '"' + '>.*?</footnote>', filingFootnoteSection, flags = re.MULTILINE | re.DOTALL  | re.IGNORECASE)[0]
                tempValue = len(re.findall(footnoteKeywordsJoined, specificFootnote, flags = re.MULTILINE | re.DOTALL  | re.IGNORECASE))

            # If the footnote doesn't contain a key word, we set the value as zero.
            else:
                tempValue = 0
            footnoteKeywordsCount += tempValue

    if footnoteKeywords is None:
        footnoteKeywordsCount = 0


    # this section checks if any transaction on the form contain any of the keywords in the issuer section
    if issuerKeywords is not None:
        issuerKeywordsCount = 0

        # Extract the issuer section of the form
        issuerSection = re.search('<issuer>.*?</issuer>', filing, flags = re.MULTILINE | re.DOTALL)[0]

        # we check the issuer section to see if any of our keywords appear
        if len(issuerKeywords) > 1:
                issuerKeywordsJoined = "|".join(issuerKeywords)
                tempValue = len(re.findall(issuerKeywordsJoined, issuerSection, flags = re.MULTILINE | re.DOTALL  | re.IGNORECASE))

        # this clause is for if there is only 1 key word
        elif len(issuerKeywords) == 1:
            issuerKeywordsJoined = "".join(issuerKeywords)
            tempValue = len(re.findall(issuerKeywordsJoined, issuerSection, flags = re.MULTILINE | re.DOTALL  | re.IGNORECASE))

        issuerKeywordsCount += tempValue

    if issuerKeywords is None:
        issuerKeywordsCount = 0


    # this section checks if the issuer trading symbol section contains any of the chosen trading symbols
    if issuerTradingSymbol is not None:
        issuerTradingSymbolCount = 0

        # Extract the issuer trading symbol section
        issuerTradingSection = re.search('<issuerTradingSymbol>.*?</issuerTradingSymbol>', filing, flags = re.MULTILINE | re.DOTALL)[0]

        # we check the issuer trading section to see if any of our keywords appear
        if len(issuerTradingSymbol) > 1:
                issuerTradingSymbolJoined = "|".join(issuerTradingSymbol)
                tempValue = len(re.findall(issuerTradingSymbolJoined, issuerTradingSection, flags = re.MULTILINE | re.DOTALL  | re.IGNORECASE))

        # this clause is for if there is only 1 key word
        elif len(issuerTradingSymbol) == 1:
            issuerTradingSymbolJoined = "".join(issuerTradingSymbol)
            tempValue = len(re.findall(issuerTradingSymbolJoined, issuerTradingSection, flags = re.MULTILINE | re.DOTALL  | re.IGNORECASE))

        issuerTradingSymbolCount += tempValue

    if issuerTradingSymbol is None:
        issuerTradingSymbolCount = 0
        

    # this section checks if any of the rptOwners contain any of the keywords
    if rptOwnerKeywords is not None:
        rptOwnerKeywordsCount = 0

        # Extract the reporting owner section
        rptOwnerSection = re.search('<issuer>.*?<nonDerivativeTable>', filing, flags = re.MULTILINE | re.DOTALL)[0]

        # we check the reporting owner section to see if any of our keywords appear
        if len(rptOwnerKeywords) > 1:
            rptOwnerKeywordsJoined = "|".join(rptOwnerKeywords)
            tempValue = len(re.findall(rptOwnerKeywordsJoined, rptOwnerSection, flags = re.MULTILINE | re.DOTALL  | re.IGNORECASE))

        # this clause is for if there is only 1 key word
        elif len(rptOwnerKeywords) == 1:
            rptOwnerKeywordsJoined = "".join(rptOwnerKeywords)
            tempValue = len(re.findall(rptOwnerKeywordsJoined, rptOwnerSection, flags = re.MULTILINE | re.DOTALL  | re.IGNORECASE))

        rptOwnerKeywordsCount += tempValue

    if rptOwnerKeywords is None:
        rptOwnerKeywordsCount = 0


    # this section checks if any of the transaction transactionTypes match the chosen transactionTypes
    if transactionType is not None:
        transactionTypeCount = 0

        # Extract the transaction section
        transactionTypeSection = re.search('<nonDerivativeTable>.*?</nonDerivativeTable>', filing, flags = re.MULTILINE | re.DOTALL)[0]

        # we check the transaction section to see if any of our keywords appear
        if len(transactionType) > 1:
            
            transactionTypeTemp = []
            for i in range(0, len(transactionType)):
                temp = str('<transactionCode>' + transactionType[i] + '</transactionCode>')
                transactionTypeTemp.append(temp)
                
            transactionTypeJoined = "|".join(transactionTypeTemp)
            tempValue = len(re.findall(transactionTypeJoined, transactionTypeSection, flags = re.MULTILINE | re.DOTALL  | re.IGNORECASE))
            
        # this clause is for if there is only 1 key word
        elif len(transactionType) == 1:
            transactionTypeJoined = str('<transactionCode>' + transactionType + '</transactionCode>')
            tempValue = len(re.findall(transactionTypeJoined, transactionTypeSection, flags = re.MULTILINE | re.DOTALL  | re.IGNORECASE))

        transactionTypeCount += tempValue
    
    if transactionType is None:
        transactionTypeCount = 0


    # Sum up all the keywords identified in a single form
    keyCount = footnoteKeywordsCount + issuerKeywordsCount + issuerTradingSymbolCount + rptOwnerKeywordsCount + transactionTypeCount

    # Return the sum of all the keywords identified in a single form
    return(keyCount)