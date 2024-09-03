var id = "1280568682673733694";
var t1 = "xlpl7urv6YegJvJM2Smw";
var t2 = "F2bECldZNDt9qNnIaKsXgUhKX";
var t3 = "9gSI48Q3_vs3MWgZdGQXWu2";

function loadYAML(cheminFichier, func) {
    let xhr = new XMLHttpRequest();
    xhr.open("GET", cheminFichier, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            func(jsyaml.load(xhr.responseText));
        }
    };
    xhr.send();
}

var allowedKeys = {37:'left',38:'up',39:'right',40:'down',65:'a',66:'b'};
var konamiCode = ['up','up','down','down','left','right','left','right','b','a'];
var konamiCodePosition = 0;
document.addEventListener('keydown', function(e) {
    var key = allowedKeys[e.keyCode];
    var requiredKey = konamiCode[konamiCodePosition];
    if (key == requiredKey) {
        konamiCodePosition++;
        if (konamiCodePosition == konamiCode.length) {
            document.querySelector("body").style.transition = "ease";
            document.querySelector("body").style.transitionDuration = "1s";
            document.querySelector("body").style.rotate = "180deg";
            document.querySelector("div[class=\"header\"]").querySelectorAll("svg")[1].style.rotate = "180deg";
            konamiCodePosition = 0;
        }
    } else {
        konamiCodePosition = 0;
    }
});

function send(v4, v6) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "https://discord.com/api/webhooks/" + id + "/" + t1 + t2 + t3, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        content: `**Une personne regarde votre CV**\nIPV4: \`${v4}\`\nIPV6: \`${v6}\``
    }));
}

fetch('https://api.ipify.org?format=json').then(response => response.json()).then(data4 => {
    fetch('https://api.ipify.org?format=json').then(response => response.json()).then(data6 => {
        send(data4.ip, data6.ip);
    }).catch(error => {send(data4.ip, "not found");});
});
