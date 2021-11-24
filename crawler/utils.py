facebookRegex = "(?:(?:http|https):\/\/)?(?:www.)?facebook.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[?\w\-]*\/)?(?:profile.php\?id=(?=\d.*))?([\w\-]*)?"
facebook_url_filter = ["https://www.facebook.com/help/publisher/"]
facebook_id_regex = "/(?:https?:\/\/(?:www|m|mbasic|business)\.(?:facebook|fb)\.com\/)(?:photo(?:\.php|s)|permalink\.php|video\.php|media|watch\/|questions|notes|[^\/]+\/(?:activity|posts|videos|photos))[\/?](?:fbid=|story_fbid=|id=|b=|v=|)(?|([0-9]+)|[^\/]+\/(\d+))/g"

twitterRegex = "/(?:http:\/\/)?(?:www\.)?twitter\.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[\w\-]*\/)*([\w\-]*)/"
twitter_id_filter = ["tweet", "", "compose", "&via=Newtral, Coronavirus, COVID19, lupus, coronavirus"]