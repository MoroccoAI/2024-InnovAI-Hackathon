import { initNavigation } from './navigation.js';
import { initChat } from './chat.js';
import { initSocial } from './social.js';

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initChat();
    initSocial();
});

document.addEventListener("DOMContentLoaded", () => {
    const text =
        "MedConnect is a platform designed specifically for doctors, providing advanced tools to improve patient care, streamline medical workflows, and enhance collaboration between healthcare professionals.";
    const purposeElement = document.getElementById("platform-purpose");

    // Time delay between words (in milliseconds)
    const wordDelay = 500; // Set this to control word appearance speed
    const repeatInterval = 10000; // Total interval to repeat the animation (in milliseconds)

    const displayWords = (text, element, delay) => {
        const words = text.split(" ");
        element.innerHTML = ""; // Clear existing content

        words.forEach((word, index) => {
            const span = document.createElement("span");
            span.className = "word";
            span.style.animationDelay = `${index * (delay / 1000)}s`; // Convert ms to seconds
            span.textContent = word; // Add the word text
            element.appendChild(span);

            // Add space after each word except the last
            if (index < words.length - 1) {
                element.appendChild(document.createTextNode(" "));
            }
        });
    };

    // Initial word-by-word display
    displayWords(text, purposeElement, wordDelay);

    // Repeat the process at the defined interval
    setInterval(() => {
        displayWords(text, purposeElement, wordDelay);
    }, repeatInterval);
});


