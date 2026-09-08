import re

from app.library.book import Chapter, Page


class Paginator:

    def __init__(
        self,
        font,
        page_width,
        lines_per_page=9,
        margin=10,
    ):
        self.font = font
        self.page_width = page_width
        self.lines_per_page = lines_per_page
        self.margin = margin

    def paginate_chapter(self, chapter: Chapter):
        # TODO: do i want page in chapter and or page in book?
            # c_page and b_page ?
        
        lines = self.wrap_text(chapter.text)

        pages = []

        for i in range(0, len(lines), self.lines_per_page):

            page_lines = lines[i:i + self.lines_per_page]

            pages.append(
                Page(
                    number=len(pages) + 1,
                    text="\n".join(page_lines),
                )
            )

        chapter.pages = pages

        return pages

    def wrap_text(self, text):

        max_width = self.page_width - (self.margin * 2)

        lines = []

        # EPUB text nodes often introduce a newline between inline words.
        # Only a blank line represents a paragraph break; single newlines are
        # folded into spaces by ``split()`` below.
        paragraphs = re.split(r"\n\s*\n+", text)

        for paragraph in paragraphs:

            words = paragraph.split()

            if not words:
                lines.append("")
                continue

            line_words = []
            line_width = 0

            for word in words:

                word_parts = self._split_word(word, max_width)
                for word_part in word_parts:
                    separator_width = self.font.getlength(" ") if line_words else 0
                    part_width = self.font.getlength(word_part)

                    if line_words and line_width + separator_width + part_width > max_width:
                        lines.append(" ".join(line_words))
                        line_words = []
                        line_width = 0
                        separator_width = 0

                    line_words.append(word_part)
                    line_width += separator_width + part_width

            if line_words:
                lines.append(" ".join(line_words))

        return lines

    def _split_word(self, word, max_width):
        """Split a word that is wider than the available line."""
        if self.font.getlength(word) <= max_width:
            return [word]

        parts = []
        current = ""

        for character in word:
            candidate = current + character
            if current and self.font.getlength(candidate) > max_width:
                parts.append(current)
                current = character
            else:
                current = candidate

        if current:
            parts.append(current)

        return parts
