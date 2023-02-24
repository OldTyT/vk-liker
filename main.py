import os
import random
import time

import requests


def get_value_env(key: str, type_value: type):
    value = os.getenv(key)
    if value is None:
        print(f"Value is not set, key - {key}")
        exit(1)
    if type_value == str:
        return value
    if type_value == int:
        if not value.isdigit():
            print(f"Isn't int key - {key}, value - {value}")
            exit(1)
        return int(value)
    if type_value == list:
        if value.find(",") == -1:
            print(f"Comma not found in key - {key}. Value - {value}")
            exit(1)
        return value.split(",")
    exit(1)


API_VER = "5.131"
GROUP_ID = get_value_env("GROUP_ID", str)
TIME_SLEEP = get_value_env("TIME_SLEEP", int)
WALL_CNT = get_value_env("WALL_CNT", int)
VK_TOKENS = get_value_env("VK_TOKENS", list)


def load_accounts():
    count = 0
    accounts = {}
    for VK_TOKEN in VK_TOKENS:
        accounts.update({count: {"username": f"SOME_USERNAME{str(random.randint(0, 100))}",
                                 "password": f"SOME_PASSWORD{str(random.randint(0, 100))}",
                                 "access_token": VK_TOKEN}})
        count += 1
    like(accounts)


def get_latest_posts_from_group(access_token: str) -> dict:
    wall_get = requests.get(url="https://api.vk.com/method/wall.get", params={
        "owner_id": GROUP_ID,
        "count": WALL_CNT,
        "access_token": access_token,
        "v": API_VER})
    time.sleep(TIME_SLEEP)
    if wall_get.status_code != 200:
        return {"error": True}
    wall_get = wall_get.json()
    if 'error' in wall_get.keys():
        return {"error": True}
    if 'response' in wall_get.keys():
        print("Success wall get")
        like(wall_get)
        return wall_get
    return {"error": True}


def like(accounts: dict):
    for i in accounts:
        print(i)
        print(f"Use account - {i[:5]}...{i[-3:]}")
        if "access_token" in accounts[i].keys():
            if accounts[i]['access_token'] != '':
                last_posts = get_latest_posts_from_group(accounts[i]['access_token'])
                if "error" in last_posts:
                    continue
                print(f"Account - {accounts[i]['username']}")
                like_post(last_posts, accounts, i)


def like_post(last_posts: dict, accounts: dict, i):
    for e in last_posts['response']['items']:
        if e['likes']['user_likes'] == 0:
            user_pass = accounts[i]["username"] + accounts[i]["password"] + accounts[i]['access_token']
            my_rnd = len(user_pass) + int(str(e["id"]))
            if my_rnd % 2 == 0:
                if random.choice([True, False]):
                    like_add = requests.get(url="https://api.vk.com/method/wall.addLike", params={
                        "owner_id": GROUP_ID,
                        "post_id": e["id"],
                        "access_token": accounts[i]['access_token'],
                        "repost": True,
                        "v": API_VER})
                else:
                    like_add = requests.get(url="https://api.vk.com/method/wall.addLike", params={
                        "owner_id": GROUP_ID,
                        "post_id": e["id"],
                        "access_token": accounts[i]['access_token'],
                        "v": API_VER})
                like_add_js = like_add.json()
                print(like_add.text)
                print(like_add.status_code)
                time.sleep(TIME_SLEEP)
                if "error" in like_add_js:
                    return
            if my_rnd % 3 == 0:
                like_add = requests.get(url="https://api.vk.com/method/wall.addLike", params={
                    "owner_id": GROUP_ID,
                    "post_id": e["id"],
                    "access_token": accounts[i]['access_token'],
                    "v": API_VER})
                like_add_js = like_add.json()
                print(like_add.text)
                print(like_add.status_code)
                time.sleep(TIME_SLEEP)
                if "error" in like_add_js:
                    return


if __name__ == '__main__':
    while True:
        load_accounts()
        print(f"Sleep - {TIME_SLEEP}s.")
        time.sleep(TIME_SLEEP)
