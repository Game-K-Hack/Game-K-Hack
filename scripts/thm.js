let box = document.getElementById("thm_badge");
let level = box.querySelector("span[class=\"thm_rank\"]").innerText;
level = level.substring(3, level.length-1);
values = box.innerText.split("\n");

document.getElementById("thmrank").innerText = values[3];
document.getElementById("thmroom").innerText = values[4];
document.getElementById("thmlevel").innerText = level;
document.getElementById("thmbadge").innerText = values[5];

var onc = document.getElementById("thm_badge").attributes.onclick.nodeValue
var url = onc.substring(onc.indexOf("='") + 2, onc.lastIndexOf("'"));
document.querySelector("div[class=\"cyber-container\"]").onclick = function(){window.open(url, '_blank').focus();};

document.getElementById("thm_badge").remove();
document.getElementById("thm_script").remove();
