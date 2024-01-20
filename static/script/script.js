// Setup code editor variables
const codeEditor = document.getElementById("code-editor"); // Access the textarea element
let isTabIndented = false; // Flag to detect if the last action was a tab indentation
let codeHistory = [codeEditor.value]; // Initialize history with the current value of the editor
let historyIndex = 0; // Index to track the current position in history

// Event listener for handling tab keydown events in the code editor
codeEditor.addEventListener("keydown", function (event) {
  if (event.key === "Tab") { // Check if the Tab key was pressed
    event.preventDefault(); // Prevent the default tab key behavior
    handleTabIndentation(); // Add tab indentation at the cursor's position
  }
});

// Event listener for input changes in the code editor
codeEditor.addEventListener("input", function () {
  if (isTabIndented) { // If the last action was a tab indent
    isTabIndented = false; // Reset the flag as the input change was due to tab indent
  } else { // If the last action was not a tab indent
    saveCodeState(); // Save the new state to history for undo/redo functionality
  }
});

// Handles tab indentation
function handleTabIndentation() {
  const indentation = "    "; // Define four spaces as a tab
  const cursorPosition = codeEditor.selectionStart; // Get current cursor position

  // Insert the tab space at the current cursor position
  codeEditor.setRangeText(indentation, cursorPosition, cursorPosition, "end");

  // Move cursor position after the inserted tab space
  codeEditor.selectionStart = codeEditor.selectionEnd = cursorPosition + indentation.length;

  // Set the flag to true as tab was just inserted
  isTabIndented = true;
}

// Saves the current state of the code editor into the history array
function saveCodeState() {
  const currentCode = codeEditor.value; // Get current content of the code editor

  // If the current code is different from the latest saved state
  if (currentCode !== codeHistory[historyIndex]) {
    // Remove future states if any exist
    codeHistory = codeHistory.slice(0, historyIndex + 1);
    // Add the new state to history and increment the index to point to it
    codeHistory.push(currentCode);
    historyIndex++;
  }
}

// Global event listener for undo (Ctrl+Z) and redo (Ctrl+Y) keydown events
document.addEventListener("keydown", function (event) {
  if (event.ctrlKey && event.key === "z") { // If Ctrl+Z is pressed
    event.preventDefault(); // Prevent default browser undo action
    undo(); // Trigger undo action
  } else if (event.ctrlKey && event.key === "y") { // If Ctrl+Y is pressed
    event.preventDefault(); // Prevent default browser redo action
    redo(); // Trigger redo action
  }
});

// Undo the last action by reverting to the previous state in the history array
function undo() {
  if (historyIndex > 0) { // Ensure there is a previous state to revert to
    historyIndex--; // Move back one position in the history array
    // Set the code editor's value to the previous state
    codeEditor.value = codeHistory[historyIndex];
  }
}

// Redo an action by applying the next state in the history array
function redo() {
  if (historyIndex < codeHistory.length - 1) { // Ensure there is a next state to apply
    historyIndex++; // Move forward one position in the history array
    // Set the code editor's value to the next state
    codeEditor.value = codeHistory[historyIndex];
  }
}

// Add code execution functionality
const runCodeBtn = document.querySelector('.run-code-btn');

runCodeBtn.addEventListener('click', function () {
  const code = codeEditor.value;

  fetch('/runcode', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ code: code }),
  })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        console.error(data.error);
      } else {
        console.log(data.result);

        // Update the output areas (replace with your own logic)
        lexicalAnalyzer.textContent = data.result.lexical;
        syntaxAnalyzer.textContent = data.result.syntax;
      }
    })
    .catch(error => console.error('Error:', error));
});