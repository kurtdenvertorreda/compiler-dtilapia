// Get the code editor element from the DOM
const codeEditor = document.getElementById("code-editor");
// Flag to track if the last input was a tab indentation
let isTabIndented = false;
// Array to store the history of code for undo/redo functionality
let codeHistory = [codeEditor.value];
// Index to keep track of the current state in the history array
let historyIndex = 0;

// Event listener for keydown events in the code editor
codeEditor.addEventListener("keydown", function (event) {
  // If the Tab key is pressed
  if (event.key === "Tab") {
    event.preventDefault(); // Prevent the default tab action
    handleTabIndentation(); // Call the function to handle tab indentation
  }
});

// Event listener for input events in the code editor
codeEditor.addEventListener("input", function () {
  // If the last input was a tab indentation, reset the flag
  if (isTabIndented) {
    isTabIndented = false;
  } else {
    // If not, save the current state of the code editor for undo/redo
    saveCodeState();
  }
});

// Function to handle tab indentation
function handleTabIndentation() {
  // Define the indentation as four spaces
  const indentation = "    ";
  const cursorPosition = codeEditor.selectionStart; // Get the current cursor position

  // Insert the indentation text at the current cursor position
  codeEditor.setRangeText(indentation, cursorPosition, cursorPosition, "end");

  // Update the cursor position after the indentation
  codeEditor.selectionStart = codeEditor.selectionEnd = cursorPosition + indentation.length;

  // Set the flag indicating that a tab was inserted
  isTabIndented = true;
}

// Function to save the current state of the code editor into history
function saveCodeState() {
  const currentCode = codeEditor.value; // Get the current code from the editor

  // If the current code is different from the last state, save it
  if (currentCode !== codeHistory[historyIndex]) {
    // Cut off the history if we're in the middle of the history stack and start a new branch
    codeHistory = codeHistory.slice(0, historyIndex + 1);
    // Add the current code to the history and increment the history index
    codeHistory.push(currentCode);
    historyIndex++;
  }
}

// Global event listener for keydown events to handle undo and redo
document.addEventListener("keydown", function (event) {
  if (event.ctrlKey && event.key === "z") { // If Ctrl+Z is pressed
    event.preventDefault(); // Prevent the default action
    undo(); // Call the undo function
  } else if (event.ctrlKey && event.key === "y") { // If Ctrl+Y is pressed
    event.preventDefault(); // Prevent the default action
    redo(); // Call the redo function
  }
});

// Function to undo the last action in the code editor
function undo() {
  if (historyIndex > 0) { // If there is a previous state in the history
    historyIndex--; // Decrement the history index
    // Update the code editor with the previous state
    codeEditor.value = codeHistory[historyIndex];
  }
}

// Function to redo an action in the code editor
function redo() {
  if (historyIndex < codeHistory.length - 1) { // If there is a next state in the history
    historyIndex++; // Increment the history index
    // Update the code editor with the next state
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