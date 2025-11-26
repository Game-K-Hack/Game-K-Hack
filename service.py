import os
import requests
from fake_useragent import UserAgent
from dotenv import load_dotenv; load_dotenv()

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib.parse import urlsplit
import os.path


TRYHACKME_URL_PROFILE = "https://tryhackme.com/p/" + os.getenv("TRYHACKME_USERNAME")
ROOTME_URL_PROFILE = "https://www.root-me.org/" + os.getenv("ROOTME_USER")

def get_credly_badges() -> dict:
    print("[WAIT] get_credly_badges")
    def __request__(url) -> dict:
        return requests.get(url, headers={
                "User-Agent": UserAgent().firefox, 
                "Accept": "application/json"
            }
        ).json()
    
    data = []
    next_url = True

    url = f"https://www.credly.com/users/{os.getenv('CREDLY_ID')}/badges?page=1&page_size=48"

    while next_url:
        res = __request__(url)
        data += res["data"]
        url = res["metadata"]["next_page_url"]
        if url is None:
            next_url = False
            break

    print("[OK] get_credly_badges")
    return [{
        "name": elm["badge_template"]["name"], 
        "description": elm["badge_template"]["description"], 
        "level": elm["badge_template"]["level"], 
        "image": elm["badge_template"]["image_url"], 
        "issuer": elm["badge_template"]["issuer"]["summary"], 
        "url": "https://www.credly.com/earner/earned/badge/" + elm["id"]
    } for elm in data]

def get_rootme_stat() -> dict:
    print("[WAIT] get_rootme_stat")
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    print("[DEBUG] webdriver started")
    url = "https://www.root-me.org/" + os.getenv("ROOTME_USER") + "?lang=fr"
    driver.get(url)
    print("[DEBUG] webdriver go to url")

    try:
        # Attendre que l'élément #main soit présent dans le DOM
        main = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "main"))
        )
        # Attendre que le tableau soit chargé
        table_rows = main.find_elements(By.CSS_SELECTOR, "table tbody tr")
        print("[TRACE] len of table_rows:", str(len(table_rows)))

        if len(table_rows) >= 3:
            # Récupérer le lien dans la troisième ligne
            link_element = table_rows[2].find_element(By.CSS_SELECTOR, "a")
            href_value = link_element.get_attribute("href")
            # Comparaison avec example.com
            if href_value.startswith(url):
                html = driver.page_source
                profile = html.split('id="main_wrapper"')[1].split('id="main"')[1]
                profile_stat = {
                    i.split('<span class="gras">')[1].split('</span>')[0]:i.split("</h3>")[0].split("&nbsp;")[-1]
                    for i in profile.split('<div class="tile">')[1].split("<h3>")[1:]
                }
                stat = [
                    {
                        "title": i.split('<a title="')[1].split('"')[0],
                        "image": "https://www.root-me.org/" + i.split("background: url(")[1].split(")")[0],
                        "value": i.split("</a></span>")[0].split(">")[-1]
                    } for i in profile.split("Validations</h3>")[1].split("<h3>Badges")[0].split('<div class="small-3 medium-2 large-1 columns">')[1:]
                ]
            else:
                print("❌ Condition non remplie → Pas de récupération")
        else:
            print("⚠️ Tableau incomplet → Pas assez de lignes")
    except Exception as e:
        print("Erreur :", e)
    finally:
        driver.quit()

    return profile_stat, stat

def get_thm_badges_and_rooms() -> tuple[int, int, int, list[dict], list[dict], list[dict]]:
    print("[WAIT] get_thm_badges_and_rooms")
    user_profile = requests.get(
        "https://tryhackme.com/api/v2/public-profile?username=" + os.getenv("TRYHACKME_USERNAME"), 
        headers = { "Accept": "application/json" }
    ).json()["data"]

    user_id = user_profile["_id"]
    rank = user_profile["rank"]
    level = user_profile["level"]
    completed_rooms_number = user_profile["completedRoomsNumber"]
    badges_number = user_profile["badgesNumber"]

    def __request_room__(tab:str) -> dict:
        def __request__(index_page:int) -> dict:
            return requests.get(
                f"https://tryhackme.com/api/v2/public-profile/{tab}?user={user_id}&limit=16&page={index_page}", 
                headers = { "Accept": "application/json" }
            ).json()
        data = []
        total_pages = __request__(1)["data"]["totalPages"]
        for index_page in range(total_pages):
            res = __request__(index_page+1)
            data += res["data"]["docs"]
        return data

    def __request_cert__() -> dict:
        def __request__(index_page:int) -> dict:
            return requests.get(
                f"https://tryhackme.com/api/v2/certificates/public-list?page={index_page}&limit=10&sort=Newest&username={os.getenv('TRYHACKME_USERNAME')}", 
                headers = { "Accept": "application/json" }
            ).json()
        data = []
        total_pages = __request__(1)["data"]["totalPages"]
        for index_page in range(total_pages):
            res = __request__(index_page+1)
            data += res["data"]["docs"]
        return data

    rooms = [{
        "title": i["title"], 
        "description": i["description"], 
        "image": i["imageURL"], 
        "url": "https://tryhackme.com/room/" + i["code"], 
        "difficulty": i["difficulty"], 
    } for i in __request_room__("completed-rooms")]

    badges = [{
        "title": i["title"], 
        "description": i["description"], 
        "image": "https://tryhackme.com" + i["image"], 
        "rarity": {
            "tier": i["rarityTier"],
            "percent": i["rarityPercent"]
        }
    } for i in __request_room__("badges")]

    path_completions = [{
        "name": i["name"], 
        "certId": i["certId"], 
        "url": f"https://tryhackme-certificates.s3-eu-west-1.amazonaws.com/{i['certId']}.png"
    } for i in __request_cert__()]

    for i in path_completions:
        if i["name"] + ".png" not in os.listdir("./images"):
            content = requests.get(i["url"]).content
            with open("./images/" + i["name"] + ".png", "wb") as image:
                image.write(content)

    print("[OK] get_thm_badges_and_rooms")

    return (
        rank, level, completed_rooms_number, badges_number, 
        rooms, badges, path_completions
    )

def download_image(url:str, dirpath:str="download", rename:str=None) -> str:
    filename = urlsplit(url).path.split("/")[-1] if rename is None else rename
    # correction
    if "." not in filename or not (3 <= len(filename.split(".")[-1]) <= 4):
        filename += ".png"

    dirpath = "./images/" + dirpath.strip("/")
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    filepath = dirpath + "/" + filename
    if not os.path.exists(filepath):
        with open(filepath, "wb") as file:
            image = requests.get(url).content
            file.write(image)
    return filepath
