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
