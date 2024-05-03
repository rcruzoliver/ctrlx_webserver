document.addEventListener('DOMContentLoaded', () => {  // Ensure the DOM is fully loaded
    const toggleButton = new Button('toggleButton', 'motion/axs/AxisX/cmd/power' ,(currentState) => {
        console.log(`Button is now: ${currentState}`);
    });
});

document.addEventListener('DOMContentLoaded', () => {  // Ensure the DOM is fully loaded
    const toggleButton2 = new Button('toggleButton2', 'motion/axs/AxisY/cmd/power', (currentState) => {
        console.log(`Button is now: ${currentState}`);
    });
});

document.addEventListener('DOMContentLoaded', () => {  // Ensure the DOM is fully loaded
    const toggleButton3 = new Button('toggleButton3', 'motion/axs/AxisZ/cmd/power',(currentState) => {
        console.log(`Button is now: ${currentState}`);
    });
});


const volumeSlider = document.getElementById('volumeSlider');

//volumeSlider.addEventListener('input', function() {

volumeSlider.addEventListener('change', function() {
    let value = volumeSlider.value;

    // Display the current value
    document.getElementById('volumeValue').textContent = value;

    // Construct URL with parameters
    let apiUrl = `/api/datalayer?data-path=plc/app/Application/sym/GVL/fFUSpeed`;

    // Send the value to the server
    fetch(apiUrl, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({value: value})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message); // Log the message from the server
    })
    .catch(error => {
        console.error('Error:', error);
    });

});

class Button {
    constructor(elementId, pathtoDL, onClick) {
        // Get the button element by its ID
        this.buttonElement = document.getElementById(elementId);

        // If the button element exists, add the click event listener
        if (this.buttonElement) {
            this.buttonElement.addEventListener('click', () => {
                this.toggleState();
                if (onClick) onClick(this.state);  // Call the provided callback
            });
        }

        // Initial state of the button
        this.state = 'not-clicked';

        // path to datalayer
        this.apiUrl = '/api/datalayer?data-path=' + pathtoDL;
    }

    // Method to toggle the button's state
    toggleState() {
        if (this.state === 'not-clicked') {

            // Send the value to the server
            fetch(this.apiUrl, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({value: true})
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.message); // Log the message from the server
                this.state = 'clicked';
                this.buttonElement.textContent = 'Ein';
                this.buttonElement.setAttribute('data-state', 'clicked');
            })
            .catch(error => {
                console.error('Error:', error);
            });
            
            
        } else {

            // Send the value to the server
            fetch(this.apiUrl, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({value: false})
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.message); // Log the message from the server
            this.state = 'not-clicked';
            this.buttonElement.textContent = 'Aus';
            this.buttonElement.setAttribute('data-state', 'not-clicked');
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    }
}
