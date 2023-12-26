// Search button click event
document.getElementById("search-button").addEventListener("click", function() {
  const searchInput = document.getElementById("search-input");
  const query = searchInput.value.trim();
  if (query !== "") {
    // Show the spinner while waiting for the API response
    const spinner = document.getElementById("spinner");
    spinner.style.display = "block";

    // Call the API function
    askPolicyA(query);
  }
});

document.getElementById("web-button").addEventListener("click", function() {
  const searchInput = document.getElementById("search-input");
  const query = searchInput.value.trim();
  if (query !== "") {
    // Show the spinner while waiting for the API response
    const spinner = document.getElementById("spinner");
    spinner.style.display = "block";

    // Call the API function
    askPolicyB(query);
  }
});

// Function to ask the city and display the response in the card
function askPolicyA(query) {
  const url = `/policy/query/neurolitiks/?query=${encodeURIComponent(query)}`;
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

      // Hide the spinner after the API response is received
      const spinner = document.getElementById("spinner");
      spinner.style.display = "none";
    })
    .catch(error => {
      console.log('Error in policy query:', error);
      // Hide the spinner on error as well
      const spinner = document.getElementById("spinner");
      spinner.style.display = "none";
    });
}

// Function to ask the city and display the response in the card
function askPolicyB(query) {
  const url = `/policy/query/web/?query=${encodeURIComponent(query)}`;
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

      // Hide the spinner after the API response is received
      const spinner = document.getElementById("spinner");
      spinner.style.display = "none";
    })
    .catch(error => {
      console.log('Error in policy query:', error);
      // Hide the spinner on error as well
      const spinner = document.getElementById("spinner");
      spinner.style.display = "none";
    });
}
