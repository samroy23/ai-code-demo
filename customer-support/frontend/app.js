document.getElementById("queryForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const query = document.getElementById("query").value;
    
    fetch("/api/customer-service", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        let resultHTML = `<h3>Response:</h3><p>${data.response}</p>`;
        if (data.escalated) {
            resultHTML += `<p style="color:#ff6b6b;">This query was escalated to human support.</p>`;
            if(data.notification) {
                resultHTML += `<p>Notification Status: ${data.notification}</p>`;
            }
        }
        // Add thumbs up and thumbs down buttons for feedback
        resultHTML += `
            <div class="feedback-buttons">
                <span class="thumb" id="thumbUp">👍</span>
                <span class="thumb" id="thumbDown">👎</span>
            </div>
        `;
        document.getElementById("response").innerHTML = resultHTML;
        
        // Set up feedback handlers
        document.getElementById("thumbUp").addEventListener("click", function() {
            sendFeedback(query, data.response, "positive");
        });
        document.getElementById("thumbDown").addEventListener("click", function() {
            sendFeedback(query, data.response, "negative");
        });
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("response").innerHTML = "<p>Error occurred.</p>";
    });
});

function sendFeedback(query, ai_response, feedback) {
    fetch("/api/feedback", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: query, ai_response: ai_response, feedback: feedback })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Feedback response:", data);
        // Optionally, display a thank you message or update UI
        alert("Thank you for your feedback!");
    })
    .catch(error => {
        console.error("Error submitting feedback:", error);
    });
}
