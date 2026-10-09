# Personal  Knowledge  Base

This Project lets you extract emails from Folders in your emai-account, and from These documents (Texts + attachments) build a RAG System that can answer Questions regarding the subjects contained in These folders

## Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Technologies Used](OCR, RAG)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## About the Project

his Project lets you extract emails from email-accountFolders, and use This data (Texts + attachments) to build a RAG System that can answer Questions regarding the subjects contained in These folders

## Features

- Feature 1: extract Texts + attachments of email-Folders in your account
- Feature 2: process the data and build a data-base Ready to be used by a RAG system
- Feature 3: an interface that allows getting annswers to queries oncerning the subject contained in the emails

## Technologies Used

- Programming language:  Python
- Tools: [ Git, VS Code, uv, fastapi, imap]


## Getting Started

1. create a Password that allows you to contact your email-Account via imap-protocol
2  get an API-KEY for OpenRouter
3. choose a Folder where the email-data will reside
4. set (or put in a ".env" file) These 3 environment-variable with appropriate.values:
    a)  OPENROUTER_API_KEY
    b)  MAIL_SERVER_PASSWD
    3)  PKB_DATA_FOLDER      (full-path to the documents-data)




### Prerequisites

Install:    Git, Python, VS code

## Installation

1. Clone the repository:

   ```bash
   git clone ...
   ```

2. Open the project directory:

   ```bash
   cd personal_knowledge_base
   ```

3. Install the project's dependencies using the appropriate command.

   For Python projects:

   ```bash
   uv add fastapi
   uv add imap-tools
   uv add pypdf
   uv add pytesseract
   uv add dotenv
   uv add fastembed
   uv add fonttools
   ```

## Usage

1. go to "src\personal_knowledge_base" Folder (where the source files are) and run the command:   "uv run fastapi dev .\web_service.py"  (starts the server-side)
2. Open a browser, and type "http://localhost:8000/docs" - that will open a UI with the 4 available endpoints are .
3. ALTERNITAVELY - open a web-browser and activate manually one of the 4 endpoints:
                     o   localhost:8000/save_attachments?username=< EMAIL >&email_folder=< EXTRACTED EMAIL FOLDER >_eng&save_folder=< FOLDER TO SAVE DATA >
                     o   localhost:8000/save_texts?username=< EMAIL >&email_folder=< EXTRACTED EMAIL FOLDER >&save_folder=< FOLDER TO SAVE DATA >
                     o   localhost:8000/create_vectorestore/< DOCUMENTS_FOLDER >   
                     o   localhost:8000/query_rag/< QUERY >
4. NOTES:   a) before running "create_vectorestore", do a MANUAL check that < DOCUMENTS_FOLDER > contains valid documents (for now: "pdf" and "txt" files) 
            b) "create_vectorestore" will create a folder named < DOCUMENTS_FOLDER_qdrant_db >
            c) before running "query_rag", make sure the environment-variable QDRANT_DB_PATH is set the full-path of the qdrant_db created by "create_vectorestore"


```bash
# Example
  o   localhost:8000/save_attachments?username=rami.mayer@yahoo.com&email_folder=Simulator_2015_eng&save_folder=att
  o   localhost:8000/save_texts?username=rami.mayer@yahoo.com&email_folder=CodingAcademy&save_folder=msgs"
  o   localhost:8000/localhost:8000/create_vectorestore/my_docs
  o   localhost:8000/query_rag/what is Instrument flying

```

## Project Structure

Example structure (adapt it to your repository):

```text
YOUR_REPOSITORY/
├── src/                 # Source code
├── tests/               # Test files
├── docs/                # Documentation
├── .gitignore           # Files ignored by Git
├── README.md            # Project documentation
└── LICENSE              # Project license
```

## Screenshots

Add screenshots or GIFs if they help explain your project.

Example:

```markdown
![Application Screenshot](screenshots/demo.png)
```

Make sure the image exists at the specified path in your repository.

## Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a branch for your change:

   ```bash
   git checkout -b feature/your-feature
   ```

3. Make your changes and test them.
4. Commit your changes:

   ```bash
   git commit -m "Add your feature"
   ```

5. Push your branch:

   ```bash
   git push origin feature/your-feature
   ```

6. Open a Pull Request.

## License

Specify the license for this project, for example, the MIT License.

If you use the MIT License, include a corresponding `LICENSE` file in the repository. Do not claim a license unless you have chosen one.

## Contact

Your Name

- GitLab: https://......
- Email: rami.mayer@yahoo.com

## Acknowledgments

- Thanks to Arno Venner  and  Matthias Hölzel   who supported me in this project
