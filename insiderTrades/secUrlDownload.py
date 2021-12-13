
import requests
import pandas as pd
import numpy as np
import io
import re

def secUrlDownload(quarter, year, form, name, email):
    """
    pulls a list of url's to text files for form 4 and form 5 filings
    Paramters:
        quarter (int): integar with valid options being 1 to 4
        year (int): integer with valid options being 2004 to present
        form (int): integar with valid options being 4 or 5
        name (string): string consisting of the user's name for database access purposes
        email (string): string consisting of the user's email for database access purposes
    Returns:
        dat2 (DataFrame): DataFrame containing form type and URL of the filing
    """

    # Convert inputs that could be integers to strings
    quarter = str(quarter)
    year = str(year)
    form = str(form)

    # Grab the .idx file with all of the potential URLs
    targetUrl = 'https://www.sec.gov/Archives/edgar/full-index/' + year + '/QTR' + quarter + '/form.idx'
    headers = {'user-agent': str(name + ' ' + email)}
    
    response = requests.get(targetUrl, headers=headers, allow_redirects = True).content
    dat = pd.read_csv(io.StringIO(response.decode('utf-8')), sep='\t', skiprows=10, names = ['text dump'])

    # Create final dataframe through regex
    dat1 = pd.DataFrame(index=np.arange(len(dat)), columns = ['Form Type', 'Url'])
    dat1['Form Type'] = dat['text dump'].apply(lambda x: re.search('(.*?)\s\s', x)[0].replace(" ", ""))
    dat1['Url'] = dat['text dump'].apply(lambda x: re.search('edgar/.*', x)[0].replace(" ", ""))    
    dat1['Url'] = 'https://www.sec.gov/Archives/' + dat1['Url']

    # Keep only observations that are Form 4 or 5
    dat2 = dat1[dat1['Form Type'] == form]
    return(dat2['Url'].reset_index(drop = True))
