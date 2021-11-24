from FaceBot import FaceBot
import pandas as pd
import math
import secrets
import pprint
import json
import os
import time

file_number = '1'
#INPUT_NAME = './poynter_social/poynter_social_false_'+file_number+'.json'
INPUT_NAME = './inputs/Archive/poynter_social_false_archive.json'
LOG_FILE = './outputs/Archive/facebook_false_archive_'+str(file_number)+'.log'
FILE_NAME = './outputs/Archive/output_facebook_false_archive_'+file_number+'.json'

def extract_ids_from_file():
    facebook_posts = pd.read_csv(INPUT_NAME)
    fb_ids = facebook_posts.filter(regex='^facebook_ids',axis=1)
    
    values=[]
    ids=[]
    errors = 0
    posts = 0
    
    for value in fb_ids.values.tolist():
        values += value
    
    for value in values:
        try:
            if((not math.isnan(float(value))) and (len(str(value)) > 5)):
                posts = posts+1
                ids.append(value)
            else:
                errors = errors + 1
        except:
            errors = errors + 1
            pass
    print('--- Extraction ---')
    print('Total values: '+str(errors+posts))
    print('Errors: '+str(errors))
    print('Post IDs: '+str(posts))
    return ids

def extract_ids_from_file_archive():
    facebook_posts = pd.read_csv(INPUT_NAME)
    fb_ids = facebook_posts['facebook']
    ids =[] 

    for fb_id in fb_ids:
        try:
            if((not math.isnan(float(fb_id))) and (len(str(fb_id)) > 5)):
                ids.append(fb_id)
        except:
            pass
    return ids

def create_file(name):
    f = open(name,'w')
    f.write('[')
    return f

def end_file(name, f):
    f.write(']')
    f.close()

def remove_duplicates(x):
    return list(dict.fromkeys(x))

def main_deprecated():
    #main
    #post_ids = ['331066071302214', '3117158961628521', '3295830967146135', '4010125388999766', '106631084293442', '1203940519963756']
    post_ids = remove_duplicates(extract_ids_from_file_archive())
    facebot = FaceBot(secrets.username, 
                        secrets.password, 
                        log=True, 
                        headless=True)
    f = create_file(FILE_NAME)
    n_posts = 0
    start_global_time = time.time()
    for post_id in post_ids:
        n_posts = n_posts + 1
        start_iteration_time = time.time()
        is_valid = facebot.navigate_to_post(post_id)
        response = facebot.post_info(is_valid=is_valid)
        pprint.pprint(response)
        json.dump(response, f)
        f.write(',')
        print('File '+file_number)
        print('Progress: ['+str(n_posts)+'/'+str(len(post_ids))+'] - Last Iteration: '+str(round(time.time() - start_iteration_time, 2))+'s - Total Time: '+str(round(time.time() - start_global_time, 2))+'s')

    end_file(FILE_NAME, f)
    facebot.close()

def main():
    with open(INPUT_NAME) as json_file:
        data = json.load(json_file)

    facebot = FaceBot(secrets.username, 
                secrets.password, 
                log=True, 
                headless=True)
    f = create_file(FILE_NAME)
    log = create_file(LOG_FILE)
    errors = 0
    n_posts = 0
    total_posts = 0
    start_global_time = time.time()
    
    for item in data:
        for fb_id in item['facebook_ids']:
            fb_id = fb_id.replace('_','')
            try:
                if((not math.isnan(float(fb_id))) and (len(str(fb_id)) > 5)):
                    total_posts = total_posts + 1
            except:
                pass

    for item in data:
        start_iteration_time = time.time()
        for fb_id in item['facebook_ids']:
            fb_id = fb_id.replace('_','')
            try:
                if((not math.isnan(float(fb_id))) and (len(str(fb_id)) > 5)):
                    is_valid = facebot.navigate_to_post(fb_id)
                    response = facebot.post_info(is_valid=is_valid, df=item, append_df=True)
                    pprint.pprint(response)
                    json.dump(response, f)
                    f.write(',')
                    n_posts = n_posts + 1
                    print('File '+file_number)
                    print('Progress: ['+str(n_posts)+'/'+str(total_posts)+'] - Last Iteration: '+str(round(time.time() - start_iteration_time, 2))+'s - Total Time: '+str(round(time.time() - start_global_time, 2))+'s')
            except Exception as e:
                errors = errors + 1
                log.write('\n'+str(e))
                pass
    log.write('\nTotal Errors: '+str(errors))
    end_file(FILE_NAME, f)
    end_file(LOG_FILE, log)
    facebot.close()

main()