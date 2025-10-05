# CSE FST & Automata Project Demonstrator (Flask/Pynini)

This project is a web-based demonstrator for various Finite State Transducer (FST) and Finite State Automata (FSA) operations, built using **Python Flask** and the **Pynini** library. It allows users to select an operation and input a string to see the result of the FST/FSA application.

## 🌟 Features Implemented

The application demonstrates core concepts in Formal Languages and Automata Theory by implementing the following functions, as defined in `app.py`:

| Assignment | Operation Name | Description | Automaton Type |
| :---: | :--- | :--- | :--- |
| **1** | **String Reversal** | Takes an input string and outputs the reversed string (e.g., "hello" $\rightarrow$ "olleh"). | FST |
| **3** | **Digit-to-Word Converter** | Converts a string of digits (e.g., "123") into their word representation (e.g., "one two three"). | FST |
| **6** | **Substring Matcher** | Dynamically creates an FSA to check if a specified pattern exists anywhere within a search string (case-insensitive) using the $\Sigma^*. \text{Pattern}. \Sigma^*$ rule. | FSA |
| **8** | **Palindrome Analysis** | Provides a conceptual analysis explaining why palindrome recognition for arbitrary length strings is **not** possible with a standard FSA/FST and requires a **Pushdown Automaton (PDA)**. | Conceptual Analysis |

***

## 🚀 Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

You need **Python 3.x** installed on your system.

### Installation

1.  **Obtain the Files**: Ensure you have `app.py` and `index.html` in the same directory.
2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    .\venv\Scripts\activate   # On Windows
    ```
3.  **Install dependencies**:
    This project primarily relies on `flask` and `pynini`.
    ```bash
    pip install Flask pynini
    ```
    *Note: Pynini requires specific dependencies (like `openfst`). If installation fails, please consult the official Pynini documentation for OS-specific requirements.*

### Running the Application

1.  **Start the Flask server** from the command line in the project directory:
    ```bash
    python app.py
    ```
2.  **Access the application** in your web browser:
    Open `http://127.0.0.1:5000/`

The web interface will allow you to select an operation, enter the required input(s), and view the output from the corresponding FST/FSA.

***

## 🗃️ Project Files Overview

* **`app.py`**: The core Flask application logic. It defines the FSTs/FSAs using the `pynini` library, handles the routing (`/`, `/process`), and contains the functions for each automaton assignment.
    * The `T_converter` for digit-to-word uses `pn.closure(pn.string_map(DIGIT_MAP))`.
    * The `create_substring_fsa` dynamically builds a matcher FST using `SIGMA_STAR + T_pattern + SIGMA_STAR`.
* **`index.html`**: The Jinja2 template for the frontend interface. It handles user input via a dropdown and text fields, manages the visibility of the "Pattern" input for the substring operation, and sends asynchronous requests to the `/process` endpoint using JavaScript's `fetch`.

***
*Created for the CSE Formal Systems & Automata course project.*# flat-assignment
flat assignment
