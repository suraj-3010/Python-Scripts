# R35-T040 Evidence

## Student Details
- Name: Suraj kumar
- URN: E26B07F1007
- Task ID: R35-T040 (Issue #40)
- Repository: S-AI-Projects/Python-Scripts
- Assigned working branch: student/e26b07f1007/R35-T040

## Target Item
- Module: `HTML to Images/html-to-images.py`
- Target Function: `convert_html_to_image`
- Precondition lines: Line 26 (File existence check), Line 28 (`if len(background) > 0:`)

## Protected Condition and Mutation Analysis
- Condition: `if len(background) > 0:`
- Semantic Role: Selects whether to construct CSS background styling and pass `css_str` to the renderer.
- Deliberate Mutant: Changing line 28 from `if len(background) > 0:` to `if len(background) > 5:`.
- Semantic Distinguishing Input: Short color strings such as `"red"` (length 3), `"#fff"` (length 4), `"blue"` (length 4).
  - Original: `len("red") > 0` is `True` -> passes `css_str='body {background: red;}'`.
  - Mutant: `len("red") > 5` is `False` -> drops background CSS (`css_str=None`), failing the assertion.
- Production Cleanliness: The final production file `HTML to Images/html-to-images.py` contains no test-only branches or mutant code.

## Tool Versions
- Python: 3.15.2
- OS: macOS (Darwin)

## Verification Results
1. Smallest Valid Input (Empty Background `""`):
   - Expected `css`: `None`
   - Screenshot call: Invoked without `css_str`.
   - Result: PASS

2. Ordinary Valid Input (Background `"red"`):
   - Expected `css`: `'body {background: red;}'`
   - Screenshot call: Invoked with `css_str='body {background: red;}'`.
   - Result: PASS

3. Mutant Detection Check:
   - Original implementation produced: `'body {background: red;}'`
   - Mutant implementation produced: `None`
   - Mutant caught by assertion: PASS

4. Deliberate Failure Proof:
   - Command: `FORCE_WRONG=1 python3 work/R35-T040/check.py`
   - Output: `FAIL: Expected WRONG_CSS, got None`
   - Exit code: 1
