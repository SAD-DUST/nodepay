import requests
import json
import time

req = requests.Session()
token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzQyNjAzNzksInR5cGUiOiJhY2Nlc3MiLCJpYXQiOjE3MzQxNzM5NzksImF1ZCI6InRnLmFpLmpvYnMiLCJpc3MiOiJ0Zy5haS5qb2JzIiwic3ViIjoiNzIxODQ2NDk1NyIsImp0aSI6IjQwbmwxcW00bzJldWxrIn0.zkWfhk4M7PZ5MwmBhszzhfhIkFUlqyo1M38ffhq3TNnMa5_nRz7WN7ZjeVvVmoQjYuXY-E4r7-u55XtamRlvfaTXk8bvKwQdPtJlrEQ6EV8YOTx35GE1TwK1-MOz24KmJjppnvfS379ZFgEDihaAKWB44nEWfYxriDhvaPi6YWoWNFT0mw65eBPhJdw5ne-cD79JivN8HSXAFtX-oQur6x42SLuLS6PPX4edtDMSAM2P1W8rzExn9Jcm4ur5OM6LSgyg725-hpHG6SoxLyVE4XQCplkRlqBFWIaDoAJnLcKnDv0S5AwkuzucnS7JkTxJ5mvLMIZczBCPUGnwH_VX9xspmQ4xhDxBD6VLJ1j9QZOl_1Inh56yQ4b7JB_o1Vk5Opn62Imb5bkWVuhsSevx2aTAo3LLnEhZAkBXEUPYsvPCVFSj3wKDkIB8oJoLR4Ox3LIbpHnke1LrHPAL_39Qp7D9z-C1gmOyPdNXoxTbyrB19mhja1LOgxyGsXWdSmw3U7N_Kctgl5113UoaJYB2_ria9GjLsx-8XagEPPj0bw_YV7LDQ3o0mPzi5UMbazTVjU1sdQygs_qgmE5DZ31-2xDCIfNmgyHAVvIfh_Qr6fRMR3ApBQ9f4Sz-v_tlsTDuwxpRTmELBqqR4WBHPyVuBul0c-Q7CNEHcbIqq5FRznA"

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
