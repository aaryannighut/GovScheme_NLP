// GovScheme NLP Client-side Javascript

document.addEventListener("DOMContentLoaded", function () {
    console.log("GovScheme NLP application script initialized.");

    // Populate input text from example buttons
    const exampleBtns = document.querySelectorAll(".example-btn");
    const userTextArea = document.getElementById("user_text");

    if (exampleBtns && userTextArea) {
        exampleBtns.forEach(btn => {
            btn.addEventListener("click", function () {
                const sampleText = this.getAttribute("data-text");
                if (sampleText) {
                    userTextArea.value = sampleText;
                    userTextArea.focus();
                }
            });
        });
    }

    // Form Validation
    const profileForm = document.getElementById("profileForm");
    if (profileForm) {
        profileForm.addEventListener("submit", function (e) {
            const inputVal = userTextArea ? userTextArea.value.trim() : "";
            if (!inputVal) {
                e.preventDefault();
                alert("Please enter a description of yourself or click one of the demo examples below.");
                if (userTextArea) userTextArea.focus();
            }
        });
    }

    // Processing Page Animation Checklist Simulator
    const processSteps = document.querySelectorAll(".process-step-item");
    if (processSteps && processSteps.length > 0) {
        let stepIdx = 0;
        const stepInterval = setInterval(() => {
            if (stepIdx < processSteps.length) {
                const currentStep = processSteps[stepIdx];
                const icon = currentStep.querySelector(".step-icon");
                const text = currentStep.querySelector(".step-text");

                if (icon) {
                    icon.className = "step-icon text-success fw-bold me-2";
                    icon.innerHTML = "✓";
                }
                if (text) {
                    text.classList.remove("text-muted");
                    text.classList.add("fw-semibold", "text-dark");
                }
                stepIdx++;
            } else {
                clearInterval(stepInterval);
                // Submit form to view results
                const hiddenForm = document.getElementById("hiddenSubmitForm");
                if (hiddenForm) {
                    setTimeout(() => {
                        hiddenForm.submit();
                    }, 500);
                }
            }
        }, 350);
    }
});
