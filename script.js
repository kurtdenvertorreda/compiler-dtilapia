const codeEditor = document.getElementById("code-editor");
let isTabIndented = false;
let codeHistory = [codeEditor.value];
let historyIndex = 0;

codeEditor.addEventListener("keydown", function(event) {
  if (event.key === "Tab") {
    event.preventDefault();
    handleTabIndentation();
  }
});

codeEditor.addEventListener("input", function() {
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

document.addEventListener("keydown", function(event) {
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


// const lineNumbers = document.querySelector(".line-numbers");
// console.log(lineNumbers);
// codeEditor.addEventListener("input", () => {
//   let lines = codeEditor.value.split("\n");
//   lineNumbers.textContent = lines.map((line, i) => (i + 1)).join("\n");  
// });