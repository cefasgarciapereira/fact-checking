import urllib.request
import json


class GoogleFactCheckingAPI:

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://factchecktools.googleapis.com/v1alpha1/claims:search?'

    def search(self, params):
        query_string = self.base_url+'key='+self.api_key

        try:
            query_string = query_string + '&query='+str(urllib.parse.quote(params['query']))
        except:
            pass

        try:
            query_string = query_string + '&languageCode='+str(params['languageCode'])
        except:
            pass

        try:
            query_string = query_string + '&reviewPublisherSiteFilter='+str(params['reviewPublisherSiteFilter'])
        except:
            pass

        try:
            query_string = query_string + '&maxAgeDays='+str(params['maxAgeDays'])
        except:
            pass

        try:
            query_string = query_string + '&pageSize='+str(params['pageSize'])
        except:
            pass

        try:
            query_string = query_string + '&pageToken='+str(params['pageToken'])
        except:
            pass

        try:
            query_string = query_string + '&offset='+str(params['offset'])
        except:
            pass

        with urllib.request.urlopen(query_string) as response:
            data = json.loads(response.read().decode())
            return data
