📘 BrowserStack Assignment – Selenium Automation

📌 Overview

This project demonstrates end-to-end Selenium automation combined with web scraping, API integration, text processing, and cross-browser testing using BrowserStack.

The solution:

    Scrapes opinion articles from El País (Spanish news website)
    Extracts article titles, content, and image captions
    Translates Spanish titles into English
    Performs keyword frequency analysis on translated titles
    Executes cross-browser tests using BrowserStack with parallel sessions

🛠️ Tech Stack

    Language: Python 3
    Automation: Selenium 4
    Translation: Google Translate (via googletrans)
    Cloud Testing: BrowserStack
    Environment Management: python-dotenv

📂 Project Structure
BrowserStack_Assignment/
│
├── main.py                 # Main script (scraping, translation, analysis)
├── browserstack_run.py     # BrowserStack parallel execution script
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
├── images/                 # Downloaded article images
├── .gitignore              # Ignored files (.env, cache, etc.)
└── .env                    # Environment variables (NOT committed)

⚙️ Setup Instructions
1️⃣ Clone the Repository
    git clone <your-github-repo-url>
    cd BrowserStack_Assignment

2️⃣ Install Dependencies
    pip install -r requirements.txt

3️⃣ Configure Environment Variables
    Create a .env file in the project root:

    BROWSERSTACK_USERNAME=your_browserstack_username
    BROWSERSTACK_ACCESS_KEY=your_browserstack_access_key

⚠️ The .env file is excluded from version control for security.

▶️ Local Execution

    Run the main script locally to validate scraping and processing:
    python main.py

This will:
    Verify the website language (Spanish)
    Scrape the first 5 opinion articles
    Extract content and images
    Translate titles to English
    Perform repeated-word analysis

🌐 BrowserStack Execution (Parallel Testing)

The solution is executed on BrowserStack using 5 parallel sessions to validate cross-browser compatibility.

Browsers Tested
Chrome (Windows 11)
Firefox (Windows 11)
Edge (Windows 11)
Safari (macOS Ventura)
Chrome (Android – Samsung Galaxy S23)

Run on BrowserStack
    python browserstack_run.py

Expected Output
    5 live sessions visible on the BrowserStack dashboard
    Console logs confirming execution on each platform

🔐 Security Considerations
BrowserStack credentials are managed using environment variables
No secrets are hard-coded
.env file is excluded via .gitignore

🧠 Key Highlights
Handles dynamic DOM content and multiple article layouts
Extracts paragraph text, standfirsts, and image captions
Deduplicates content while preserving reading order
Uses Selenium 4–compatible BrowserStack configuration
Demonstrates parallel execution across desktop and mobile browsers

✅ Assignment Completion
This implementation fulfills all requirements specified in Round 2 – Technical Assignment, including:
Web scraping
API-based translation
Text analysis
Cross-browser parallel execution on BrowserStack

👤 Author
Riddhi Danej
B.Tech – Artificial Intelligence & Machine Learning