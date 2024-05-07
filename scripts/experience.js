function patternExperience(elm) {
    date = elm["start_date"].toUpperCase() + " | " + elm["end_date"].toUpperCase();
    return `
        <li class="timeline-item">
            <div class="timeline-info">
                <span style="color:#768390;">${date}</span>
            </div>
            <div class="timeline-marker"></div>
            <div class="timeline-content">
                <h3 class="timeline-title" style="color:#3d4351;font-size: 24px;margin-bottom: 5px;">${elm["type"]} - ${elm["company"]} (${elm["place"]})</h3>
                <p style="color:#768390;">${elm["info"]}</p>
            </div>
        </li>`
}

loadYAML("./data/experience.yml", content => {
    content = content["experience"];
    let base = document.getElementById("ep").innerHTML;
    for (let elm of content) {
        base = patternExperience(elm) + base;
    }
    document.getElementById("ep").innerHTML = base;
});
