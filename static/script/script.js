const codeEditor = document.getElementById("code-editor");
let isTabIndented = false;
let codeHistory = [codeEditor.value];
let historyIndex = 0;

codeEditor.addEventListener("keydown", function (event) {
  if (event.key === "Tab") {
    event.preventDefault();
    handleTabIndentation();
  }
});

codeEditor.addEventListener("input", function () {
  if (isTabIndented) {
    isTabIndented = false;
  } else {
    saveCodeState();
  }
});

function handleTabIndentation() {
  const editor = document.getElementById("code-editor");
  const cursorPosition = editor.selectionStart;
  const indentation = "    "; // 4 spaces

  // Insert the indentation at the current cursor position
  editor.setRangeText(indentation, cursorPosition, cursorPosition, "end");

  // Update the cursor position to account for the inserted indentation
  editor.selectionStart = editor.selectionEnd = cursorPosition + indentation.length;

  isTabIndented = true;
}

function saveCodeState() {
  const currentCode = codeEditor.value;

  // Only save the code state if it has changed
  if (currentCode !== codeHistory[historyIndex]) {
    codeHistory = codeHistory.slice(0, historyIndex + 1);
    codeHistory.push(currentCode);
    historyIndex++;
  }
}

document.addEventListener("keydown", function (event) {
  if (event.ctrlKey && event.key === "z") {
    event.preventDefault();
    undo();
  } else if (event.ctrlKey && event.key === "y") {
    event.preventDefault();
    redo();
  }
});

function undo() {
  if (historyIndex > 0) {
    historyIndex--;
    codeEditor.value = codeHistory[historyIndex];
  }
}

function redo() {
  if (historyIndex < codeHistory.length - 1) {
    historyIndex++;
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