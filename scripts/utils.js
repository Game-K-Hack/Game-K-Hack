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
