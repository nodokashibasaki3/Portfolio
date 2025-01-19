let noClickCount = 0;

const noButtonTextVariations = [
    "Are you sure?",
    "Maybe you misunderstood",
    "Good thing I believe in second chances!",
    "Lost in translation, maybe?",
    "Maybe a WiFi issue?",
    "Your cat? bruh",
    "I think we should get a second opinion",
    "Now you're just chasing this for funzies",
    "This will never end",
    "Yes",
    "Why did you still try to click it when it said YES",
    "I knew you liked me",
    "So like why aren't you clicking the other one",
    "I AM WAITING",
    "...",
    "I AM RUNNING OUT OF COMMENTARY"
];
// To track which text variation to show next
let currentVariationIndex = 0;

document.addEventListener('DOMContentLoaded', function() {
    
    const noBtn = document.getElementById('noBtn');
    noBtn.addEventListener('mouseover', handleNoHover);
    noBtn.addEventListener('click', handleNoClick);

    setupInitialEventListeners();

});

function setupInitialEventListeners() {
    document.getElementById('yesBtn').addEventListener('click', handleYesClick);
    document.getElementById('noBtn').addEventListener('mouseover', handleNoHover);
}

function handleYesClick() {
    const valentineDiv = document.getElementById('valentineContent'); // Main content div

    // Clear existing content
    valentineDiv.innerHTML = '';

    // Create and display the thank you message
    const thankYouMessage = document.createElement('h2');
    thankYouMessage.innerHTML = 'Thank you for choosing to be Nodoka\'s Valentine 2024! 🎉';
    valentineDiv.appendChild(thankYouMessage);

    thankYouMessage.style.textAlign = 'center';
    thankYouMessage.style.marginTop = '20px';
}

function handleNoHover() {
    noClickCount++;
    
    // For the first 5 hovers, just move the "No" button
    if (noClickCount <= 5) {
        moveNoButton();
    }
    // After 5 hovers, show the surprise if it hasn't been shown yet
    else if (noClickCount === 6) {
        showSurprise();
        // After showing the surprise, prepare for the next hover interactions
    } else {
        // Make "Yes" button bigger and "No" button smaller, and change "No" button text
        changeButtonStylesAndText();
        moveNoButton();
    }

}

function handleNoClick() {
    if (noClickCount > 5) {
        alert("Error Code 302: Temporarily Moved to Denial. Please try your rejection again later.");
        // Here, call showSurprise or any function you want to proceed with
        showSurprise();
    }
}

function moveNoButton() {
    const noBtn = document.getElementById('noBtn');
    noBtn.style.position = 'absolute';
    noBtn.style.top = Math.random() * (window.innerHeight - noBtn.offsetHeight) + 'px';
    noBtn.style.left = Math.random() * (window.innerWidth - noBtn.offsetWidth) + 'px';
}


function showSurprise() {
    const valentineDiv = document.getElementById('valentineContent'); // Ensure this is the correct ID for your Valentine content div
    valentineDiv.innerHTML = '<h2>I admire your persistence! 💖</h2><p>Does this super cute animated heart change your mind?</p>';

    const heartImg = document.createElement('img');
    heartImg.src = 'pixelheart.png';
    heartImg.id = 'heartImg';
    heartImg.style.display = 'block';
    valentineDiv.appendChild(heartImg);

    setTimeout(addButtons, 2000);
}

function addButtons() {
    const valentineDiv = document.getElementById('valentineContent'); // Re-using the same Valentine content div

    // Remove old buttons if they exist
    removeElement('yesBtn');
    removeElement('noBtn');

    // Create and append new "Yes" and "No" buttons
    const yesBtn = document.createElement('button');
    yesBtn.id = 'yesBtn';
    yesBtn.textContent = 'Yes';
    yesBtn.addEventListener('click', handleYesClick);
    valentineDiv.appendChild(yesBtn);

    const noBtn = document.createElement('button');
    noBtn.id = 'noBtn';
    noBtn.textContent = 'No';
    // This time, attach handleNoHover to ensure it works after adding new buttons
    noBtn.addEventListener('mouseover', handleNoHover);
    valentineDiv.appendChild(noBtn);
}

function changeButtonStylesAndText() {
    const valentineDiv = document.getElementById('valentineContent');
    const yesBtn = document.getElementById('yesBtn');
    const noBtn = document.getElementById('noBtn');

    let yesFontSize = parseFloat(window.getComputedStyle(yesBtn, null).getPropertyValue('font-size'));
    yesFontSize += 5; // Increase "Yes" button font size more significantly
    yesBtn.style.fontSize = `${yesFontSize}px`;

    if (currentVariationIndex < noButtonTextVariations.length) {
        // Change the "No" button text to the next variation
        noBtn.textContent = noButtonTextVariations[currentVariationIndex++];
    } else {
        // After all variations are shown, show defeat message and a "Maybe" button
        valentineDiv.innerHTML = '<h2>I accept defeat...</h2><p>But maybe there\'s still a chance?</p>';
        showDefeatMessage()
    }
}

function handleMaybeClick() {
    const valentineDiv = document.getElementById('valentineContent'); // Main content div

    // Clear existing content
    valentineDiv.innerHTML = '';

    // Create and display the whimsical explanation
    const maybeExplanation = document.createElement('p');
    maybeExplanation.innerHTML = `
        <h2>What does a maybe mean????</h2>
        <p>In the vast expanse of choices, where 'Yes' means certainty and 'No' means denial, there lies 'Maybe'. With endless possibilities, where the quantum states of 'Yes' and 'No' coalesce into a superposition of potentiality.</p>
        <p>'Maybe' is not merely a lack of decision, but a gateway to infinite outcomes---AN ESCAPE. It's the Schrödinger's Cat of responses. Heisenberg's Uncertainty Principle in quantum mechanics. Alive with every 'Yes' that could be, and every 'No' that might not happen. I simply do not make the rules. In this liminal space, 'Maybe' hints the promise of 'Yes' with the probabilities until the universe collapses into a single outcome. KABOOM.</p>
        <p>So, a 'Maybe' is merely the universe's way of saying, 'Why not explore the possibility?'. For the deep definition of 'Maybe' lies the curiosity and attentiveness to 'Yes.'</p>
        <p>And so, in the HUGE cosmic of choices given, 'Maybe' is only a whisper away from the resounding the simple three letter word...'Yes'. Because, in the end, every 'Maybe' holds the seed of a 'Yes', waiting for the right moment to go bloom.</p>
        <p>Thus, your 'Maybe' is my 'Yes,' and you are my valentine.</p><p></p>
        <p>XOXO, </p><p>Non</p>
    `;
    valentineDiv.appendChild(maybeExplanation);

    // Apply styles to the explanation and button if needed
    maybeExplanation.style.textAlign = 'justify';
    maybeExplanation.style.margin = '20px';
    backButton.style.display = 'block';
    backButton.style.margin = '20px auto';
    backButton.style.padding = '10px 20px';
    backButton.style.fontSize = '1em';
}

function showDefeatMessage() {
    // Remove old "Yes" and "No" buttons if they exist
    removeElement('yesBtn');
    removeElement('noBtn');

    const valentineDiv = document.getElementById('valentineContent'); // Assuming this is your main content div

    // Clear existing content and display the defeat message
    valentineDiv.innerHTML = '<h2>I accept defeat...</h2><p>But maybe there\'s still a chance?</p>';

    // Create and append a "Maybe" button
    const maybeBtn = document.createElement('button');
    maybeBtn.id = 'maybeBtn';
    maybeBtn.textContent = 'Maybe';
    maybeBtn.addEventListener('click', handleMaybeClick);
    valentineDiv.appendChild(maybeBtn);
    
    // Create and append a "Yes" button next to the "Maybe" button
    const yesBtn = document.createElement('button');
    yesBtn.id = 'yesBtn';
    yesBtn.textContent = 'Yes!';
    valentineDiv.appendChild(yesBtn);

    // Style the buttons if needed (you can add CSS classes or directly apply styles)
    maybeBtn.style.marginRight = '10px'; // Example of direct styling
}

function removeElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.parentNode.removeChild(element);
    }
}

// setting up the click event listener
document.getElementById('yesBtn').addEventListener('click', function() {
    showFinalThankYou();
});
document.getElementById('noBtn').addEventListener('mouseover', handleNoHover);
