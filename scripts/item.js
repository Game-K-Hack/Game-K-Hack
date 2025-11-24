document.querySelectorAll("#elm").forEach((elm) => {
  // Cloner l'élément pour calculer sa hauteur complète
  const clone = elm.cloneNode(true);
  clone.style.height = "auto";
  clone.style.visibility = "hidden";
  clone.style.position = "absolute";
  clone.querySelector(".item-description").style.animation = "unset";
  clone.querySelector(".item-description").style.height = "100%";

  // Ajouter le clone au DOM temporairement
  document.body.appendChild(clone);

  // Récupérer la hauteur complète
  const fullHeight = clone.scrollHeight;

  // Supprimer le clone
  document.body.removeChild(clone);

  // Gérer l'affichage du texte
  elm.addEventListener("mouseenter", function () {
    this.style.height = fullHeight + "px";
  });

  elm.addEventListener("mouseleave", function () {
    this.style.height = "";
  });
});
