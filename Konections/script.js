const tiles = document.querySelectorAll('.tile');
const message = document.getElementById('message');
const topRow = document.getElementById('top-row');
let selectedTiles = [];
let completedGroups = 0; // Track the number of completed groups
const totalGroups = 4; // Total number of groups to match

// Define group difficulty levels
const groupDifficulty = {
    fruit: 1, // Easiest
    animal: 2,
    instrument: 3,
    color: 4 // Hardest
};

tiles.forEach(tile => {
    tile.addEventListener('click', () => {
        if (!tile.classList.contains('selected')) {
            tile.classList.add('selected');
            selectedTiles.push(tile);
        }

        if (selectedTiles.length === 4) {
            checkSelection();
        }
    });
});

function checkSelection() {
    const groups = selectedTiles.map(tile => tile.dataset.group);
    const allSameGroup = groups.every(group => group === groups[0]);

    if (allSameGroup) {
        const group = groups[0];
        message.textContent = `正解！グループ: ${group} - 難易度: レベル${groupDifficulty[group]}`;
        message.style.color = 'green';
        moveToTopRow(group);
        completedGroups++; // Increment completed groups

        // Check if the game is complete
        if (completedGroups === totalGroups) {
            showConfetti();
            message.textContent = 'おめでとうございます！すべてのグループを完成しました！';
        }
    } else {
        message.textContent = '不正解！もう一度試してください。';
        message.style.color = 'red';
    }

    resetSelection();
}

function moveToTopRow(group) {
    selectedTiles.forEach(tile => {
        tile.classList.add('highlighted'); // Add special styling for confirmed tiles
        topRow.appendChild(tile); // Move tiles to the top row
    });

    selectedTiles = [];
}

function resetSelection() {
    setTimeout(() => {
        selectedTiles.forEach(tile => tile.classList.remove('selected'));
        selectedTiles = [];
    }, 1000);
}

// Function to show confetti
function showConfetti() {
    confetti({
        particleCount: 150,
        spread: 70,
        origin: { y: 0.6 }
    });
}