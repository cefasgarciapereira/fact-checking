urls = []
for page in range(1, 8):
    url = 'https://www.poynter.org/ifcn-covid-19-misinformation/page/'+str(page)+'/?covid_countries=47364&covid_rating=0&covid_fact_checkers=0#038;covid_rating=0&covid_fact_checkers=0'
    urls.append(url)
print(urls)