import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import random
from tqdm import tqdm
import json
from overview import Data

rand_pages = [
    "https://www.sololearn.com/{lang}",
    "https://www.sololearn.com/{lang}",
    "https://www.sololearn.com/{lang}/profile/{random-profile}",
    "https://www.sololearn.com/{lang}/profile/{random-profile}",
    "https://www.sololearn.com/{lang}/profile/{random-profile}",
    "https://www.sololearn.com/{lang}/profile/{random-profile}",
    "https://www.sololearn.com/{lang}/profile/{random-profile}",
    #"https://www.sololearn.com/{lang}/profile/{random-profile}",
    #"https://www.sololearn.com/{lang}/profile/{random-profile}",
    #"https://www.sololearn.com/{lang}/profile/{random-profile}",
    "https://www.sololearn.com/{lang}/profile/{brentspine-profile}",
    "https://www.sololearn.com/{lang}/learn",
    "https://www.sololearn.com/{lang}/learn/courses/web-development",
    "https://www.sololearn.com/{lang}/learn/courses/python-developer",
    "https://www.sololearn.com/{lang}/learn/courses/coding-foundations",
    "https://www.sololearn.com/{lang}/learn/courses/data-programming",
    "https://www.sololearn.com/{lang}/learn/courses/angular-developer",
    "https://www.sololearn.com/{lang}/learn/courses/genai-in-practice",
    "https://www.sololearn.com/{lang}/learn/language/java",
    "https://www.sololearn.com/{lang}/learn/language/python",
    "https://www.sololearn.com/{lang}/learn/language/javascript",
    "https://www.sololearn.com/{lang}/learn/language/html",
    "https://www.sololearn.com/{lang}/learn/language/css",
    "https://www.sololearn.com/{lang}/learn/language/sql",
    "https://www.sololearn.com/{lang}/learn/language/php",
    "https://www.sololearn.com/{lang}/compiler-playground",
    "https://www.sololearn.com/{lang}/discuss",
    "https://www.sololearn.com/{lang}/teams",
    "https://www.sololearn.com/{lang}/payments/pro"
    "https://www.sololearn.com/{lang}/{rand-chars}",
    "https://www.sololearn.com/{lang}/{rand-chars}",
    #"https://www.sololearn.com/{lang}/{rand-chars}",
    "https://www.sololearn.com/{rand-chars}",
    "https://www.sololearn.com/{rand-chars}",
    #"https://www.sololearn.com/{rand-chars}",
    "https://www.sololearn.com/{rand-chars}/{lang}",
    #"https://www.sololearn.com/{rand-chars}/{lang}",
    "https://www.sololearn.com/{rand-chars}/{rand-chars}",
]

rand_langs = [
    "de",
    "de",
    "en",
    "en",
    "en",
    "en",
    "en",
    "en",
    "en",
    "en",
    "es",
    "pt",
    "fr",
    "ru"
]

def on_exit():
    print("Exiting ...")
    exit()

nchars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def change_pfp(driver, access_token, refresh_token, expires_at, cloudflare_xd=None, user_id=None, profile_picture_url=None, profile_picture_type=None):
    if user_id == None:
        user_id = driver.execute_script("""return localStorage.getItem("userID").toString()""")
        print("User ID: " + user_id)
    if profile_picture_url == None:
        profile_picture_url = driver.execute_script("""return JSON.parse(localStorage.getItem("botUser"))["profile_picture_url"]""")
        print("Profile Picture URL: " + profile_picture_url)
    if profile_picture_type == None:
        profile_picture_type = driver.execute_script("""return JSON.parse(localStorage.getItem("botUser"))["profile_picture_type"]""")
        print("Profile Picture Type: " + profile_picture_type)
    driver.get("https://www.sololearn.com/en/profile/" + str(user_id))
    time.sleep(1)
    driver.execute_script("""localStorage.setItem("accessToken", JSON.stringify({"data": '""" + access_token + """'}))""")
    driver.execute_script("""localStorage.setItem("refreshToken", JSON.stringify({"data": '""" + refresh_token + """'}))""")
    driver.execute_script("""localStorage.setItem("expiresIn", JSON.stringify({"data": '""" + str(expires_at) + """'}))""")
    # Set the cookie __cf_bm using driver.execute_script
    if cloudflare_xd != None:
        driver.add_cookie(cloudflare_xd)
        time.sleep(1)
    with open("sololearn_pfp.js", "r") as file:
        script_content = file.read()
    driver.execute_script(script_content.replace("%%profile_picture_url%%", profile_picture_url).replace("%%profile_picture_type%%", profile_picture_type).replace("%%auth%%", access_token))
    
full_data = Data.load_data()

custom_bio = "DM @kathie.hcg on Instagram: Boost your portfolio easily! Cheap SoloLearn Followers! Numbers matter, let's help eachother 🚀🚀🚀"

def do_follow(auth):
    print("do_follow called")
    max_follow = full_data["max_follows_per_user"]
    random_follows = 10
    print("Max follow: " + str(max_follow))
    print("Random follows: " + str(random_follows))
    x = []
    i = -1
    for c in full_data["paid"]:
        i += 1
        if c["amount_done"] >= c["amount_do"]:
            continue
        x.append(c)
        full_data["paid"][i]["amount_done"] += 1
        if len(x) >= max_follow:
            break
    if len(x) < max_follow:
        i = -1
        for c in full_data["advertise"]:
            i += 1
            if c["amount_done"] >= c["amount_do"]:
                continue
            x.append(c)
            full_data["advertise"][i]["amount_done"] += 1
            if len(x) >= max_follow:
                break
    for i in range(random_follows):
        x.append({"id": 30000000+random.randint(0,150000), "amount_done": -1, "amount_do": -1})
    print(f"Determined {len(x)} accounts to follow")
    while(len(x) < max_follow):
        # If the amount of accounts to follow is less than max_follow, skip or there will be an infinite loop.
        if (len(full_data["paid"]) + len(full_data["advertise"])) < max_follow:
            break
        # Add random, check if it exists. 
        c = random.choice(full_data["paid"] + full_data["advertise"])
        #if c["amount_done"] >= c["amount_do"]:
            #continue
        # Add amount_done
        full_data["paid" if c in full_data["paid"] else "advertise"][full_data["paid" if c in full_data["paid"] else "advertise"].index(c)]["amount_done"] += 1
        x.append(c)
    print(f"Final amount of accounts to follow: {len(x)}")
    print("Saving data ... (Updated follow these for saved users)")
    Data.save_data(full_data)
    follow_these = "["
    for c in x[:-1]:
        follow_these += "'" + str(c["id"]) + "',"
    follow_these += "'" + str(x[len(x)-1]["id"]) + "']"
    # print("Follow these: " + follow_these)
    print("Going to API2 ...")
    driver.get("https://api2.sololearn.com/")
    time.sleep(3)
    with open(r'sololearn_bot_script.txt', 'r') as file:
        script_content = file.read()
    # !!! "use_username" or "use_first_last" or custom name
    # UNCOMMENT for use | bot_name = random.choice(full_data["bot_names"])
    # UNCOMMENT for use | bot_name = "use_username"
    bot_name = "use_first_last"
    print("Bot name: " + bot_name)
    print("Injecting script ...")
    driver.execute_script(script_content.replace("%%auth%%", auth).replace("%%follow%%", follow_these).replace("%%bio%%", custom_bio).replace("%%ngrok%%", full_data["ngrok"]).replace("%%username%%", bot_name))
    print("Script injected ...")

for i in range(1000000):
    try:
        # Throw an exception (for testing)
        #raise Exception("Test")
        full_data = Data.load_data()
        if i % 2 == 0:
            if i != 0:
                print("Dumping webdriver")
                driver.quit()
            options = Options()
            options.add_argument("--start-maximized")
            options.add_argument("--auto-open-devtools-for-tabs");
            driver = webdriver.Firefox(options)
        url = random.choice(rand_pages).replace("{lang}", random.choice(rand_langs)).replace("{random-profile}", str(random.randint(50000000, 99999999))).replace("{brentspine-profile}", "32001493")
        # Replace each {rand-chars} with a random string of 3-12 characters
        rurl = ""
        parts = url.split("{rand-chars}")
        for c in parts[:-1]:
            rurl += c + "".join(random.choices(nchars, k=random.randint(6, 12)))
        rurl += parts[len(parts)-1]
        if random.randint(1, 4) == 1:
            rurl += "?ref=" + "".join(random.choices(nchars, k=random.randint(6, 12)))
        print("Using page link: " + rurl)
        driver.get(rurl)
        # Sleep 80 seconds or until localStorage.getItem("accessToken") is not null
        for i in tqdm(range(40)):
            time.sleep(2)
            #try:
            if driver.execute_script("""return localStorage.getItem("accessToken")""") != None:
                break
            #except Exception as e:
               # print("ERROR (Wait for public token):")
                #print(e)
        
        auth = driver.execute_script("""return JSON.parse(localStorage.getItem("accessToken"))["data"]""")
        refresh = driver.execute_script("""return JSON.parse(localStorage.getItem("refreshToken"))["data"]""")
        # Fetch expires_in and convert it into timestamp (Raw Data: 2024-05-13T17:11:19.947Z)
        expires_in = driver.execute_script("""return Date.parse(JSON.parse(localStorage.getItem("expiresIn"))["data"])""")
        # //1000, since it's in milliseconds
        Data.add_refresh_token(refresh, expires_in//1000, False, auth)
        print("Taken auth, length: " + str(len(auth)))
        
        time.sleep(1.5)
        
        for i in range(2):
            try:
                do_follow(auth)
                print("Executing follows...")
                time_for_follows = int(0 + (full_data["max_follows_per_user"] * 1)) + 5
                for i in tqdm(range(time_for_follows)):
                    time.sleep(1)
                access_token = driver.execute_script("""return localStorage.getItem("grabbedAccessToken")""")
                refresh_token = driver.execute_script("""return localStorage.getItem("grabbedRefreshToken")""")
                profile_picture_url = driver.execute_script("""return JSON.parse(localStorage.getItem("botUser"))["profile_picture_url"]""")
                profile_picture_type = driver.execute_script("""return JSON.parse(localStorage.getItem("botUser"))["profile_picture_type"]""")
                user_id = driver.execute_script("""return localStorage.getItem("userID").toString()""")
                # Converting into seconds
                expires_at = int(driver.execute_script("""return localStorage.getItem("grabbedExpiresAt")""")) // 1000
                Data.add_refresh_token(refresh_token, expires_at, True, access_token)
                print("=== Trying to change profile picture ===")
                change_pfp(driver, access_token, refresh_token, expires_at)
                time.sleep(10)
            except Exception as e:
                print("ERROR (In the loop after auth taken):")
                print(e)

        # driver.quit()
        # Clear localStorage 
        driver.execute_script("""localStorage.removeItem("accessToken")""")
        driver.execute_script("""localStorage.removeItem("refreshToken")""")
        driver.execute_script("""localStorage.removeItem("expiresIn")""")
        # time_till_next_session = random.randint(120, 280)
        full_data = Data.load_data()
        if full_data["exit_on_next_cycle"]:
            full_data["exit_on_next_cycle"] = False
            Data.save_data(full_data)
            print("Exiting (exit_on_next_cycle is set to True) ...")
            on_exit()
        time_till_next_session = 2
        print("Waiting " + str(time_till_next_session) + "s ...")
        for i in tqdm(range(time_till_next_session)):
            time.sleep(1)

        print("Waiting some more time for the rate limit of 1m")
        time.sleep(14)
    except KeyboardInterrupt:
        on_exit()
        pass
    except Exception as e:
        print("ERROR:")
        print("Couldn't parse access token")
        driver.quit()
        time_till_next_session = random.randint(60*15, 60*30)
        #print("Waiting " + str(time_till_next_session) + "s ...")
        #for i in tqdm(range(time_till_next_session)):
            #time.sleep(1)
        tokens = Data.get_refresh_token_data()
        new_tokens_public = []
        tokens_to_refresh = []
        print("=== Token Stats ===")
        print("Public Tokens: " + str(len(tokens["public"])))
        print("Account Tokens: " + str(len(tokens["users"])))
        print("")
        for c in tokens["public"]:
            try:
                print(c)
                if c["expires_at"] < time.time():
                    tokens_to_refresh.append(c["token"])
                else:
                    new_tokens_public.append(c)
            except Exception as e:
                print("ERROR append token:")
                print(e)
                
        # Maximum 5
        for c in tokens_to_refresh[5:]:
            new_tokens_public.append(c)
        tokens_to_refresh = tokens_to_refresh[:5]
        do_wait_at_end = len(tokens_to_refresh) < 4
        # do_wait_at_end = False
        print(f"Trying to refresh {len(tokens_to_refresh)} tokens ...")
        driver = webdriver.Firefox()
        driver.get("https://api2.sololearn.com/")
        time.sleep(3)
        with open(r'sololearn_bot_refresh.js', 'r') as file:
            script_content = file.read()
        driver.execute_script(script_content.replace("%%tokens_to_refresh%%", str(tokens_to_refresh)))
        time.sleep(len(tokens_to_refresh) * 1.5 + 1.5)
        refreshed_tokens = driver.execute_script("""return JSON.parse(localStorage.getItem('refreshed_tokens'))""")
                    # {
            #   "{old_refresh_token}": {"access_token": "{new_access_token}", "refresh_token": "{new_refresh_token}", "expires_at": {new_expires_at}}
            # }
        print(refreshed_tokens)
        for c in refreshed_tokens.keys():
            new_tokens_public.append({"token": refreshed_tokens[c]["refreshToken"], "expires_at": time.time() + 3600, "access_token": refreshed_tokens[c]["accessToken"]})
        tokens["public"] = new_tokens_public
        with open("refresh_tokens.json", "w") as file:
            json.dump(tokens, file)
        time.sleep(1)
        driver.refresh()
        driver.execute_script("""localStorage.removeItem('refreshed_tokens')""")
        for c in refreshed_tokens.keys():
            do_follow(refreshed_tokens[c]["accessToken"])
            time.sleep(10)
            four_two_nine = driver.execute_script("""return JSON.stringify(localStorage.getItem("encountered_429"))""")
            if four_two_nine == "true":
                print("Encountered 429, using next token...")
                continue
            else:
                print("Signup successful, proceeding ...")
            time_to_wait = (full_data["max_follows_per_user"] * 1) - 5
            time_to_wait = 1 if time_to_wait < 1 else time_to_wait
            print("Executing follows (Recycled Tokens) ...")
            for i in tqdm(range(time_to_wait)):
                time.sleep(1)
            cloudflare_xd = driver.get_cookie("__cf_bm")
            print("__cf_bm: " + str(cloudflare_xd))
            access_token = refreshed_tokens[c]["accessToken"]
            refresh_token = refreshed_tokens[c]["refreshToken"]
            print("=== Trying to change profile picture (Recycled Tokens) ===")
            # UNCOMMENT FOR USE (currently doesn't work) | 
            change_pfp(driver, access_token, refresh_token, refreshed_tokens[c]["expiresIn"])
            time.sleep(10)

        driver.quit()
        if do_wait_at_end:
            for i in tqdm(range(60*15)):
                time.sleep(1)
