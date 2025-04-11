document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const cards = document.querySelectorAll(".card");

    searchInput.addEventListener("input", function () {
        const filter = searchInput.value.toLowerCase();
        
        cards.forEach(card => {
            const title = card.querySelector("h2").textContent.toLowerCase();
            const location = card.querySelector("p").textContent.toLowerCase();
            
            if (title.includes(filter) || location.includes(filter)) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    });
});
