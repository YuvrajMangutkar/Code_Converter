// Define default code snippets
const defaultCode = {
    python: "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n\n# Calculate the 10th Fibonacci number\nresult = [fibonacci(i) for i in range(10)]\nprint(f\"Fibonacci sequence: {result}\")",
    javascript: "function fibonacci(n) {\n    if (n <= 1) return n;\n    return fibonacci(n - 1) + fibonacci(n - 2);\n}\n\n// Calculate the 10th Fibonacci number\nconst result = Array.from({length: 10}, (_, i) => fibonacci(i));\nconsole.log('Fibonacci sequence: ' + result.join(', '));"
};

const sourceEditor = document.getElementById('source-editor');
const targetEditor = document.getElementById('target-editor');
const sourceLangSelect = document.getElementById('source-lang');
const targetLangSelect = document.getElementById('target-lang');

// Set initial value
sourceEditor.value = defaultCode.python;

// Handle language change for Source Editor
sourceLangSelect.addEventListener('change', (e) => {
    const lang = e.target.value;
    if (defaultCode[lang]) {
        sourceEditor.value = defaultCode[lang];
    }
});

// Conversion Logic
const convertBtn = document.getElementById('convert-btn');
const loadingIndicator = document.getElementById('loading-indicator');
const API_URL = 'http://localhost:8000/api/convert';

convertBtn.addEventListener('click', async () => {
    const sourceCode = sourceEditor.value;
    const sourceLang = sourceLangSelect.value;
    const targetLang = targetLangSelect.value;

    if (!sourceCode.trim()) {
        alert("Please enter some code to convert.");
        return;
    }

    // UI Feedback
    convertBtn.classList.add('hidden');
    loadingIndicator.classList.remove('hidden');
    targetEditor.value = "// Converting...\n// Please wait...";

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                code: sourceCode,
                source_language: sourceLang,
                target_language: targetLang
            })
        });

        if (!response.ok) {
            throw new Error("Server responded with " + response.status);
        }

        const data = await response.json();
        
        // Update Target Editor
        targetEditor.value = data.converted_code;

    } catch (error) {
        console.error("Conversion failed:", error);
        targetEditor.value = "// Error during conversion:\n// " + error.message + "\n// Ensure the FastAPI backend is running on localhost:8000";
    } finally {
        // Reset UI Feedback
        loadingIndicator.classList.add('hidden');
        convertBtn.classList.remove('hidden');
    }
});
