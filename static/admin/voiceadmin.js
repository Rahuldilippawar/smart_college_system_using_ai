const queryInput = document.getElementById('queryInput');
const responseInput = document.getElementById('responseInput');
const addQueryBtn = document.getElementById('addQueryBtn');

addQueryBtn.addEventListener('click', async () => {
    const query = queryInput.value.trim().toLowerCase();
    const response = responseInput.value.trim();
    const language = 'en-US';  // This can be dynamic based on your language selection

    if (query && response) {
        try {
            const res = await fetch('http://localhost:3000/add-query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query, response, language }),
            });
            const result = await res.text();
            alert(result);  // Show success or failure message
            queryInput.value = '';
            responseInput.value = '';
        } catch (error) {
            console.error('Error adding query:', error);
            alert('Failed to add query');
        }
    } else {
        alert('Please enter both query and response.');
    }
});
