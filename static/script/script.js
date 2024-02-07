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
  const tableBody = document.querySelector('.styled-table tbody');

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
      tableBody.innerHTML = '';
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
                    const lineCell = document.createElement('td');
                    const typeCell = document.createElement('td');
                    const valueCell = document.createElement('td');
                    const noise_row = document.createElement('tr');
                    const noise_lineCell = document.createElement('td');
                    const noise_typeCell = document.createElement('td');
                    const noise_valueCell = document.createElement('td');

                    const [key, noise] = token.split(',').map(part => part.trim());
                    var [tokenLine, tokenType, tokenValue] = key.split(':').map(part => part.trim());
                    var [noise_tokenLine,noise_tokenType, noise_tokenValue] = noise.split(':').map(part => part.trim());
                    tokenLine = tokenLine.replace('(',"");
                    noise_tokenValue = noise_tokenValue.slice(0, -1);

                    lineCell.textContent = `${parseInt(tokenLine) + 1}`;
                    typeCell.textContent = `${tokenType}`;
                    valueCell.textContent = `${tokenValue}`;
                    noise_lineCell.textContent = `${noise_tokenLine}`;
                    noise_typeCell.textContent = `${noise_tokenType}`;
                    noise_valueCell.textContent = `${noise_tokenValue}`;


                    row.appendChild(lineCell);
                    row.appendChild(typeCell);
                    row.appendChild(valueCell);
                    tableBody.appendChild(row);

                    noise_row.appendChild(noise_lineCell);
                    noise_row.appendChild(noise_typeCell);
                    noise_row.appendChild(noise_valueCell);
                    tableBody.appendChild(noise_row);

                }else{
                    console.log(token)
                    const row = document.createElement('tr');
                    const lineCell = document.createElement('td');
                    const typeCell = document.createElement('td');
                    const valueCell = document.createElement('td');

                    // Split the token to extract type and value
                    const [tokenLine, tokenType, tokenValue] = token.split(':').map(part => part.trim());

                    lineCell.textContent = `${parseInt(tokenLine) + 1}`;
                    typeCell.textContent = `${tokenType}`;
                    valueCell.textContent = `${tokenValue}`;

                    row.appendChild(lineCell);
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

function generateFile() {
  const codeEditor = document.getElementById('code-editor');
  const codeContent = codeEditor.value;

  if (codeContent.trim() !== '') {
      // Prompt the user for a file name
      const fileName = window.prompt('Enter file name (without extension):');
      
      if (fileName !== null) { // Check if the user provided a file name
          // Add the ".dtil" extension to the provided file name
          const fullFileName = fileName.trim() === '' ? 'generated_file.dtil' : `${fileName}.dtil`;

          // Create a Blob containing the code content
          const blob = new Blob([codeContent], { type: 'text/plain' });

          // Create a download link with the specified file name
          const link = document.createElement('a');
          link.href = window.URL.createObjectURL(blob);
          link.download = fullFileName;

          // Append the link to the body
          document.body.appendChild(link);

          // Programmatically trigger the click event
          link.click();

          // Remove the link from the body
          document.body.removeChild(link);
      }
  } else {
      alert('Error: Cannot generate an empty file.');
  }
}
function exportTableToFile() {
    const table = document.querySelector('.styled-table');
    const rows = table.querySelectorAll('tbody tr');
    let tableText = 'Tokens                                                  Lexemes\r\n';
    tableText += '===============================================================================================\r\n';

    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        cells.forEach((cell, index) => {
            console.log(index + " " + cell + " " + cell.textContent);
            tableText += cell.textContent;

            // Calculate the padding based on the length of the content in the cell
            const paddingCount = 50 - cell.textContent.length;
            const padding = ' '.repeat(paddingCount);
            tableText += padding;

            if (index === 0) {
                tableText += '\t'; // Use tab as a delimiter
            }
        });

        tableText += '\r\n';
    });

    // Prompt the user for a file name
    const fileName = window.prompt('Enter file name (without extension):');
    if (fileName !== null) { // Check if the user provided a file name
      // Add the ".dtil" extension to the provided file name
      const fullFileName = fileName.trim() === '' ? 'table_text.txt' : `${fileName}.txt`;

      // Create a Blob containing the table text
      const blob = new Blob([tableText], { type: 'text/plain' });

      // Create a download link
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = fullFileName;

      // Append the link to the body
      document.body.appendChild(link);

      // Programmatically trigger the click event
      link.click();

      // Remove the link from the body
      document.body.removeChild(link);
    }
}

// Save copy of syntax output
function saveCopy(textareaId, derivationType) {
  // Get the content of the textarea
  var content = document.getElementById(textareaId).value;

  // Prompt user for a name input using window.prompt
  var userName = window.prompt("Enter file name:");

  if (userName !== null && userName.trim() !== "") {
    // Create a Blob with the content
    var blob = new Blob([content], { type: "text/plain" });

    // Create a link element
    var link = document.createElement("a");

    // Set the download attribute and filename
    link.download = userName + "_" + derivationType + "_derivation.txt";

    // Create a URL for the Blob and set it as the link's href
    link.href = window.URL.createObjectURL(blob);

    // Append the link to the body
    document.body.appendChild(link);

    // Trigger a click on the link to start the download
    link.click();

    // Remove the link from the body
    document.body.removeChild(link);
  }
}

// Attach the click event to the "Save Copy" buttons
document.querySelector("#leftmost-derivation-btn").addEventListener("click", function() {
  saveCopy("leftmost-derivation", "leftmost");
});

document.querySelector("#rightmost-derivation-btn").addEventListener("click", function() {
  saveCopy("rightmost-derivation", "rightmost");
});