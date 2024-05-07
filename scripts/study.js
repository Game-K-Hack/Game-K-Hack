function patternStudy(elm) {
  info = elm["place"]
  if (elm["info"] != "" && elm["info"] != null) {
    info = elm["info"] + "<br>" + info;
  }
  return `
    <li class="timeline-item">
      <div class="timeline-info">
        <span style="color:#768390;">${elm["start_year"]}, ${elm["end_year"]}</span>
      </div>
      <div class="timeline-marker"></div>
      <div class="timeline-content">
        <h3 class="timeline-title" style="color:#3d4351;font-size: 24px;margin-bottom: 5px;">${elm["name"]}</h3>
        <p style="color:#768390;">${info}</p>
      </div>
    </li>
  `
}

loadYAML("./data/study.yml", content => {
  content = content["study"];
  content.reverse();
  var base = document.getElementById("std").innerHTML;
  for (let elm of content) {
    base = patternStudy(elm) + base;
  }
  document.getElementById("std").innerHTML = base;
});
