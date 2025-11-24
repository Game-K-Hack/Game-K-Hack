function centofintClearP() {
    document.querySelector(`div[class="centofint-list"]`).querySelectorAll(`div[class="centofint-elm"]`).forEach(elm => {
    elm.attributes.p.value = "";
    });
}

document.querySelector(`div[class="centofint-list"]`).querySelectorAll(`div[class="centofint-elm"]`).forEach(elm => {
    elm.onclick = function() {
        if (elm.attributes.unselectable != undefined) return;
        centofintClearP();
        elm.attributes.p.value = "c";
        if (elm.previousElementSibling) elm.previousElementSibling.attributes.p.value = "b";
        if (elm.nextElementSibling) elm.nextElementSibling.attributes.p.value = "a";
    };
});

const elms = document.querySelector(`div[class="centofint-list"]`).querySelectorAll(`div[class="centofint-elm"]`);
elms[0].attributes.p.value = "b";
elms[1].attributes.p.value = "c";
elms[2].attributes.p.value = "a";