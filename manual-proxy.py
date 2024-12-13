import requests
import json
import time

req = requests.Session()
token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzQyMTgzNDgsInR5cGUiOiJhY2Nlc3MiLCJpYXQiOjE3MzQxMzE5NDgsImF1ZCI6InRnLmFpLmpvYnMiLCJpc3MiOiJ0Zy5haS5qb2JzIiwic3ViIjoiNzIxODQ2NDk1NyIsImp0aSI6IjQwbmwxeG00bmRkemUxIn0.lK5f69RJk7mQ12ew3UWzlU-SwmwbGUveiTNn_J7Ls4X5FA00bdC4v85xCpRWiCvxAwLGYDij6S95ARYxsht3ppSXHNj_8SLrelG2Zf49TR84PW1UK066wniBQCkv0hK3rkMO18uy0ea33nkOmmG6YQaLyluUDxdkeeLBr-QZJueRXDyBRoXMw7VR5c7BNR3DgYY6zAiCdBMGobAnCLgtKm66HgQW9T0JbJtjpz1xEfOHziNtd1ltTABAx2PHCkPtC0y_hCPx8_c3zmL7MME9rZwDRK5SMs9xJ6WxppOIpwRhnzWm2VYYXbHXqLt8bxTp2EO_uJKKpp0sS8WWudT5U3lpPt840IH6DIDANbvmTM13BCDNcJ5xT4UQe_i3p82qq6uu95fKfdkwAJF7JTWRYSDEdQG9sYIrh1Xupdt1AuhHXTq8OYBSYzXH0ZeMhZrIHL5Gh5ZmfcUEI0RkE9dtG5YnvhPZAN4yHByWCbY6iSZA7mXvS61OIOMo2kFAapzZhWfFbKhVGXf4dSM0Wl3jdoe1EP1YWVhtKFaRxstaWuaouJBqUvrTmvRi3aZX47j40kArvnEcsKdqIr8gvjdNZ1-FLREzSB1XdD5U4OY-U51ZWxBntkwz3ZuoiE4CakhxsJhl9-SsutrL0T81yRur5wu0BLrwx8bOriAiZrZ1_lY"

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
