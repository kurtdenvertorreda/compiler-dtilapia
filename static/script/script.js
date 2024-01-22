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

function handleFile() {
  const fileInput = document.getElementById('inputfile');
  const codeEditor = document.getElementById('code-editor');

  const file = fileInput.files[0];

  if (file) {
    const fileName = file.name;
    const fileExtension = fileName.slice(((fileName.lastIndexOf(".") - 1 >>> 0) + 2));

    if (fileExtension.toLowerCase() === 'dtil') {
      const reader = new FileReader();

      reader.onload = function (e) {
        const content = e.target.result;
        codeEditor.value = content;
      };

      reader.readAsText(file, 'UTF-8');
    } else {
      codeEditor.value = "Error: Please select a valid .dtil file.";
      fileInput.value = ""; // Clear the file input
    }
  } else {
    codeEditor.value = "No file selected.";
  }
}

function executeCode() {
    const codeEditor = document.getElementById('code-editor');
    const code = codeEditor.value;

    fetch('/execute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: code }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);  // Log the received data

        const outputContainer = document.getElementById('output');
        const tableBody = document.querySelector('.styled-table tbody');

        if (data.error) {
            outputContainer.textContent = `Error: ${data.error}`;
        } else {
            // Assuming you have a 'tokens' property in the response
            //outputContainer.textContent = data.tokens.join('\n');

            // Clear existing rows in the table
            tableBody.innerHTML = '';

            // Log the tokens for debugging
            //console.log(data.tokens);

            // Populate the table with token information
            data.tokens.forEach(token => {
                if(token.startsWith('(') && token.endsWith(')')){
                    const row = document.createElement('tr');
                    const typeCell = document.createElement('td');
                    const valueCell = document.createElement('td');
                    const noise_row = document.createElement('tr');
                    const noise_typeCell = document.createElement('td');
                    const noise_valueCell = document.createElement('td');

                    const [key, noise] = token.split(',').map(part => part.trim());
                    var [tokenType, tokenValue] = key.split(': ').map(part => part.trim());
                    var [noise_tokenType, noise_tokenValue] = noise.split(': ').map(part => part.trim());
                    tokenType = tokenType.replace('(',"");
                    noise_tokenValue = noise_tokenValue.slice(0, -1);

                    typeCell.textContent = `${tokenType}`;
                    valueCell.textContent = `${tokenValue}`;
                    noise_typeCell.textContent = `${noise_tokenType}`;
                    noise_valueCell.textContent = `${noise_tokenValue}`;

                    row.appendChild(typeCell);
                    row.appendChild(valueCell);
                    tableBody.appendChild(row);

                    noise_row.appendChild(noise_typeCell);
                    noise_row.appendChild(noise_valueCell);
                    tableBody.appendChild(noise_row);

                }else{
                    const row = document.createElement('tr');
                    const typeCell = document.createElement('td');
                    const valueCell = document.createElement('td');

                    // Split the token to extract type and value
                    const [tokenType, tokenValue] = token.split(': ').map(part => part.trim());

                    typeCell.textContent = `${tokenType}`;
                    valueCell.textContent = `${tokenValue}`;

                    row.appendChild(typeCell);
                    row.appendChild(valueCell);
                    tableBody.appendChild(row);
                }
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}