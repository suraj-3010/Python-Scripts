import unittest
from unittest.mock import MagicMock
import tempfile
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
# Import the hyphenated module name
hti_mod = __import__("html-to-images")


class TestHtmlToImageMutationResistance(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.html_file = os.path.join(self.tmpdir.name, "sample.html")
        with open(self.html_file, "w", encoding="utf-8") as f:
            f.write("<p>Hello</p>")

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_smallest_valid_input_empty_background(self):
        # Smallest valid input: minimal file with empty background string
        # Preconditions established at html-to-images.py line 28: if len(background) > 0
        mock_hti = MagicMock()
        f, img, css = hti_mod.convert_html_to_image(
            self.html_file, "output.png", background="", hti=mock_hti
        )

        self.assertEqual(f, self.html_file)
        self.assertEqual(img, "output.png")
        self.assertIsNone(css)
        mock_hti.screenshot.assert_called_once_with("<p>Hello</p>", save_as="output.png")

    def test_ordinary_valid_input_with_background(self):
        # Ordinary input: short valid background color "red" (length 3)
        mock_hti = MagicMock()
        f, img, css = hti_mod.convert_html_to_image(
            self.html_file, "colored.png", background="red", hti=mock_hti
        )

        self.assertEqual(css, "body {background: red;}")
        mock_hti.screenshot.assert_called_once_with(
            "<p>Hello</p>", css_str="body {background: red;}", save_as="colored.png"
        )

    def test_mutation_detection_on_mutated_condition(self):
        # Prove that a mutant with `len(background) > 5` (e.g. plausible bug) fails on "red"
        # Original logic: len("red") > 0 is True
        # Mutant logic: len("red") > 5 is False
        def mutated_convert(file, img, background='', hti=None):
            css = None
            if len(background) > 5:  # MUTANT
                css = ('body {background: %s;}' % (background))
                with open(file, 'r', errors='ignore') as f:
                    hti.screenshot(f.read(), css_str=css, save_as=img)
            else:
                with open(file, 'r', errors='ignore') as f:
                    hti.screenshot(f.read(), save_as=img)
            return (file, img, css)

        mock_hti = MagicMock()
        # The mutant produces None for css on "red"
        _, _, mutant_css = mutated_convert(self.html_file, "out.png", background="red", hti=mock_hti)
        self.assertNotEqual(mutant_css, "body {background: red;}", "Mutant should fail to apply background CSS")


if __name__ == "__main__":
    unittest.main()
