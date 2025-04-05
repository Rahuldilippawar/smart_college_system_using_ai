document.addEventListener("DOMContentLoaded", () => {
    const dashboardButton = document.getElementById("dashboardButton");
    const manageUsersButton = document.getElementById("manageUsersButton");
    const settingsButton = document.getElementById("settingsButton");

    const dashboardSection = document.getElementById("dashboardSection");
    const manageUsersSection = document.getElementById("manageUsersSection");
    const settingsSection = document.getElementById("settingsSection");

    // Function to toggle sections
    function showSection(section) {
        dashboardSection.style.display = "none";
        manageUsersSection.style.display = "none";
        settingsSection.style.display = "none";

        section.style.display = "block";
    }

    // Add event listeners to navigation buttons
    dashboardButton.addEventListener("click", () => showSection(dashboardSection));
    manageUsersButton.addEventListener("click", () => showSection(manageUsersSection));
    settingsButton.addEventListener("click", () => showSection(settingsSection));

    // Fetch Dashboard Data
    const fetchDashboardData = () => {
        fetch("/api/dashboard") // Replace with your actual API endpoint
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                document.getElementById("userCount").textContent = data.totalUsers || "0";
                document.getElementById("noticeCount").textContent = data.activeNotices || "0";
            })
            .catch((error) => {
                console.error("Error fetching dashboard data:", error);
                document.getElementById("userCount").textContent = "Error";
                document.getElementById("noticeCount").textContent = "Error";
            });
    };

   

    
});
