// Function to fetch the current time
function updateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    document.getElementById("time").textContent = timeString;
    setTimeout(updateTime, 1000);
}
// Start time 
updateTime();

document.addEventListener("DOMContentLoaded", () => {
    const noticeCard = document.getElementById("notice-card");

    // Fetch notices from the backend
    fetch("/api/notices")
        .then(response => response.json())
        .then(data => {
            noticeCard.innerHTML = "";
            if (data.length === 0) {
                noticeCard.innerHTML = "<p>No notices available at the moment.</p>";
            } else {
                data.forEach((notice, index) => {
                    const noticeElement = document.createElement("p");
                    noticeElement.innerText = `${index + 1}. ${notice}`;
                    noticeCard.appendChild(noticeElement);
                });
            }
        })
        .catch(error => {
            console.error("Error fetching notices:", error);
        });
});

// Music Button Functionality
let musicButton = document.getElementById("musicButton");
let musicAudio = document.getElementById("musicAudio");
let musicPlaying = false;

musicButton.addEventListener("click", function() {
    if (musicPlaying) {
        musicAudio.pause();
        musicButton.querySelector("span").innerText = "Play Dhun";
    } else {
        musicAudio.play();
        musicButton.querySelector("span").innerText = "Stop Dhun";
        showDevotionalEffect();
    }
    musicPlaying = !musicPlaying;
});

// Function to show multiple flowers and devotional effect
function showDevotionalEffect() {
    let flowers = document.createElement("div");
    flowers.classList.add("flowers");
    flowers.innerHTML = "<img src='/static/images/fl1.png' alt='Flower'><img src='/static/images/fl2.png' alt='Flower'><img src='/static/images/fl1.png' alt='Flower'>";
    document.body.appendChild(flowers);
    
    setTimeout(() => {
        flowers.style.animation = "devotionalEffect 5s infinite";
    }, 100);

    setTimeout(() => {
        flowers.remove();
    }, 15000); // Remove after 15 seconds
}

// Image Slider Functionality
let slideIndex = 0;
const slides = document.querySelectorAll(".slider img");

function showSlides() {
    slideIndex++;
    if (slideIndex >= slides.length) {
        slideIndex = 0;
    }

    // Move the slider by adjusting its transform property
    document.querySelector(".slider").style.transform = `translateX(-${slideIndex * 100}%)`;
}

setInterval(showSlides, 3000); // Change image every 3 seconds

