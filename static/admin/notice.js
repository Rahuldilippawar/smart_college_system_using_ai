document.addEventListener("DOMContentLoaded", () => {
    const noticeForm = document.getElementById("notice-form");
    const noticeText = document.getElementById("notice-text");
    const noticeList = document.getElementById("notice-list");
    const popup = document.getElementById("popup");
    const popupMessage = document.getElementById("popup-message");
    const popupClose = document.getElementById("popup-close");

    // Function to show pop-up message
    function showPopup(message) {
        popupMessage.textContent = message;
        popup.style.display = "block"; // Show pop-up
    }

    // Close the pop-up when the close button is clicked
    popupClose.addEventListener("click", () => {
        popup.style.display = "none"; // Hide pop-up
    });

    // Function to load all notices
    function loadNotices() {
        fetch("/api/notices") // Fetch notices from the backend
            .then((response) => {
                if (!response.ok) throw new Error("Failed to fetch notices");
                return response.json();
            })
            .then((notices) => {
                noticeList.innerHTML = ""; // Clear existing notices
                if (notices.length === 0) {
                    noticeList.innerHTML = "<p>No notices available.</p>";
                } else {
                    notices.forEach((notice, index) => {
                        const listItem = document.createElement("li");
                        listItem.innerHTML = `
                            <span>${notice}</span>
                            <button data-id="${index}" class="delete-notice">Delete</button>
                        `;
                        noticeList.appendChild(listItem);
                    });
                }
            })
            .catch((error) => console.error("Error loading notices:", error));
    }

    // Add or update a notice
    noticeForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const newNotice = noticeText.value.trim();
        if (newNotice) {
            fetch("/api/notices", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ notice: newNotice }),
            })
                .then((response) => {
                    if (!response.ok) throw new Error("Failed to save notice");
                    return response.json();
                })
                .then(() => {
                    noticeText.value = ""; // Clear the input
                    loadNotices(); // Reload the notice list
                    showPopup("Notice saved successfully!"); // Show success message
                })
                .catch((error) => console.error("Error saving notice:", error));
        }
    });

    // Delete a notice
    noticeList.addEventListener("click", (e) => {
        if (e.target.classList.contains("delete-notice")) {
            const noticeId = e.target.getAttribute("data-id");
            fetch(`/api/notices/${noticeId}`, { method: "DELETE" })
                .then((response) => {
                    if (!response.ok) throw new Error("Failed to delete notice");
                    return response.json();
                })
                .then(() => {
                    loadNotices(); // Reload the notice list
                    showPopup("Notice deleted successfully!"); // Show success message
                })
                .catch((error) => console.error("Error deleting notice:", error));
        }
    });

    // Load notices on page load
    loadNotices();
});
