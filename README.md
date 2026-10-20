# AI E-commerce Customer Support Assistant

A web-based AI customer support assistant built using Python, Streamlit, FastAPI, and the Gemini API. This project demonstrates how a Large Language Model (LLM) can assist with common e-commerce customer queries, retrieve sample order details, check refund eligibility, and provide fallback responses when the AI service is unavailable.

## Features

- **AI-Powered Customer Support:** Uses the Gemini API to generate responses to customer queries.
- **Order Tracking:** Retrieves order information from sample order records.
- **Refund Eligibility Checks:** Checks refund eligibility using the available sample data.
- **Fallback Handling:** Provides alternative responses when the Gemini API encounters an error.
- **FastAPI Backend:** Provides API endpoints for order-related operations.
- **Streamlit Chat Interface:** Offers a simple web-based interface for interacting with the assistant.
- **Automated Testing:** Includes tests for order tools, fallback behavior, and LLM response evaluation.

## Technologies Used

- Python
- Streamlit
- FastAPI
- Gemini API
- REST APIs
- JSON
- Uvicorn
- Python virtual environments

## Project Structure

```text
ecommerce-ai-assistant/
├── app.py
├── api_server.py
├── assistant.py
├── tools.py
├── data/
│   └── orders.json
├── test_evaluation.py
├── test_fallback.py
├── test_llm_evaluation.py
├── requirements.txt
├── README.md
└── .gitignore
```

*Note: The structure above lists the main project files. The `.env` file and `.venv/` directory are excluded from version control.*

## Prerequisites

Before running the project, make sure you have:

- Python installed on your system
- A Gemini API key
- Git (optional, for cloning the repository)
- A terminal or command prompt

## Setup and Installation

### 1. Clone the Repository

After uploading the project to GitHub, replace the placeholder URL with your repository URL.

```bash
git clone <your-github-repository-url>
cd ecommerce-ai-assistant
```

Alternatively, download the project ZIP file and extract it.

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory. Add your Gemini API configuration using the variable names expected by the application.

Example:

```text
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=your_available_gemini_model
```

Replace the placeholder values with your own valid configuration. Use a Gemini model supported by your API key and account.

**Security:** Never upload your actual API key or `.env` file to GitHub. Keep `.env` and `.venv/` in `.gitignore`.

## How to Run

### 1. Start the FastAPI Backend

Open a terminal in the project directory and run:

```powershell
python -m uvicorn api_server:app --reload --port 8001
```

The API server will be available at:

- API base URL: `http://127.0.0.1:8001`
- Interactive API documentation: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

Keep this terminal running.

### 2. Start the Streamlit Application

Open a second terminal in the project directory and run:

```powershell
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

[http://localhost:8501](http://localhost:8501)

Make sure the backend is running if the application depends on the FastAPI server.

## Testing and Evaluation

The project includes automated tests and manual checks for common customer-support scenarios.

### Latest Test Results

| Test Category | Result |
|---|---|
| Local order-tool tests | 4/4 passed |
| Fallback tests | 4/4 passed |
| Manual web-app checks | 3/3 successful |
| LLM evaluation | 3/3 passed |
| Gemini API errors during the latest LLM evaluation run | 0 |

### Run the Tests

Execute the following commands from the project directory:

```powershell
python test_evaluation.py
python test_fallback.py
python test_llm_evaluation.py
```

The LLM evaluation checks whether generated responses contain predefined expected keywords. The latest run completed all three test cases successfully, with no API errors.

**Evaluation note:** Keyword matching is a basic evaluation method. Passing these tests does not guarantee that every response is factually correct, contextually appropriate, or fully accurate.

The LLM evaluation report is saved as `llm_evaluation_report.json`.

## Current Limitations

- Uses sample order data instead of a live e-commerce database.
- Does not process real orders, cancellations, refunds, or payments.
- AI responses depend on Gemini API availability and configuration.
- LLM evaluation uses basic keyword matching and does not fully measure response quality.
- The project is intended for learning and portfolio demonstration, not production use.

## Future Improvements

- Expand LLM evaluation with relevance, factual accuracy, and response-quality checks.
- Add more automated tests for edge cases and API failures.
- Improve API error handling and retry behavior.
- Integrate a real order database and authenticated e-commerce APIs.
- Add conversation history and more customer-support scenarios.
- Improve the user interface and error messages.

## Disclaimer

This project was developed for educational and portfolio purposes. All order records are sample data. No real purchases, order cancellations, refunds, or financial transactions are performed.


## Author

**Bhupendra Kumar**

Aspiring Data Analyst | AI Assistant Enthusiast

- GitHub: https://github.com/bhupendra91051