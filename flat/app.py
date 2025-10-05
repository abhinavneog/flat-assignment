import pynini as pn
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ==============================================================================
# 1. FST Definitions and Setup
# ==============================================================================

# --- ASSIGNMENT #3: Digit-to-Word Converter FST ---
# 1. Define the basic mapping for single digits
DIGIT_MAP = [
    ("0", "zero "), ("1", "one "), ("2", "two "), ("3", "three "),
    ("4", "four "), ("5", "five "), ("6", "six "), ("7", "seven "),
    ("8", "eight "), ("9", "nine ")
]
# 2. Create the core single-digit transducer (uses a trailing space for separation)
T_digit = pn.string_map(DIGIT_MAP).optimize()
# 3. Create the overall transducer: it is the closure (one or more repetitions) 
# of the single-digit transducer. (FIXED: Removed the problematic difference operator)
T_converter = pn.closure(T_digit) 


# ==============================================================================
# 2. FST Logic Functions
# ==============================================================================
def fst_string_reversal(input_string):
    """
    Assignment #1: Implements String Reversal FST.
    """
    # 1. Strip leading/trailing whitespace FIRST
    input_string = input_string.strip() 

    # 2. Check if the input is empty AFTER trimming
    if not input_string:
        return "Error: Input is empty, or consisted only of whitespace."

    # 3. Create a linear acceptor for the input string
    input_fst = pn.accep(input_string)
    
    # ... (rest of the function is the same)
    T_reversed = pn.reverse(input_fst)
    
    try:
        result = pn.shortestpath(T_reversed).string() 
        return f"Input: '{input_string}'\nReversed: {result}"
    except Exception as e:
        return f"Error during FST reversal: {e}. Check if input is supported."

def fst_digit_to_word(input_string):
    """
    Assignment #3: Transduces a string of digits (e.g., "123") into words.
    """
    if not input_string or not input_string.isdigit():
        return "Error: Input must be a non-empty string of digits (0-9)."

    # Create the FST for the input string
    input_fst = pn.accep(input_string)
    
    # Compose the input FST with the pre-defined converter FST
    try:
        result_fst = pn.compose(input_fst, T_converter)
        # Extract the shortest path (the result string)
        result = pn.shortestpath(result_fst).string()
        return f"Input: {input_string}\nWords: {result.strip()}" # strip extra space
    except Exception:
        return "Error: Transduction failed. Ensure input is pure digits."


# --- ASSIGNMENT #6: Substring Matcher FSA (Dynamic Pattern) ---

# --- ASSIGNMENT #6: Substring Matcher FSA (Dynamic Pattern) ---
def create_substring_fsa(pattern):
    """
    Dynamically creates an FSA to recognize the given pattern anywhere in a string.
    """
    if not pattern:
        return pn.Fst()

    # FIX: EXPANDED ALPHABET to include punctuation for robustness
    ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789 ,.;:!?'\"-" 
    
    SIGMA = pn.union(*[pn.accep(c) for c in ALPHABET]).optimize()
    T_pattern = pn.accep(pattern).optimize()
    SIGMA_STAR = pn.closure(SIGMA)

    # The final FSA: SIGMA* . PATTERN . SIGMA*
    T_matcher = (SIGMA_STAR + T_pattern + SIGMA_STAR).optimize()
    
    return T_matcher


def fsa_substring_matcher(search_text, pattern_text):
    """
    Checks if the dynamic pattern exists in the search text.
    """
    if not pattern_text:
        return "Error: Substring pattern cannot be empty."
        
    # FIX: Trim leading/trailing whitespace from both inputs
    search_text = search_text.strip()
    pattern_text = pattern_text.strip()
    
    if not pattern_text:
        return "Error: Substring pattern cannot be empty after trimming."

    # Standardize input for case-insensitive matching
    search_text_lower = search_text.lower()
    pattern_text_lower = pattern_text.lower()
    
    # 1. Dynamically create the Matcher FSA
    T_matcher = create_substring_fsa(pattern_text_lower)

    # 2. Convert input string to an FST (an acceptor)
    input_fst = pn.accep(search_text_lower)
    
    # 3. Test: Does the composition of (Input_FST ∘ Matcher_FSA) yield a non-empty FST?
    try:
        result_fst = pn.compose(input_fst, T_matcher)
        
        if result_fst.num_states() > 0:
            return (f"Search String: '{search_text}'\nPattern: '{pattern_text}'\n\n"
                    f"RESULT: MATCH FOUND (FSA Accepted).\n"
                    f"FSA Rule: Σ*.{pattern_text.upper()}.Σ* (Case-Insensitive)")
        else:
            return (f"Search String: '{search_text}'\nPattern: '{pattern_text}'\n\n"
                    f"RESULT: NO MATCH FOUND.")
            
    except Exception as e:
        return f"Error: Could not run FSA matching. ({e})"

# The rest of your app.py remains unchanged.


def fsa_substring_matcher(search_text, pattern_text):
    """
    Checks if the dynamic pattern exists in the search text.
    """
    if not pattern_text:
        return "Error: Substring pattern cannot be empty."
        
    # NEW: Trim leading/trailing whitespace from both inputs
    search_text = search_text.strip()
    pattern_text = pattern_text.strip()
    
    if not pattern_text:
        return "Error: Substring pattern cannot be empty after trimming."

    # Standardize input for case-insensitive matching
    search_text_lower = search_text.lower()
    pattern_text_lower = pattern_text.lower()
    
    # 1. Dynamically create the Matcher FSA
    T_matcher = create_substring_fsa(pattern_text_lower)
    # ... (rest of the function is the same)
    
    # 2. Convert input string to an FST (an acceptor)
    input_fst = pn.accep(search_text_lower)
    
    # 3. Test: Does the composition of (Input_FST ∘ Matcher_FSA) yield a non-empty FST?
    try:
        # Composition finds the intersection of the two languages
        result_fst = pn.compose(input_fst, T_matcher)
        
        if result_fst.num_states() > 0:
            return (f"Search String: '{search_text}'\nPattern: '{pattern_text}'\n\n"
                    f"RESULT: MATCH FOUND (FSA Accepted).\n"
                    f"FSA Rule: Σ*.{pattern_text.upper()}.Σ* (Case-Insensitive)")
        else:
            return (f"Search String: '{search_text}'\nPattern: '{pattern_text}'\n\n"
                    f"RESULT: NO MATCH FOUND.")
            
    except Exception as e:
        return f"Error: Could not run FSA matching. ({e})"

def fst_palindrome_analysis(input_string):
    """
    Assignment #8: Conceptual analysis of Palindrome Recognition.
    """
    if not input_string:
        return "Input is empty."
        
    # FIX: Trim leading/trailing whitespace
    input_string = input_string.strip() 

    if not input_string:
        return "Error: Input is empty after trimming."
        
    # 1. Check if the string is actually a palindrome (Python check for comparison)
    is_palindrome = input_string.lower() == input_string[::-1].lower()
    
    analysis = (
        f"Input String: '{input_string}'\n"
        f"Python check: {'YES, it is a palindrome.' if is_palindrome else 'NO, it is not a palindrome.'}\n\n"
        "--- Theoretical Analysis ---\n"
        "The language of palindromes (strings that read the same forwards and backwards) is **NOT** a Regular Language.\n"
        "**Why an FST/FSA fails:** Finite State Machines have a finite number of states (finite memory). To recognize a palindrome of arbitrary length, the machine must remember the entire first half of the string to compare it, in reverse, with the second half.\n"
        "This requires **infinite memory** (a stack).\n"
        "**Correct Automaton:** Palindrome recognition requires a **Pushdown Automaton (PDA)**."
    )
    return analysis


# ==============================================================================
# 3. Flask Routes
# ==============================================================================

@app.route('/')
def index():
    """Renders the main input page."""
    operations = [
        ("reverse", "1. String Reversal FST"),
        ("digit_to_word", "3. Digit-to-Word Converter FST"),
        ("substring", "6. Substring Matcher FSA (Dynamic Pattern)"),
        ("palindrome", "8. Palindrome Recognizer Analysis (Conceptual)")
    ]
    return render_template('index.html', operations=operations)

@app.route('/process', methods=['POST'])
def process_string():
    """Handles the user input, runs the selected FST, and returns the result."""
    data = request.get_json()
    operation = data.get('operation')
    input_text = data.get('input', '')
    # New field to pass the pattern for the substring match
    secondary_input = data.get('secondary_input', '') 
    
    result = "Error: Invalid operation selected."

    if operation == 'reverse':
        result = fst_string_reversal(input_text)
    elif operation == 'digit_to_word':
        result = fst_digit_to_word(input_text)
    elif operation == 'substring':
        # Pass the main input as the search text, and the secondary input as the pattern
        result = fsa_substring_matcher(input_text, secondary_input) 
    elif operation == 'palindrome':
        result = fst_palindrome_analysis(input_text)
    
    return jsonify({'result': result})

if __name__ == '__main__':
    # Run the application: python app.py
    app.run(debug=True)