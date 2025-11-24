from service import download_image, \
                    get_rootme_stat, \
                    get_credly_badges, \
                    get_thm_badges_and_rooms, \
                    TRYHACKME_URL_PROFILE, \
                    ROOTME_URL_PROFILE

with open("model.html", "r", encoding="utf8") as file: # ouvrir le fichier model
    content = file.read() # lire le contenu

def get_items(name:str) -> list[tuple[list[str], str]]:
    items:list[tuple[list[str], str]] = []
    for item in content.split("{%" + name.upper() + ":")[1:]:
        item = item.split("%}")[0] # récupération des informations de l'item actuel
        balise = "{%" + name.upper() + ":" + item + "%}" # recréation de la balise complète

        n1 = item.split("§") # split niveau 1
        if len(n1) > 1:
            items.append((
                [
                    [j.strip() for j in i.split(";")] 
                    for i in item.split("§")
                ], balise
            ))
        else:
            items.append(([j.strip() for j in item.split(";")], balise))
    b = "{%" + name.upper() + "%}"
    if len(items) == 0 and b in content:
        items = [(None, b)]*content.count(b)
    return items

def set_item2html(item:tuple[list, str], code:str, format_auto_replace:bool=True) -> None:
    global content
    if format_auto_replace and "{!L:" in code:
        for i in code.split("{!L:")[1:]:
            n, l = i.split("!}")[0].split("!")
            b = "{!L:" + n + "!" + l + "!}"
            code = code.replace(b, f'<a target="_blank" rel="noopener noreferrer" href="{l}"><u>{n}</u></a>')
    content = content.replace(item[1], code, 1)



# Paramétrer les images SVG
for item in get_items("svg"):
    svg_balise = open("./images/" + item[0][0], "r", encoding="utf8").read()
    set_item2html(item, svg_balise)

# Ajouter des items à la navbar
for item in get_items("nav-item"):
    code = f'<a class="navbar-link" href="#{item[0][1]}">\n<i class="navbar-icon-hoverable fa-solid {item[0][2]}"></i>\n<i class="navbar-icon-default fa-light {item[0][2]}"></i>\n<span>{item[0][0]}</span>\n</a>'
    set_item2html(item, code)

# Ajouter les timelines
for item in get_items("timeline"):
    balise = '<div class="container-fluid"><div class="row example-basic">' \
             '<div class="col-xs-10 col-xs-offset-1 col-sm-8 col-sm-offset-2">' \
             '<ul class="timeline" id="std">'
    for subitem in item[0]:
        title, subtitle, date = subitem
        i = '<li class="timeline-item"><div class="timeline-info">' \
            f'<span style="color: #768390">{date}</span>' \
            '</div><div class="timeline-marker"></div><div class="timeline-content">' \
            f'<h3 class="timeline-title" style="color: #3d4351; font-size: 24px; margin-bottom: 5px">{title}</h3>' \
            f'<p style="color: #768390">{subtitle}</p></div></li>'
        balise += i
    balise += '<li class="timeline-item period"><div class="timeline-marker"></div>' \
              '<div class="timeline-content"></div></li></ul></div></div></div>'
    set_item2html(item, balise)

# Ajouter les items de compétence
items = get_items("item")
len_items = len(items)
for index, item in enumerate(items):
    percent, title, icon = item[0][:3]
    description = ";".join(item[0][3:])
    code = f'<div class="skill-box grid-cols-1 gap-20 lg:grid-cols-2 lg:gap-10">' \
           '<div class="flex items-center flex-wrap max-w-md px-10 bg-white shadow-xl rounded-2xl h-20" x-data="{ circumference: 50 * 2 * Math.PI, percent: ' + percent + ' }" style="z-index: ' + str(len_items-index) + ';" id="elm">' \
           '<div class="flex items-center justify-center -m-6 overflow-hidden bg-white rounded-full" style="box-shadow: rgba(0, 0, 0, 0.2) 0px 18px 50px -10px;">' \
           '<svg class="w-32 h-32 transform translate-x-1 translate-y-1" aria-hidden="true">' \
           '<circle class="text-gray-300" stroke-width="10" stroke="currentColor" fill="transparent" r="50" cx="60" cy="60"></circle>' \
           '<circle class="text-blue-600" stroke-width="10" :stroke-dasharray="circumference" :stroke-dashoffset="circumference - percent / 100 * circumference" stroke-linecap="round" stroke="currentColor" fill="transparent" r="50" cx="60" cy="60" stroke-dasharray="314.1592653589793" stroke-dashoffset="125.66370614359172"></circle></svg>' \
           f'<img class="skill-box-img absolute text-2xl text-blue-700" src="images/{icon}"></div>' \
           f'<p class="ml-10 font-medium text-gray-600 sm:text-xl" style="margin-top: 25px;">{title}</p>' \
           '<span class="ml-auto text-xl font-medium text-blue-600 hidden sm:block" style="margin-top: 25px;" x-text="`${percent}%`">' + percent + '%</span>' \
           f'<span class="item-description">{description}</span></div></div>'
    set_item2html(item, code)

# Ajouter les stats TryHackMe
item = get_items("tryhackme")[0]
rank, level, completed_rooms_number, badges_number, rooms, badges, path_completions = get_thm_badges_and_rooms()
balise = "<div class=\"cyber-container\">"
balise += f'<a target="_blank" rel="noopener noreferrer" href="{TRYHACKME_URL_PROFILE}"class="cyber-stat"><img class="cyber-thm-logo" src="./images/cyber/tryhackme/logo.png">'
balise += f'<div class="cyber-stat-elm"><h3 id="thmrank" class="cyber-stat-elm-h3">{rank}</h3><p class="cyber-stat-elm-p">Rank</p></div>'
balise += f'<div class="cyber-stat-elm"><h3 id="thmroom" class="cyber-stat-elm-h3">{completed_rooms_number}</h3><p class="cyber-stat-elm-p">Rooms Complete</p></div>'
balise += f'<div class="cyber-stat-elm"><h3 id="thmlevel" class="cyber-stat-elm-h3">{level}</h3><p class="cyber-stat-elm-p">Level</p></div>'
balise += f'<div class="cyber-stat-elm"><h3 id="thmbadge" class="cyber-stat-elm-h3">{badges_number}</h3><p class="cyber-stat-elm-p">Badges</p></div>'
balise += '</a>'
balise += '<div class="cyber-badge">'
for badge in badges:
    image = download_image(badge["image"], "cyber/tryhackme/badges")
    balise += f'<div class="cyber-badge-elm"><img class="cyber-badge-elm-img" src="{image}">'
    rarity_color = badge["rarity"]["tier"][:2]
    rarity = badge["rarity"]["tier"] + ": " + str(badge["rarity"]["percent"]) + "%"
    balise += f'<div class="cyber-badge-elm-div"><h3>{badge["title"]}</h3><p>{badge["description"]}</p><span c="{rarity_color}">{rarity}</span></div></div>'
balise += "</div>"
balise += '<div class="cyber-room">'
for room in rooms:
    image = download_image(room["image"], "cyber/tryhackme/rooms")
    balise += f'<a target="_blank" rel="noopener noreferrer" href="{room["url"]}" class="cyber-room-elm"><img class="cyber-room-elm-img" src="{image}">'
    svg = open(f"images/cyber/tryhackme/{room['difficulty']}.svg", "r", encoding="utf8").read()
    balise += f'<div class="cyber-room-elm-div"><div class="cyber-room-title"><h3>{room["title"]}</h3>{svg}<p c="{room["difficulty"][:3]}">{room["difficulty"][0].upper() + room["difficulty"][1:]}</p></div>'
    balise += f'<p class="cyber-room-elm-p">{room["description"]}</p></div></a>'
balise += "</div>"
balise += "</div>"
set_item2html(item, balise)

# Ajouter les stats RootMe
item = get_items("rootme")[0]
stat, data = get_rootme_stat()
rank, score, room = stat["Place"], stat["Points"], stat["Challenges"]
balise = "<div class=\"cyber-container\">"
balise += f'<a target="_blank" rel="noopener noreferrer" href="{ROOTME_URL_PROFILE}"class="cyber-stat"><img class="cyber-thm-logo" src="./images/cyber/rootme/logo.svg">'
balise += f'<div class="cyber-stat-elm"><h3 class="cyber-stat-elm-h3">{rank}</h3><p class="cyber-stat-elm-p">Rank</p></div>'
balise += f'<div class="cyber-stat-elm"><h3 class="cyber-stat-elm-h3">{room}</h3><p class="cyber-stat-elm-p">Challenges Completed</p></div>'
balise += f'<div class="cyber-stat-elm"><h3 class="cyber-stat-elm-h3">{score}</h3><p class="cyber-stat-elm-p">Score</p></div>'
balise += '</a>'
balise += '<div class="cyber-badge" style="flex-wrap: wrap;justify-content: center;">'
for elm in data:
    image = download_image(elm["image"], "cyber/rootme/challenges")
    value = int(elm["value"][:-1])
    balise += '<div class="skill-box grid-cols-1 gap-20 lg:grid-cols-2 lg:gap-10 slide-text-animation">' \
              '<div class="flex items-center flex-wrap max-w-md px-10 bg-white shadow-xl rounded-2xl h-20 smallbox" x-data="{ circumference: 50 * 2 * Math.PI, percent: ' + str(value) + ' }" id="elm" style="box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;">' \
              '<div class="flex items-center justify-center -m-6 overflow-hidden bg-white rounded-full" style="box-shadow: rgba(0, 0, 0, 0.2) 0px 18px 50px -10px;">' \
              '<svg class="w-32 h-32 transform translate-x-1 translate-y-1" aria-hidden="true"><circle class="text-gray-300" stroke-width="10" stroke="currentColor" fill="transparent" r="50" cx="60" cy="60"></circle>' \
              '<circle class="text-blue-600" stroke-width="10" :stroke-dasharray="circumference" :stroke-dashoffset="circumference - percent / 100 * circumference" stroke-linecap="round" stroke="currentColor" fill="transparent" r="50" cx="60" cy="60" stroke-dasharray="314.1592653589793" stroke-dashoffset="0"></circle>' \
              f'</svg><img class="skill-box-img absolute text-2xl text-blue-700" src="{image}"></div><p class="ml-10 font-medium text-gray-600 sm:text-xl" style="margin-top: 25px;">{elm["title"]}</p>' \
              f'<span class="ml-auto text-xl font-medium text-blue-600 hidden sm:block" style="margin-top: 25px;">{value}%</span></div></div>'
balise += "</div>"
balise += "</div>"
set_item2html(item, balise)

# Ajouter des certifications
item = get_items("certifications")[0]
certs = [
    {"name": "Pix", "id": "P-8RQC23RD", "image": "images/certifications/pix.png", "url": "https://app.pix.fr/verification-certificat"}, 
    {"name": "Pix", "id": "P-V2JC4RW7", "image": "images/certifications/pix.png", "url": "https://app.pix.fr/verification-certificat"}, 
    {"name": "SecNumacadémie : se former à la sécurité informatique", "image": "images/certifications/anssi.png", "url": "https://secnumacademie.gouv.fr"}, 
]
certs += [{
    "id": None, 
    "name": i["name"], 
    "image": i["image"], 
    "url": i["url"]
} for i in get_credly_badges()]
certs += [{
    "name": i["name"], 
    "id": i["certId"], 
    "image": i["url"], 
    "url": "https://tryhackme.com/certificate/" + i["certId"]
} for i in path_completions]
balise = "<div class=\"cert-container\">"
for cert in certs:
    image = download_image(
        cert["image"], 
        "certifications", 
        (cert["id"] or cert["name"]) + ".png"
    ) if cert["image"].startswith("http") else cert["image"]
    code = f'<a target="_blank" rel="noopener noreferrer" href="{cert["url"]}" class="cert-box" style="width: 200px;">' \
            '<div class="cert card3d"><div class="card3d-image-wrapper" data-z="30">' \
           f'<img src="{image}" alt="thumbnail" class="card3d-image">' \
           f'</div><h2 class="card3d-title">{cert["name"]}</h2>'
    if "id" in cert.keys() and cert["id"] is not None:
        code += f'<p class="card3d-id">{cert["id"]}</p>'
    code += '</div></a>'
    balise += code
balise += "</div>"
set_item2html(item, balise)

# Ajouter les mini box
items = get_items("minibox")
for item in items:
    title, icon, url = item[0]
    code = f'<a target="_blank" rel="noopener noreferrer" href="{url}" class="minibox-elm">' \
           f'<img src="images/{icon}"><h2>{title}</h2></a>'
    set_item2html(item, code)

# Ajouter les mini box avec effet 3d
items = get_items("minibox3d")
for item in items:
    title, icon, url = item[0]
    code = f'<a target="_blank" rel="noopener noreferrer" href="{url}" class="card3d-box">' \
           '<div class="card3d"><div class="card3d-image-wrapper" data-z="30">' \
           f'<img src="images/{icon}" class="card3d-image" alt="thumbnail"/>' \
           f'</div><h2 class="card3d-title" data-z="0">{title}</h2></div></a>'
    set_item2html(item, code)

# Ajouter les réalisations & porjets
items = get_items("product-text")
for item in items:
    if len(item[0]) == 4:
        icon, title, description, detail = item[0]
        code = f'<div class="product-text" onclick="toggle_detail_text(event)">' \
               f'<img src="images/product/{icon}">' \
               f'<h1 class="product-title">{title}</h1>' \
               f'<span class="short">{description}</span>' \
               f'<span class="long">{detail}</span></div>'
    else:
        icon, title, description = item[0]
        code = f'<div class="product-text"><img src="images/product/{icon}">' \
               f'<h1 class="product-title">{title}</h1>{description}</div>'
    set_item2html(item, code)

# Ajouter les centres d'interet
items = get_items("CENTER-OF-INTEREST")
for item in items:
    code = '<div class="centofint-container"><div class="centofint-display"></div><div class="centofint-list">'
    code += '<div class="centofint-elm" p="" unselectable></div>'
    for title, image in item[0]:
        code += f'<div class="centofint-elm" p=""><img class="ci-img" src="./images/center-of-interest/{image}"><p>{title}</p></div>'
    code += '<div class="centofint-elm" p="" unselectable></div></div></div>'
    set_item2html(item, code)



with open("index.html", "w", encoding="utf8") as index: # on créer un fichier index
    index.write(content) # et on écrie le contenu modifier
