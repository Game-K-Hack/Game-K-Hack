document.querySelectorAll(".card3d").forEach(card => {
    const items = card.querySelectorAll("[data-z]");

    card.addEventListener("mousemove", (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;

        const rotateX = (-y / 3).toFixed(2);
        const rotateY = (x / 3).toFixed(2);

        card.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;

        items.forEach(item => {
            const z = item.getAttribute("data-z");
            item.style.transform = `translateZ(${z}px)`;
        });
    });

    card.addEventListener("mouseleave", () => {
        card.style.transform = "rotateX(0deg) rotateY(0deg)";
        items.forEach(item => item.style.transform = "translateZ(0)");
    });
});
