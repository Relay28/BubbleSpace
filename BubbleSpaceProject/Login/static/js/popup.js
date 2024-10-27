function togglePopup() {
    const popup = document.getElementById("popup");
    popup.classList.toggle("show");
}

document.addEventListener("click", function(event) {
    const popup = document.getElementById("popup");
    const menuIcon = document.querySelector(".menu");

    if (!menuIcon.contains(event.target) && !popup.contains(event.target)) {
        popup.classList.remove("show");
    }
});
