import json

none = 0
twitter = 0
facebook = 0
both = 0
archive = 0


with open('./Poynter/poynter_social_false.json') as json_file:
    poynter = json.load(json_file)
    for new in poynter:
        social_media = new['social_medias']
        archives = new['archive_links']
        if social_media == 0:
            if(len(archives) > 0):
                archive = archive + 1
            else:
                none = none + 1
        elif social_media == 1:
            twitter = twitter + 1
        elif social_media == 2:
            facebook = facebook + 1
        elif social_media == 3:
            both = both + 1
        else:
            print(social_media)
            
print('Nenhum: ', none)
print('Twitter: ', twitter)
print('Facebook: ', facebook)
print('Archive: ', archive)
print('Both: ', both)
