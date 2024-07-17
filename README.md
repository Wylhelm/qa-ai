# Test Scenario Generator

## Overview
The Test Scenario Generator is an AI-powered desktop application designed to assist QA professionals and testers in creating comprehensive test scenarios. It leverages natural language processing to analyze input documents and generate scenarios that adhere to the IEEE 829 standard.

## Key Features
- Document Analysis: Processes Word, PDF, and text files to extract relevant information.
- AI-Powered Scenario Generation: Utilizes a local LLM server to generate test scenarios based on input criteria and extracted document information.
- User-Friendly Interface: Built with PyQt5 for a responsive and intuitive user experience.
- Customizable Prompts: Allows users to modify system and scenario prompts for tailored results.
- Scenario History: Maintains a database of generated scenarios for easy access and management.
- Export Functionality: Enables exporting generated scenarios to text files.

## Technical Stack
- Python 3.7+
- PyQt5 for GUI
- SQLite for local database storage
- Local LLM server for AI processing
- Document processing libraries: docx2txt, PyPDF2

## Setup
1. Ensure Python 3.7+ is installed on your system.
2. Clone this repository.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up a local LLM server accessible at http://localhost:1234.
5. Run the application:
   ```
   python main.py
   ```

## Usage
Refer to the `user_guide.md` for detailed instructions on how to use the application.

## Development
For developers interested in extending or modifying the application, please consult the `developer_guide.md` for in-depth information about the project structure and best practices.

## License
[Include license information here]

## Contributors
[List main contributors or maintainers]

## Support
For issues, feature requests, or general inquiries, please [open an issue](link-to-issue-tracker) on our GitHub repository.
