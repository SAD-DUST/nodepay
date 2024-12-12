import requests
import json
import time

req = requests.Session()
token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzQxMDY1MzQsInR5cGUiOiJhY2Nlc3MiLCJpYXQiOjE3MzQwMjAxMzQsImF1ZCI6InRnLmFpLmpvYnMiLCJpc3MiOiJ0Zy5haS5qb2JzIiwic3ViIjoiNzIxODQ2NDk1NyIsImp0aSI6ImE1ZmVwanJtNGxpdGVqeSJ9.NRqcmSzilZJBPIPZo0uYGgCmO_Jm35PEjm-tBp2-4_3IJCrRhxRddvpj1S8pWYDCpoA0qcbSoQ0BcC4sWhCMAf0-zk_j0nIOqUO9bLkBEVE5DcsTsUlfwgotnqJd3xaLHtqEXnoH2Iaaio68ztMeZm-Ftf7BgKFDfgaaJFsBxQXFAzGxrhucmgKSWUofJfAft2MHqnulMYD4UD4YFs7DXxll0UvfZwESAVXQCjK4-NUJDE23p1m_869MtIEeRwhOr0fbPokRTNBdCCU3sqWIXwzP_3x6OrXYMOdzJo0VuJgj066s8SAFwdilb-mSmV_3xDoIIv43Zd40DOY8W7Bh_iWuKwH2UKX7uMgNqZ5AKm_R2oNB8JPit_oNPDjB4Mntuv0KuLL0K5hNCIAspIiiYOptUsJGmLka_PxnTmtDGTuFR1JuAU6XicX2Zf3u1q0P1WcC1U3cRUDinqCSGpSP5phPEr1tEf9fRsYK5KcZAT_MB497uURoVahBJN4HUutrwMH7QrGqL3SiTF4dGL1n5QM8h4HixThbJh4zRualTHuqf-goN2HtKo4yRJJUeaHFU5hgt1eifb98fv36tJZ-lpBayHK93FVC2KFdjaHk8wWU8ATlvTLUlFy_O0eGA8MhYXtvOMFOIR6jk_MLsgRUFeD-9sPA5PkwhRc4msAVkqs"

headers = {
    "accept": "/",
    "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
    "authorization": token,
    "Content-Type": "application/json",
    "Origin": "https://tg-tap-miniapp.laborx.io",
    "Referer": "https://tg-tap-miniapp.laborx.io/",
    "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\"",
    "Sec-Ch-Ua-Mobile": "?1",
    "Sec-Ch-Ua-Platform": "\"ANDROID\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "sec-gpc": "1",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
}

def get_balance_info():
    try:
        response = req.get("https://tg-bot-tap.laborx.io/api/v1/farming/info", headers=headers)
        data = response.json()
        balance = data.get("balance")
        active_farm = data.get("activeFarmingStartedAt")
        print("Balance: " + str(balance))
    except requests.RequestException as error:
        print("Error getting farming info:", error)

def start_farming():
    try:
        response = req.post("https://tg-bot-tap.laborx.io/api/v1/farming/start", headers=headers, data={})
        if response.status_code == 200:
            print("Started Farming")
    except requests.RequestException as e:
        print("Error starting farming:", e)

def finish_farming():
    try:
        response = req.post("https://tg-bot-tap.laborx.io/api/v1/farming/finish", headers=headers, data={})
        if response.status_code == 200:
            print("Finished Farming")
            time.sleep(3)
            start_farming()
    except requests.RequestException as e:
        print("Error finishing farming:", e)

def get_id_task():
    url = "https://tg-bot-tap.laborx.io/api/v1/tasks/"
    try:
        response_tasks = req.get(url, headers=headers)
        response_data_tasks = response_tasks.json()
        ids = [item["id"] for item in response_data_tasks]
        titles = [item["title"] for item in response_data_tasks]
        return ids, titles
    except requests.RequestException as error:
        print("Error getting farming info:", error)

def complete_task():
    try:
        ids, titles = get_id_task()
        for id_task, title in zip(ids, titles):
            url = "https://tg-bot-tap.laborx.io/api/v1/tasks/{}/submissions".format(id_task)
            response = req.post(url, headers=headers).json()
            if 'OK' in response:
                print("Bypass => " + title)
                print(response)
                time.sleep(1)
            else:
                print("Already submitted => " + title)
    except requests.RequestException as error:
        print("Error completing task:", error)

def claim_task():
    complete_task()
    ids, titles = get_id_task()
    try:
        for id_task, title in zip(ids, titles):
            response = req.get("https://tg-bot-tap.laborx.io/api/v1/tasks/{}".format(id_task), headers=headers)
            task = response.json()
            if not task.get("submission") or task.get("submission").get("status") == "REJECTED":
                response = req.post("https://tg-bot-tap.laborx.io/api/v1/tasks/{}/submissions".format(id_task), headers=headers)
                print("Successfully submitted task : " + title)
                time.sleep(1)
            elif task.get("submission").get("status") == "SUBMITTED":
                print("cannot be claimed yet " + " => " +  title)
            elif task.get("submission").get("status") == "COMPLETED":
                response = req.post("https://tg-bot-tap.laborx.io/api/v1/tasks/{}/claims".format(id_task), headers=headers)
                print("Successfully claimed task" + " => " +  title)
                time.sleep(1)
            elif task.get("submission").get("status") == "CLAIMED":
                print("already claimed" + " => " +  title)
            if task.get("submission") and task.get("submission").get("status") != "CLAIMED":
                all_claimed = False
        if all_claimed:
            print("All tasks have been completed")
    except requests.RequestException as error:
        print("Error processing tasks:", error)

if __name__ == "__main__":
    while True:
        get_balance_info()
        finish_farming()
        claim_task()
        print("\nWaiting 1 hour before starting again...")
        get_balance_info()
        time.sleep(60 * 60)
