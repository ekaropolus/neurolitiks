// Search button click event
document.getElementById("search-button").addEventListener("click", function() {
  const searchInput = document.getElementById("search-input");
  const query = searchInput.value.trim();
  if (query !== "") {
    // Show the spinner while waiting for the API response
    const spinner = document.getElementById("spinner");
    spinner.style.display = "block";

    // Call the API function
    getPolicyAI(query);
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

// Modified getPolicyAI function to include agent response and answer details
function getPolicyAI(query) {
  const spinner = document.getElementById("spinner");
  spinner.style.display = "block";

  // Call the /policy/query/neurolitiks/ endpoint to get policy_id
  fetch(`/policy/query/neurolitiks/?query=${encodeURIComponent(query)}`)
    .then(response => response.json())
    .then(data => {
      spinner.style.display = "none";

      const searchResponseText = document.getElementById('search-response-text');
      if (data.error) {
        searchResponseText.innerHTML += `<p>Error: ${data.error}</p>`;
        return;
      }

      const policyId = data.policy_id;

      // Fetch response from getPolicyQuery function
      getPolicyQuery(policyId)
        .then(queryText => {
          searchResponseText.innerHTML += `<p>Policy ID: ${policyId}</p>`;
          searchResponseText.innerHTML += `<p>Query: ${queryText}</p>`;
        })
        .catch(error => {
          console.error('Error in fetching policy query:', error);
        });

      // Fetch response from getPolicyAnswer function
      getPolicyAnswer(policyId)
        .then(answerData => {
          // Display answer details in respective card elements
          const goalCard = document.getElementById('goal-card');
          const targetCard = document.getElementById('target-card');
          const indicatorCard = document.getElementById('indicator-card');

          if (answerData.goal) {
            goalCard.innerHTML = `<i class="material-icons">emoji_events</i> Policy Goal`;
            goalCard.nextElementSibling.innerHTML = answerData.goal;
          }

          if (answerData.target) {
            targetCard.innerHTML = `<i class="material-icons">location_on</i> Policy Target`;
            targetCard.nextElementSibling.innerHTML = answerData.target;
          }

          if (answerData.indicator) {
            indicatorCard.innerHTML = `<i class="material-icons">show_chart</i> Policy Indicator`;
            indicatorCard.nextElementSibling.innerHTML = answerData.indicator;
          }
        })
        .catch(error => {
          console.error('Error in fetching policy answer:', error);
        });

      // Fetch response from getPolicyResponse function
      getPolicyResponse(policyId)
        .then(responseText => {
          searchResponseText.innerHTML += `<p>Response: ${responseText}</p>`;
        })
        .catch(error => {
          console.error('Error in fetching policy response:', error);
        });

      // Fetch response from getAgentResponse function
      getAgentResponse(policyId)
        .then(agentResponseText => {
          searchResponseText.innerHTML += `<p>Agent Response: ${agentResponseText}</p>`;
        })
        .catch(error => {
          console.error('Error in fetching agent response:', error);
        });

      // Fetch and display lemmas and syncons
      getLemas(policyId);
      getSyncons(policyId);

    })
    .catch(error => {
      spinner.style.display = "none";
      console.error('Error in policy query:', error);
    });
}



// Function to get the query for a specific policy_id
function getPolicyQuery(policyId) {
  const url = `/policy/query/${policyId}/query/`;
  return fetch(url, { method: 'GET' })
    .then(response => response.json())
    .then(data => {
      return data.query;
    })
    .catch(error => {
      console.error('Error getting policy query:', error);
      return null;
    });
}

// Function to get the response for a specific policy_id
function getPolicyResponse(policyId) {
  const url = `/policy/query/${policyId}/response/`;
  return fetch(url, { method: 'GET' })
    .then(response => response.json())
    .then(data => {
      return data.response;
    })
    .catch(error => {
      console.error('Error getting policy response:', error);
      return null;
    });
}

// Function to get the answer for a specific policy_id
function getPolicyAnswer(policyId) {
  const url = `/policy/query/${policyId}/answer/`;
  return fetch(url, { method: 'GET' })
    .then(response => response.json())
    .then(data => {
      return data.answer;
    })
    .catch(error => {
      console.error('Error getting policy answer:', error);
      return null;
    });
}

// Function to get the lemmas for a specific policy_id
function getPolicyLemmas(policyId) {
  const url = `/policy/query/${policyId}/lemmas/`;
  return fetch(url, { method: 'GET' })
    .then(response => response.json())
    .then(data => {
      return data.lemas;
    })
    .catch(error => {
      console.error('Error getting policy lemmas:', error);
      return null;
    });
}

// Function to get the syncoms for a specific policy_id
function getPolicySyncoms(policyId) {
  const url = `/policy/query/${policyId}/syncoms/`;
  return fetch(url, { method: 'GET' })
    .then(response => response.json())
    .then(data => {
      return data.syncons;
    })
    .catch(error => {
      console.error('Error getting policy syncoms:', error);
      return null;
    });
}

// Function to get agent response for a specific policy ID
function getAgentResponse(policyId) {
  const url = `/policy/query/${policyId}/agent_response/`;
  return fetch(url, { method: 'GET' })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        return `Error: ${data.error}`;
      }
      return data.agent_response;
    })
    .catch(error => {
      console.error('Error fetching agent response:', error);
      return `Error: ${error.message}`;
    });
}

// Function to fetch and display lemmas for a specific policy
function getLemas(policyId) {
  // Make a GET request to the server endpoint for lemmas
  fetch(`/policy/query/${policyId}/lemmas/`, { method: 'GET' })
    .then(response => response.json())
    .then(data => {
      const lemasContainer = document.getElementById('lemas-container');
      lemasContainer.innerHTML = ''; // Clear previous data

      if (data.error) {
        lemasContainer.textContent = `Error: ${data.error}`;
      } else {
        // Display lemmas data
        data.lemmas.forEach(lemma => {
          const lemmaDescription = lemma.description;
          const lemmaGroup = lemma.group;
          const lemmaId = lemma.id;
          const lemmaText = lemma.lemma;

          lemasContainer.innerHTML += `
            <div class="lemma-item">
              <p>Description: ${lemmaDescription}</p>
              <p>Group: ${lemmaGroup}</p>
              <p>ID: ${lemmaId}</p>
              <p>Lemma: ${lemmaText}</p>
            </div>
          `;
        });
      }
    })
    .catch(error => {
      console.error('Error fetching lemmas:', error);
    });
}

// Function to fetch and display syncons for a specific policy
function getSyncons(policyId) {
  // Make a GET request to the server endpoint for syncons
  fetch(`/policy/query/${policyId}/syncons/`, { method: 'GET' })
    .then(response => response.json())
    .then(data => {
      const synconsContainer = document.getElementById('syncons-container');
      synconsContainer.innerHTML = ''; // Clear previous data

      if (data.error) {
        synconsContainer.textContent = `Error: ${data.error}`;
      } else {
        // Display syncons data
        data.syncons.forEach(syncon => {
          const synconDescription = syncon.description;
          const synconGroup = syncon.group;
          const synconId = syncon.id;
          const synconText = syncon.lemma;

          synconsContainer.innerHTML += `
            <div class="syncon-item">
              <p>Description: ${synconDescription}</p>
              <p>Group: ${synconGroup}</p>
              <p>ID: ${synconId}</p>
              <p>Syncon: ${synconText}</p>
            </div>
          `;
        });
      }
    })
    .catch(error => {
      console.error('Error fetching syncons:', error);
    });
}
