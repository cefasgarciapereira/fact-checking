# this code aims to compare results of fact check collected in Poynter to the ones
# contained in Google Fact Checking API
import pandas as pd

from GoogleFactCheckingAPI import GoogleFactCheckingAPI

def append_claim(claims=[], GoogleClaims=[], poynter_url='', poynter_title='', poynter_link=''):
    for claim in claims:
        GoogleClaim = {
            'title': '',
            'text': '',
            'claimDate': '',
            'reviewDate': '',
            'claimant': '',
            'publisher': '',
            'url': '',
            'label': '',
            'poynter': 9,
            'poynter_title': poynter_title,
            'poynter_link': poynter_link
        }

        try:
            GoogleClaim['title'] = claim['claimReview'][0]['title']
        except:
            pass

        try:
            GoogleClaim['text'] = claim['text']
        except:
            pass

        try:
            GoogleClaim['claimDate'] = claim['claimDate']
        except:
            pass

        try:
            GoogleClaim['reviewDate'] = claim['claimReview'][0]['reviewDate']
        except:
            pass

        try:
            GoogleClaim['claimant'] = claim['claimant']
        except:
            pass

        try:
            GoogleClaim['publisher'] = claim['claimReview'][0]['publisher']['name']
        except:
            pass

        try:
            GoogleClaim['url'] = claim['claimReview'][0]['url']
        except:
            pass

        try:
            GoogleClaim['label'] = claim['claimReview'][0]['textualRating']
        except:
            pass

        try:
            if(GoogleClaim['url'] == poynter_url):
                GoogleClaim['poynter'] = 1
            else:
                GoogleClaim['poynter'] = 0
        except:
            pass

        GoogleClaims.append(GoogleClaim)


GF = GoogleFactCheckingAPI(api_key='AIzaSyBRV-U_rPYmjo9oHSEw1wtkKEy1xkvCnHE')
poynter = pd.read_csv('./dataset/poynter.csv')
GoogleClaims = []
Log = []

for index, item in poynter.iterrows():
    try:
        res = GF.search(params={
            'query': str(item['checked_link']),
        })

        claims = res["claims"]
        append_claim(claims, GoogleClaims, poynter_url=str(item['checked_link']), poynter_title=str(item['title']), poynter_link=str(item['checked_link']))
        print(str(index)+'/'+'11724'+' ok')
        Log.append({
            'index': str(index),
            'status': 'ok'
            })
    except:
        print(str(index)+'/'+'11724'+' nok')
        Log.append({
            'index': str(index),
            'status': 'nok'
            })
        pass

df = pd.DataFrame(GoogleClaims)
df.to_csv('./dataset/GoogleClaims4.csv')

Log_df = pd.DataFrame(Log)
Log_df.to_csv('./dataset/logs4.csv')
