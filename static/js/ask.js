// Search button click event
document.getElementById("search-button").addEventListener("click", function() {
  const searchInput = document.getElementById("search-input");
  const query = searchInput.value.trim();
  if (query !== "") {
    askPolicy(query);
  }
});

// Function to ask the city and display the response in the card
function askPolicy(query) {
  const url = `/policy/query/?query=${encodeURIComponent(query)}`;
  fetch(url, { method: 'GET' })
    .then(response => response.json())
    .then(response => {
      const searchResponseText = document.getElementById('search-response-text');
      const searchResponseCard = document.getElementById('search-response-card');

      if (response.error) {
        searchResponseText.textContent = `Error: ${response}`;
      } else {
        searchResponseText.textContent = `Response: ${response}`;
      }


    })
    .catch(error => console.log('Error in policy query:', error));
}