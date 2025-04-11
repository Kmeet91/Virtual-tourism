document.addEventListener("DOMContentLoaded", function () {
    // Smooth Scrolling for Hero Button
    document.querySelector(".hero .btn").addEventListener("click", function (e) {
        e.preventDefault();
        document.querySelector("#destinations").scrollIntoView({ behavior: "smooth" });
    });

    // Search Functionality
    document.getElementById("searchInput").addEventListener("keyup", function () {
        let searchText = this.value.toLowerCase();
        let cards = document.querySelectorAll(".grid-container .card");

        cards.forEach((card) => {
            let placeName = card.querySelector("h3").textContent.toLowerCase();
            let location = card.querySelector("p").textContent.toLowerCase();
            if (placeName.includes(searchText) || location.includes(searchText)) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    });
});
