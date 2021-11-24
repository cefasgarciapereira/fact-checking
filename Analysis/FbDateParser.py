import datetime
import json
import re

class FbDateParser:

    def abbreviateMonth(self, string_date):
        # convert the month name to 3 first letter
        abbreviated = str(string_date).replace('january', 'jan')
        abbreviated = str(abbreviated).replace('february', 'feb')
        abbreviated = str(abbreviated).replace('march', 'mar')
        abbreviated = str(abbreviated).replace('april', 'apr')
        abbreviated = str(abbreviated).replace('may', 'may')
        abbreviated = str(abbreviated).replace('june', 'jun')
        abbreviated = str(abbreviated).replace('july', 'jul')
        abbreviated = str(abbreviated).replace('august', 'aug')
        abbreviated = str(abbreviated).replace('september', 'sep')
        abbreviated = str(abbreviated).replace('october', 'oct')
        abbreviated = str(abbreviated).replace('november', 'nov')
        abbreviated = str(abbreviated).replace('december', 'dec')
        return abbreviated

    def removeTime(self, string_date):
        # removes the `at 18:00 am` part of the date
        response = re.sub(
            r"([0-1]?[0-9]|2[0-3]):[0-5][0-9]", '', str(string_date))
        response = response.replace('at ', '')
        response = response.replace('am ', '')
        response = response.replace('pm ', '')

        response = response.replace('at', '')
        response = response.replace('am', '')
        response = response.replace('pm', '')
        return response

    def monthToNum(self, string_date):
        # convert the abbreviated date to its correspondent number
        response = str(string_date).replace('jan', '01')
        response = str(response).replace('feb', '02')
        response = str(response).replace('mar', '03')
        response = str(response).replace('apr', '04')
        response = str(response).replace('may', '05')
        response = str(response).replace('jun', '06')
        response = str(response).replace('jul', '07')
        response = str(response).replace('aug', '08')
        response = str(response).replace('sep', '09')
        response = str(response).replace('oct', '10')
        response = str(response).replace('nov', '11')
        response = str(response).replace('dec', '12')
        return response

    def parseYYYYmmdd(self, date, poynter_date):
        # format the date YYYY/mm/dd
        if (("2020" not in str(date)) and ("2021" not in str(date)) and ("2019" not in str(date))) and (len(str(date)) > 1):
            date = str(date)+'/'+poynter_date.split('-')[0]
        
        date_arr = date.split('/')
        month = date_arr[0]
        day = date_arr[1]
        year = date_arr[2]

        def hzero(num):
            num = int(num)
            if num < 10:
                return '0'+str(num)
            else:
                return str(num)

        if str(year) == '':
            year = '2020'

        return str(year)+'-'+str(hzero(month))+'-'+str(hzero(day))

    def parse(self, fb_date, poynter_date):
        # starts the whole process of parsing the date
        lower_date = str(fb_date).lower()
        abbreviated_date = self.abbreviateMonth(lower_date)
        date_wo_time = self.removeTime(abbreviated_date)
        date_num = self.monthToNum(date_wo_time)
        date_num = date_num.replace('  ', '/')
        date_num = date_num.replace(' ', '/')

        try:
            date_num = date_num[:-1] if str(date_num)[-1] == '/' else date_num
        except:
            pass

        try:
            date_num = self.parseYYYYmmdd(date_num, poynter_date)
        except:
            pass

        return date_num
