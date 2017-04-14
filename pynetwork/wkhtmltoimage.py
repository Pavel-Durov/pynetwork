""" Python wrapper for wkhtmltopdf library, for rendering images from html files.
        [ doc: https://wkhtmltopdf.org/docs.html ]

    This script designed to be run on devices without display.
    Uses xvfb (X virtual framebuffer) for that functionality.
        [ doc: https://www.x.org/archive/X11R7.6/doc/man/man1/Xvfb.1.xhtml ].

    Dependencies : [xvfb, wkhtmltopdf]

    Dependencies install:
        apt-get install wkhtmltopdf
        apt-get install xvfb
"""

from subprocess import call
import logging
import argparse

__version__ = '1.0.0'
__description__ = "Python wrapper for wkhtmltopdf library, for rendering images from html files."

CMD = "wkhtmltoimage"
HTML_WINDOW_STATUS = "ready_to_print"
XVFB_CMD = "xvfb-run " + CMD + " --window-status " + HTML_WINDOW_STATUS + " {0} {1}"

def convert_html_to_image(html_path, image_out_path):
    """Converts html file to image and stores to disk
        Returns:
            whether the operations succeeded
    """
    try:
        cmd = XVFB_CMD.format(html_path, image_out_path)
        call(cmd, shell=True)
        return True
    except IOError as ex:
        logging.getLogger("PYNETWORK").exception(ex)

    return False

def main():
    """Main entry point"""

    arg_parser = argparse.ArgumentParser(
        description=__description__,
        usage='%(prog)s [OPTION]...')

    arg_parser.add_argument("html", help="Html file path")
    arg_parser.add_argument("image", help="Image Output file path")
    args = arg_parser.parse_args()

    if args:
        convert_html_to_image(args.html, args.image)

if __name__ == "__main__":
    main()


