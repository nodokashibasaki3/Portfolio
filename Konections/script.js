// DOM Elements
const tiles = document.querySelectorAll('.tile');
const message = document.getElementById('message');
const topRow = document.getElementById('top-row');
const selectionCounter = document.getElementById('counter');
const progressIndicator = document.querySelector('.progress-indicator');
const progressText = document.querySelector('.progress-text');
const resetButton = document.getElementById('reset-button');

// Game state
let selectedTiles = [];
let completedGroups = 0;
const totalGroups = 4;

// Define group names and difficulty levels
const groupInfo = {
    fruit: { 
        name: 'フルーツ', 
        difficulty: 1,
        color: 'group-fruit'
    },
    animal: { 
        name: '動物', 
        difficulty: 2,
        color: 'group-animal'
    },
    instrument: { 
        name: '楽器', 
        difficulty: 3,
        color: 'group-instrument'
    },
    color: { 
        name: '色', 
        difficulty: 4,
        color: 'group-color'
    }
};

// Initialize game
function initGame() {
    // Shuffle tiles
    shuffleTiles();
    
    // Add event listeners to tiles
    tiles.forEach(tile => {
        tile.addEventListener('click', handleTileClick);
    });
    
    // Reset button functionality
    resetButton.addEventListener('click', resetGame);
    
    // Update UI
    updateProgressBar();
    updateCounter();
}

// Shuffle tiles
function shuffleTiles() {
    const grid = document.getElementById('grid');
    const tilesArray = Array.from(tiles);
    
    // Fisher-Yates shuffle algorithm
    for (let i = tilesArray.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [tilesArray[i].style.order, tilesArray[j].style.order] = 
        [tilesArray[j].style.order, tilesArray[i].style.order];
    }
}

// Handle tile click
function handleTileClick() {
    // Ignore click if tile is already selected or has been completed
    if (this.classList.contains('selected') || this.parentNode.classList.contains('completed-group')) {
        return;
    }
    
    // Select tile
    this.classList.add('selected');
    selectedTiles.push(this);
    
    // Update selection counter
    updateCounter();
    
    // Check if 4 tiles are selected
    if (selectedTiles.length === 4) {
        checkSelection();
    }
}

// Check if selection forms a valid group
function checkSelection() {
    const groups = selectedTiles.map(tile => tile.dataset.group);
    const allSameGroup = groups.every(group => group === groups[0]);
    
    if (allSameGroup) {
        handleCorrectSelection(groups[0]);
    } else {
        handleIncorrectSelection();
    }
}

// Handle correct selection
function handleCorrectSelection(group) {
    // Update message
    message.textContent = `正解！「${groupInfo[group].name}」のグループを見つけました！`;
    message.style.color = 'var(--success-color)';
    
    // Move tiles to top row
    moveToTopRow(group);
    
    // Update progress
    completedGroups++;
    updateProgressBar();
    
    // Check if game is complete
    if (completedGroups === totalGroups) {
        showGameComplete();
    }
}

// Handle incorrect selection
function handleIncorrectSelection() {
    message.textContent = '不正解！もう一度試してください。';
    message.style.color = 'var(--error-color)';
    
    // Add shake animation to selected tiles
    selectedTiles.forEach(tile => {
        tile.style.animation = 'shake 0.5s';
        setTimeout(() => {
            tile.style.animation = '';
        }, 500);
    });
    
    // Reset selection
    resetSelection();
}

// Move a completed group to the top row
function moveToTopRow(group) {
    // Create a container for the group
    const groupContainer = document.createElement('div');
    groupContainer.className = `completed-group ${groupInfo[group].color}-bg`;
    
    // Add the group name to the container
    const groupName = document.createElement('div');
    groupName.className = 'group-title';
    groupName.textContent = groupInfo[group].name;
    groupContainer.appendChild(groupName);
    
    // Add the tile words to the container
    const wordContainer = document.createElement('div');
    wordContainer.className = 'group-words';
    
    // Get all words from selected tiles
    const words = selectedTiles.map(tile => tile.textContent);
    wordContainer.textContent = words.join('・');
    
    groupContainer.appendChild(wordContainer);
    
    // Add the container to the top row
    topRow.appendChild(groupContainer);
    
    // Hide the original tiles from the main grid
    selectedTiles.forEach(tile => {
        tile.style.display = 'none';
    });
    
    // Clear selection
    selectedTiles = [];
    updateCounter();
}

// Reset the current selection
function resetSelection() {
    setTimeout(() => {
        selectedTiles.forEach(tile => {
            tile.classList.remove('selected');
        });
        selectedTiles = [];
        updateCounter();
    }, 1000);
}

// Update selection counter
function updateCounter() {
    selectionCounter.textContent = `${selectedTiles.length}/4`;
}

// Update progress bar
function updateProgressBar() {
    const progressPercentage = (completedGroups / totalGroups) * 100;
    progressIndicator.style.width = `${progressPercentage}%`;
    progressText.textContent = `${completedGroups}/${totalGroups}`;
}

// Show game complete state
function showGameComplete() {
    message.textContent = 'おめでとうございます！すべてのグループを完成しました！';
    message.className = 'message winning-message';
    showConfetti();
    resetButton.textContent = '新しいゲーム';
}

// Reset game
function resetGame() {
    // Reset state
    selectedTiles = [];
    completedGroups = 0;
    
    // Reset UI
    message.textContent = '選択してグループを見つけてください！';
    message.style.color = 'var(--dark-gray)';
    message.className = 'message';
    updateProgressBar();
    updateCounter();
    
    // Clear top row
    topRow.innerHTML = '';
    
    // Reset tiles
    tiles.forEach(tile => {
        tile.classList.remove('selected');
        tile.style.display = ''; // Make tiles visible again
        tile.style.order = ''; // Reset order
    });
    
    // Shuffle tiles
    shuffleTiles();
    
    // Reset button text
    resetButton.textContent = 'リセット';
}

// Show confetti animation
function showConfetti() {
    confetti({
        particleCount: 150,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#fd79a8', '#6c5ce7', '#00b894', '#fdcb6e', '#e17055']
    });
    
    // Additional confetti bursts
    setTimeout(() => {
        confetti({
            particleCount: 50,
            angle: 60,
            spread: 55,
            origin: { x: 0 }
        });
    }, 500);
    
    setTimeout(() => {
        confetti({
            particleCount: 50,
            angle: 120,
            spread: 55,
            origin: { x: 1 }
        });
    }, 900);
}

// Add shake animation for incorrect selections
document.head.insertAdjacentHTML('beforeend', `
    <style>
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
            20%, 40%, 60%, 80% { transform: translateX(5px); }
        }
    </style>
`);

// Initialize the game when the page loads
window.addEventListener('load', initGame);