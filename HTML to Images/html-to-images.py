import os
try:
    from html2image import Html2Image
except ImportError:
    Html2Image = None


def convert_html_to_image(file: str, img: str, background: str = '', hti=None) -> tuple:
    """
    Convert an HTML file into an image with optional background styling.

    Contract & Protected Condition Specification:
    - Precondition: file must point to an accessible HTML file (source line 26).
    - Protected Condition (source line 28):
      `if len(background) > 0:`
      When a non-empty background string is provided, a CSS rule 'body {background: %s;}'
      is constructed and passed as css_str to hti.screenshot().
      When background is empty (""), screenshot() is called without css_str.
    - Mutation Resistance:
      A plausible one-line mutation (e.g. `if len(background) > 5:` or `if not background:`)
      will either drop background styling for valid colors like 'red' (len=3) or incorrectly
      inject invalid CSS for empty strings.
    - Return Value: Tuple containing (file, img, css_used) describing the completed invocation.
    """
    if not os.path.exists(file):
        raise FileNotFoundError(f"HTML file not found: {file}")

    if hti is None:
        if Html2Image is None:
            raise RuntimeError("html2image is not installed")
        hti = Html2Image()

    css = None
    if len(background) > 0:
        css = ('body {background: %s;}' % (background))
        with open(file, 'r', errors='ignore') as f:
            hti.screenshot(f.read(), css_str=css, save_as=img)
    else:
        with open(file, 'r', errors='ignore') as f:
            hti.screenshot(f.read(), save_as=img)

    return (file, img, css)


def main():
    if Html2Image is None:
        print("Error: html2image library is required.")
        return

    hti = Html2Image()
    file = str(input('Enter the directory of your html file: '))
    img = str(input('Enter the name of your image including file format: '))
    background = str(input('(OPTIONAL) Enter the background color you would like: '))
    convert_html_to_image(file, img, background=background, hti=hti)


if __name__ == '__main__':
    main()
