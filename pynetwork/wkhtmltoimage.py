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
import shutil

__version__ = '1.0.0'
__description__ = "Python wrapper for wkhtmltopdf library - renders html to image (.jpeg) file"

XVFB_RUN = "xvfb-run"
WKHTML_TO_IMAGE = "wkhtmltoimage"
XVFB_CMD = XVFB_RUN + " " + WKHTML_TO_IMAGE + " --window-status ready_to_print --crop-h 396 {0} {1}"

@property
def dependencies_installed():
    """
        Checks whether xvfb-run and wkhtmltoimage packages installed on local machine
    """
    xvfb = shutil.which(XVFB_RUN) is not None
    wkhtml = shutil.which(WKHTML_TO_IMAGE) is not None
    return xvfb and wkhtml

def convert_html_to_image(html_path, image_out_path):
    """Converts html file to image and stores to disk
        Returns:
            whether the operations succeeded
    """
    if dependencies_installed() is False:
        return False

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


