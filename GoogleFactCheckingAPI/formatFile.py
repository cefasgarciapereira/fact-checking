import pandas as pd

poynter = pd.read_csv('./dataset/poynter.csv')
google = pd.read_csv('./dataset/GoogleClaims.csv')
counter = 0
new_google = []

for poynter_row in poynter.to_dict('records'):
    counter = counter + 1
    print(counter)
    for google_row in google.to_dict('records'):
        if(google_row['query'] == poynter_row['checked_link']):
            google_row['poynter_date'] = poynter_row['date']
            new_google.append(google_row)
            break

new_google = pd.DataFrame(new_google)
new_google.to_csv('./dataset/GoogleClaimsByUrl.csv')