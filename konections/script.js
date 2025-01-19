const words = [
  "絆", "影", "夢", "鏡",
  "種", "雨", "時間", "風",
  "ドア", "窓", "本", "ノート",
  "バッテリー", "食事", "休憩", "水"
];

const correctGroups = {
  '見えない力': { words: ["絆", "影", "夢", "鏡"], difficulty: 'easy' },
  '成長の要素': { words: ["種", "雨", "時間", "風"], difficulty: 'medium' },
  '開けるもの': { words: ["ドア", "窓", "本", "ノート"], difficulty: 'hard' },
  'エネルギー補給': { words: ["バッテリー", "食事", "休憩", "水"], difficulty: 'extreme' }
};

let selectedWords = [];
let remainingWords = [...words];
let wrongGuesses = 0; 
const maxGuesses = 4; 

function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

function initWords() {
  const container = document.getElementById("randomWords");
  container.innerHTML = ''; 
  shuffle(remainingWords); 
  remainingWords.forEach(word => {
    const div = document.createElement("div");
    div.className = "word";
    div.textContent = word;
    div.onclick = () => selectWord(word, div);
    container.appendChild(div);
  });
  updateGuessesLeft(); 
}

function selectWord(word, div) {
  if (selectedWords.includes(word)) {
    selectedWords = selectedWords.filter(w => w !== word);
    div.classList.remove("selected");
  } else if (selectedWords.length < 4) {
    selectedWords.push(word);
    div.classList.add("selected");
  }
  updateFinalizeButtonState();
}

function updateFinalizeButtonState() {
  const finalizeButton = document.getElementById("finalizeButton");
  finalizeButton.disabled = selectedWords.length !== 4;
}

function displayCorrectGroup(groupName, difficulty) {
  const wordsContainer = document.getElementById("randomWords");
  const container = document.createElement("div");
  container.className = `groupContainer ${difficulty}`; 
  
  const groupDiv = document.createElement("div");
  groupDiv.className = "correctGroup";
  groupDiv.textContent = groupName;
  container.appendChild(groupDiv);

  const answersDiv = document.createElement("div");
  answersDiv.className = "answers";
  correctGroups[groupName].words.forEach(word => {
    const wordDiv = document.createElement("div");
    wordDiv.className = "answer";
    wordDiv.textContent = word;
    answersDiv.appendChild(wordDiv);
    remainingWords = remainingWords.filter(w => w !== word); 
  });
  container.appendChild(answersDiv);

  wordsContainer.before(container); 
}

function updateGuessesLeft() {
  const guessesLeftElement = document.getElementById("guessesLeft");
  guessesLeftElement.textContent = `間違えた回数: ${maxGuesses - wrongGuesses}`;
}

function showMessage(msg, isError = false) {
  const messageElement = document.getElementById("message");
  messageElement.textContent = msg;
  messageElement.style.display = 'block'; 
  if (isError) {
    setTimeout(() => {
      messageElement.style.display = 'none';
    }, 2000);
  }
}

function disableAllButtons() {
  document.querySelectorAll('button, input[type="submit"], input[type="button"], a').forEach(element => {
    element.disabled = true; 
    element.style.pointerEvents = 'none';
  });
  console.log("All buttons should now be disabled.");
}

function showGameOver() {
  const gameOverPopup = document.getElementById("gameOverPopup");
  gameOverPopup.style.display = 'block';

  disableAllButtons();

  const words = document.querySelectorAll(".word");
  words.forEach(word => {
    word.style.pointerEvents = 'none';
  });
}

document.getElementById("finalizeButton").onclick = () => {
  const groupName = Object.keys(correctGroups).find(name =>
    correctGroups[name].words.every(word => selectedWords.includes(word))
  );

  if (groupName) {
    const difficulty = correctGroups[groupName].difficulty;
    displayCorrectGroup(groupName, difficulty);
    selectedWords = [];
    initWords(); 
    showMessage('Correct group!', false);
  } else {
    wrongGuesses++;
    updateGuessesLeft();
    if (wrongGuesses >= maxGuesses) {
      showGameOver();
    } else {
      showMessage('違います', true);
    }
  }

  updateFinalizeButtonState();
};

window.onload = initWords;
