import botometer
import pandas as pd

# now it's called rapidapi key
#rapidapi_key = "c5128eb2dfmsh4737010bee85c87p1e905ejsn79e3e9ce1a2a" #cefas gmail 0 - 480
#rapidapi_key = "1f0e090ec4msh3b70522aa458fa3p134e2djsne77fd2d17bb9" #cefas facebook 480 - 980
#rapidapi_key = "e13cad9c1cmshc7be3163131eafbp1565bajsn6fd3da7b4a7a" #gregory 980 - 1480
#rapidapi_key = "4306a063bdmshf44062ad27c2a4bp189c55jsnbdc929ca07a9" #cefas trivento 1480 - 1980
rapidapi_key = "f96434e1f6mshdcba0bb8e073ba6p1e3f64jsn20b498d52620" #cefas easyquant 1980 - 2058

twitter_app_auth = {
    'consumer_key': 'cXrvEZXI1Xd7XtxGab3XtBKR2',
    'consumer_secret': 'RvZilUnat44X3FAD65oHj80Nz83BHIkztLG4CIxVYkTP516OeE'
}

bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

#read csv data and feed accounts array
df = pd.read_csv('tweet_out_screen_name.csv')
screen_names = list(df['screen_name'])
unique_screen_names = list(set(screen_names))
accounts = []

with open('users_bot_lvl3.csv', 'w', encoding='UTF8') as f:
    for name in unique_screen_names:
        accounts.append(str("@"+name))

# Check a sequence of accounts
results = []
prog = 1980
for screen_name, result in bom.check_accounts_in(accounts[1980:]):
    # Do stuff with `screen_name` and `result`
    try:
        results.append({
            "screen_name": screen_name,
            "en_astroturf": result['raw_scores']['english']['astroturf'],
            "en_fake_follower": result['raw_scores']['english']['fake_follower'],
            "en_financial": result['raw_scores']['english']['financial'],
            "en_other": result['raw_scores']['english']['other'],
            "en_overall": result['raw_scores']['english']['overall'],
            "en_self_declared": result['raw_scores']['english']['self_declared'],
            "en_spammer": result['raw_scores']['english']['spammer'],
            "astroturf": result['raw_scores']['universal']['astroturf'],
            "fake_follower": result['raw_scores']['universal']['fake_follower'],
            "financial": result['raw_scores']['universal']['financial'],
            "other": result['raw_scores']['universal']['other'],
            "overall": result['raw_scores']['universal']['overall'],
            "self_declared": result['raw_scores']['universal']['self_declared'],
            "spammer": result['raw_scores']['universal']['spammer'],
            "en_cap": result['cap']['english'],
            "universal_cap": result['cap']['universal']

        })
        results_df = pd.DataFrame(results)
        results_df.to_csv('botometer_1980.csv')
    except:
        pass
    prog = prog + 1
    print(str(prog)+" / "+str(len(accounts)))
