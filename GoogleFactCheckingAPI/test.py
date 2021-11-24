import pandas as pd
from GoogleFactCheckingAPI import GoogleFactCheckingAPI
from urllib.parse import urlparse

GF = GoogleFactCheckingAPI(api_key='AIzaSyBRV-U_rPYmjo9oHSEw1wtkKEy1xkvCnHE')
poynter = pd.read_csv('./dataset/poynter.csv')
global GoogleClaims
GoogleClaims = []
LogError = []
match = 0
notMatch = 0


def getGoogleFactCheck(item):
    q = item['checked_link']
    claims = []

    res = GF.search(params={
        'query': q,
    })

    try:
        claims = res["claims"]
    except:
        pass

    if(len(claims) < 1):
        GoogleClaims.append({
            'id': item['id'],
            'title': '',
            'text': '',
            'claimDate': '',
            'reviewDate': '',
            'claimant': '',
            'publisher': '',
            'url': '',
            'label': '',
            'found': 9,
            'query': q,
            'poynter_date': item['date']
        })

    for claim in claims:
        GoogleClaim = {
            'id': item['id'],
            'title': '',
            'text': '',
            'claimDate': '',
            'reviewDate': '',
            'claimant': '',
            'publisher': '',
            'url': '',
            'label': '',
            'found': 9,
            'query': q,
            'poynter_date': item['date']
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
            a_url = urlparse(GoogleClaim['url'])
            b_url = urlparse(q)

            if(a_url.netloc == b_url.netloc):
                GoogleClaim['found'] = 1
                match = match + 1
            else:
                GoogleClaim['found'] = 0
                notMatch = notMatch + 1

            print(str(match)+' matches')
            print(str(notMatch)+' not matched')
        except:
            pass

        GoogleClaims.append(GoogleClaim)


poynter_dict = poynter.to_dict('records')
progress = 0

for row in poynter_dict:
    try:
        progress += 1
        print(str(progress)+' / '+str(len(poynter_dict)))
        getGoogleFactCheck(row)
    except Exception as e:
        print('\n')
        print(str(progress)+' / '+str(len(poynter_dict)))
        print('Error: '+str(e))
        print(row['checked_link'])
        print('\n')
        LogError.append({
            'url': row['checked_link'],
            'error': e
        })

df = pd.DataFrame(GoogleClaims)
df.to_csv('./dataset/GoogleClaims5.csv')

log_df = pd.DataFrame(LogError)
log_df.to_csv('./dataset/log_error5.csv')
