"""
Cloe Helper Functions

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
from typing import Optional

from manga_ocr import MangaOcr
from PIL import Image
from PyQt5.QtCore import QBuffer
from PyQt5.QtGui import QPixmap


def pixmapToText(pixmap: QPixmap, model:Optional[MangaOcr]=None) -> str:
    """
    Convert QPixmap object to text using the model
    """

    buffer = QBuffer()
    buffer.open(QBuffer.ReadWrite)
    pixmap.save(buffer, "PNG")
    bytes = BytesIO(buffer.data())

    if bytes.getbuffer().nbytes == 0:
        return ""

    pillowImage = Image.open(bytes)
    text = ""

    if model is not None:
        text = model(pillowImage)

    return text.strip()
