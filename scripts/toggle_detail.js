function toggle_detail_text(event) {
    let elm = event.target;
    if (elm.nodeName.toLowerCase() == "a" || elm.parentElement.nodeName.toLowerCase() == "a") return;
    if (elm.onclick == undefined) elm = elm.parentElement;
    elm.className = (elm.className == "product-text") ? "product-text product-text-extended" : "product-text";
}