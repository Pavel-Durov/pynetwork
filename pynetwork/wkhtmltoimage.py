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

CMD = "wkhtmltoimage"
XVFB_CMD = "xvfb-run " + CMD + " {0} {1}"

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
