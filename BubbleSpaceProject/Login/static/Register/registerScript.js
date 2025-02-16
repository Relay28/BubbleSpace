window.onload = function () {
    const formInputs = document.querySelectorAll("input, select");
    const submitButton = document.getElementById("submit-btn");

    // Add event listeners to all form inputs
    formInputs.forEach(input => {
        input.addEventListener("input", checkFormCompletion);
    });

    function checkFormCompletion() {
        let allFilled = true;

        formInputs.forEach(input => {
            if (input.hasAttribute("required") && !input.value.trim()) {
                allFilled = false;
            }
        });

        if (allFilled) {
            submitButton.disabled = false;
            submitButton.classList.add("active");
        } else {
            submitButton.disabled = true;
            submitButton.classList.remove("active");
        }
    }

    // Toggle password visibility
    const togglePassword = document.querySelector(".toggle-password");
    const passwordField = document.getElementById("password");

    togglePassword.addEventListener("click", function () {
        if (passwordField.type === "password") {
            passwordField.type = "text";
            togglePassword.textContent = "👁️ Hide";
        } else {
            passwordField.type = "password";
            togglePassword.textContent = "👁️ Show";
        }
    });
};
