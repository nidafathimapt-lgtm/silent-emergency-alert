const btn = document.getElementById('emergency-btn');
const statusText = document.getElementById('status-text');

btn.addEventListener('click', async () => {
    // 1. Visual Feedback
    btn.classList.add('active');
    btn.innerText = 'SENDING...';
    statusText.innerText = 'Activating Emergency Protocols...';

    // 2. Get Location & Send Alert
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(sendAlert, handleError, {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0
        });
    } else {
        alert("Geolocation is not supported by this browser.");
        sendAlert(null); // Try sending without location
    }
});

// Load saved contact on startup
window.addEventListener('load', () => {
    const savedContact = localStorage.getItem('trustedContact');
    if (savedContact) {
        document.getElementById('trusted-contact').value = savedContact;
    }
});

// Check for correct protocol
window.addEventListener('load', () => {
    if (window.location.protocol === 'file:') {
        alert("CRITICAL ERROR: You are running this file directly. You must open 'http://127.0.0.1:5000' in your browser to use the app.");
        statusText.innerText = "Error: Open http://127.0.0.1:5000";
        statusText.style.color = 'red';
        btn.disabled = true;
    }
});

function sendAlert(position) {
    const contactInput = document.getElementById('trusted-contact');
    const contact = contactInput.value;

    // Save contact for next time
    if (contact) {
        localStorage.setItem('trustedContact', contact);
    }

    const data = {
        message: "SILENT DISTRESS SIGNAL ACTIVATED",
        latitude: position ? position.coords.latitude : null,
        longitude: position ? position.coords.longitude : null,
        trusted_contact: contact
    };

    fetch('/alert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(async response => {
            const isJson = response.headers.get('content-type')?.includes('application/json');
            const data = isJson ? await response.json() : null;

            if (!response.ok) {
                // get error message from body or default to response status
                const error = (data && data.message) || response.statusText;
                return Promise.reject(new Error(error));
            }
            return data;
        })
        .then(data => {
            console.log('Success:', data);

            if (!data) {
                throw new Error("Empty response from server");
            }

            // Update UI to show success
            btn.innerText = 'SENT';
            statusText.innerText = 'Alert Successfully Sent!';
            statusText.style.color = '#4caf50'; // Green
            btn.classList.add('success'); // Add success style class
            btn.classList.remove('active');

            // Revert button state after some time
            setTimeout(() => {
                btn.innerText = 'SOS';
                statusText.innerText = 'Ready';
                statusText.style.color = '';
                btn.classList.remove('success');
            }, 5000);
        })


        .catch((error) => {
            console.error('Error:', error);
            statusText.innerText = `Error: ${error.message}`;
            statusText.style.color = '#ff5252'; // Red
            btn.innerText = 'SOS'; // Reset text
            btn.classList.remove('active');
        });
}

function handleError(error) {
    console.warn(`Geolocation error (${error.code}): ${error.message}`);
    // Send alert anyway, even if location failed
    sendAlert(null);
}


