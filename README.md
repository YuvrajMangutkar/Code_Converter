# Nexus Code Converter ✨

Transform your source code from one programming language to another instantly with the power of AI! This application uses a modern, dynamic web interface backed by a lightning-fast FastAPI server and Google's Gemini AI.

## 🚀 Features

*   **Fast & Accurate translation** of code across top programming languages.
*   **10 Supported Languages**: Python, JavaScript, Java, C++, C#, Go, Rust, PHP, Ruby, and Swift.
*   **Intuitive UI**: Smooth glassmorphism design, responsive layouts, and beautifully styled code blocks.
*   **No Database Required**: 100% stateless execution—just paste and convert.

## 🛠️ Built With

*   **Frontend**: HTML5, Vanilla CSS, Vanilla JavaScript
*   **Backend**: Python, FastAPI, Uvicorn
*   **AI Engine**: Google GenAI (`gemini-2.5-flash-lite`)

## 💻 Local Setup

Want to run this project on your own machine? Follow these steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/YuvrajMangutkar/Code_Converter.git
   cd Code_Converter
   ```

2. **Install Backend Dependencies**
   Make sure you have Python installed, then install the required libraries:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Configure the Environment**
   Create a `.env` file inside the `backend` folder and add your Google Gemini API Key:
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key_here
   ```

4. **Start the Server**
   Start the FastAPI app using Uvicorn:
   ```bash
   python -m uvicorn backend.main:app
   ```
   *Note: Because we mapped the frontend directly in the FastAPI file, you can now instantly view the application by navigating to `http://localhost:8000` in your web browser!*

## ☁️ Deployment (Render)

This repository is optimized to easily drop right into **Render.com**. 

1. Create a New Web Service connected to this GitHub repo.
2. Set the **Build Command** to: `pip install -r backend/requirements.txt`
3. Set the **Start Command** to: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4. Make sure to add the `GEMINI_API_KEY` Environment Variable under **Advanced** options!

---
*Made for College Students. Powered by FastAPI & AI.*
