#!/usr/bin/env python3
import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TARGET_DIR = os.path.join(ROOT_DIR, "HTML to Images")
sys.path.insert(0, TARGET_DIR)

hti_mod = __import__("html-to-images")


def run_checks():
    print("Running mutation-resistant checks for R35-T040: HTML to Images...")
    force_wrong = os.environ.get("FORCE_WRONG") == "1"

    with tempfile.TemporaryDirectory() as tmpdir:
        sample_html = os.path.join(tmpdir, "test.html")
        with open(sample_html, "w", encoding="utf-8") as f:
            f.write("<h1>Sample</h1>")

        # Check 1: Smallest valid input (empty background "")
        # Preconditions established at html-to-images.py line 28 (if len(background) > 0)
        mock_hti = MagicMock()
        _, _, css_small = hti_mod.convert_html_to_image(sample_html, "small.png", background="", hti=mock_hti)
        expected_small_css = "WRONG_CSS" if force_wrong else None
        print(f"[Smallest input (background='')] CSS: {css_small}")
        if css_small != expected_small_css:
            print(f"FAIL: Expected {expected_small_css}, got {css_small}")
            sys.exit(1)
        mock_hti.screenshot.assert_called_once_with("<h1>Sample</h1>", save_as="small.png")

        # Check 2: Ordinary input (background='red')
        mock_hti = MagicMock()
        _, _, css_ord = hti_mod.convert_html_to_image(sample_html, "ord.png", background="red", hti=mock_hti)
        expected_ord_css = "body {background: red;}"
        print(f"[Ordinary input (background='red')] CSS: {css_ord}")
        if css_ord != expected_ord_css:
            print(f"FAIL: Expected {expected_ord_css}, got {css_ord}")
            sys.exit(1)
        mock_hti.screenshot.assert_called_once_with(
            "<h1>Sample</h1>", css_str="body {background: red;}", save_as="ord.png"
        )

        # Check 3: Mutant proof - Plausible mutation `len(background) > 5`
        # On background='red', original passes with 'body {background: red;}', while mutant produces None
        def mutant_implementation(file, img, background='', hti=None):
            css = None
            if len(background) > 5:  # MUTANT: altered boundary condition from > 0 to > 5
                css = ('body {background: %s;}' % (background))
                with open(file, 'r', errors='ignore') as f:
                    hti.screenshot(f.read(), css_str=css, save_as=img)
            else:
                with open(file, 'r', errors='ignore') as f:
                    hti.screenshot(f.read(), save_as=img)
            return (file, img, css)

        mock_mutant = MagicMock()
        _, _, mutant_css = mutant_implementation(sample_html, "mut.png", background="red", hti=mock_mutant)
        if mutant_css == expected_ord_css:
            print("FAIL: Mutant failed to alter semantic behavior on background='red'")
            sys.exit(1)
        print(f"[Mutant Detection] Original produced: '{css_ord}', Mutant produced: {mutant_css} (Detected: PASS)")

    # Run unittest suite
    suite = unittest.defaultTestLoader.discover(TARGET_DIR, pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    res = runner.run(suite)
    if not res.wasSuccessful():
        print("FAIL: unittest suite failed")
        sys.exit(1)

    print(f"PASS: All mutation checks passed (ran {res.testsRun} unittest cases).")
    return 0


if __name__ == "__main__":
    sys.exit(run_checks())
