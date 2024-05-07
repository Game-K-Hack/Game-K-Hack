function mouseOverSkillBox(id) {
    let elm = document.querySelector(`div[id="` + id + `"] div[class="slide-text"]`);
    elm.style.animation = "1s slide-text forwards";
    elm.style.transform = "translateY(0)";
    elm.style.display = ""
}

function mouseOutSkillBox(id) {
    let elm = document.querySelector(`div[id="` + id + `"] div[class="slide-text"]`);
    elm.style.animation = "1s slide-text forwards";
    elm.style.transform = "translateY(-100%)";
    elm.style.display = "none"
}

function patternSkill(elm, index) {
    return `
      <div class="skill-box grid-cols-1 gap-20 lg:grid-cols-2 lg:gap-10" id="${elm["name"]}">
        <div class="flex items-center flex-wrap max-w-md px-10 bg-white shadow-xl rounded-2xl h-20"
          x-data="{ circumference: 50 * 2 * Math.PI, percent: ${elm["percent"]} }"
          style="z-index: ${index + 1};"
          onmouseover="this.style.height='${elm["height"]}'"
          onmouseout="this.style.height=''"
          id="elm">
          <div class="flex items-center justify-center -m-6 overflow-hidden bg-white rounded-full"
            style="box-shadow: rgba(0, 0, 0, 0.2) 0px 18px 50px -10px;">
            <svg class="w-32 h-32 transform translate-x-1 translate-y-1" x-cloak aria-hidden="true">
              <circle class="text-gray-300" stroke-width="10" stroke="currentColor" fill="transparent" r="50" cx="60"
                cy="60" />
              <circle class="text-blue-600" stroke-width="10" :stroke-dasharray="circumference"
                :stroke-dashoffset="circumference - percent / 100 * circumference" stroke-linecap="round"
                stroke="currentColor" fill="transparent" r="50" cx="60" cy="60" />
            </svg>
            <!-- <span class="absolute text-2xl text-blue-700" x-text="\`\${percent}\%\`"></span> -->
            <img class="skill-box-img absolute text-2xl text-blue-700" src="${elm["src"]}"/>
          </div>
          <p class="ml-10 font-medium text-gray-600 sm:text-xl" style="margin-top: 25px;">${elm["name"]}</p>
          <span class="ml-auto text-xl font-medium text-blue-600 hidden sm:block" style="margin-top: 25px;"
            x-text="\`\${percent}\%\`"></span>
          <div class="slide-text" style="display: none; text-align: left;">
            <h2>
              ${elm["desc"]}
            </h2>
          </div>
        </div>
      </div>`
}

loadYAML("./data/skill.yml", content => {
  content = content["skill"];

  lang = content["language"];

  let baseSkpl = document.getElementById("skpl").innerHTML
  lang.forEach(function (value, index) {
    baseSkpl += patternSkill(value, (lang.length*2)-index);
  });

  document.getElementById("skpl").innerHTML = baseSkpl;

  lang.forEach(function (value, _) {
    document.getElementById(value["name"]).children[0].addEventListener(
      "mouseover",
      function () {
          mouseOverSkillBox(value["name"])
      }
    );
    document.getElementById(value["name"]).children[0].addEventListener(
        "mouseout",
        function () {
            mouseOutSkillBox(value["name"])
        }
    );
  });

  tool = content["tool"];

  let baseSkt = document.getElementById("skt").innerHTML
  tool.forEach(function (value, index) {
    baseSkt += patternSkill(value, tool.length-index);
  });

  document.getElementById("skt").innerHTML = baseSkt;

  tool.forEach(function (value, _) {
    document.getElementById(value["name"]).children[0].addEventListener(
      "mouseover",
      function () {
          mouseOverSkillBox(value["name"])
      }
    );
    document.getElementById(value["name"]).children[0].addEventListener(
        "mouseout",
        function () {
            mouseOutSkillBox(value["name"])
        }
    );
  });

});