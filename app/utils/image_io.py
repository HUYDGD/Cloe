"""
Poricom Image Processing Utility

Copyright (C) `2021-2022` `<Alarcon Ace Belen>`

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from io import BytesIO

from PyQt5.QtCore import QBuffer
from PyQt5.QtGui import QGuiApplication
from tesserocr import PyTessBaseAPI
from PIL import Image

from utils.config import config


def pixboxToText(pixmap, lang="jpn_vert", model=None):

    buffer = QBuffer()
    buffer.open(QBuffer.ReadWrite)
    pixmap.save(buffer, "PNG")
    bytes = BytesIO(buffer.data())

    if bytes.getbuffer().nbytes == 0:
        return

    pillowImage = Image.open(bytes)
    text = ""

    if model is not None:
        text = model(pillowImage)

    # PSM = 1 works most of the time except on smaller bounding boxes.
    # By smaller, we mean textboxes with less text. Usually these
    # boxes have at most one vertical line of text.
    else:
        with PyTessBaseAPI(path=config["LANG_PATH"], lang=lang, oem=1, psm=1) as api:
            api.SetImage(pillowImage)
            text = api.GetUTF8Text()

    return text.strip()


def logText(text, mode=False, path="."):
    clipboard = QGuiApplication.clipboard()
    clipboard.setText(text)

    if mode:
        with open(path, 'a', encoding="utf-8") as fh:
            fh.write(text + "\n")
