document.addEventListener("DOMContentLoaded", function() {
    // Example API response
    const itineraryData = {
        destination: "Delhi",
        days: [
            {
                day: 1,
                activities: "Visit Red Fort and India Gate"
            },
            {
                day: 2,
                activities: "Explore Humayun's Tomb and Lotus Temple"
            }
        ]
    };

    // Function to display itinerary with animations
    function displayItinerary(data) {
        const itinerarySection = document.getElementById('itinerary');

        let content = `<h2>Your Itinerary for ${data.destination}</h2>`;

        data.days.forEach(day => {
            content += `
                <h3>Day ${day.day}</h3>
                <p>${day.activities}</p>
            `;
        });

        itinerarySection.innerHTML = content;

        // Trigger animation
        const items = itinerarySection.querySelectorAll('h2, h3, p');
        items.forEach((item, index) => {
            item.style.animationDelay = `${index * 0.2}s`;
        });
    }

    // Simulate delay for API response
    setTimeout(() => {
        displayItinerary(itineraryData);
    }, 500);
});
