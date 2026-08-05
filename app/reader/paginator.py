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

        # Calling PIL's font measurement for every word is prohibitively slow
        # on the Raspberry Pi for a full novel. Measure once, then use a
        # proportional character budget while wrapping.
        sample = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        average_char_width = self.font.getlength(sample) / len(sample)
        max_chars = max(1, int(max_width / average_char_width))

        lines = []

        for paragraph in text.splitlines():

            words = paragraph.split()

            if not words:
                lines.append("")
                continue

            line_words = []
            line_length = 0

            for word in words:

                next_length = line_length + len(word) + bool(line_words)

                if line_words and next_length > max_chars:
                    lines.append(" ".join(line_words))
                    line_words = [word]
                    line_length = len(word)
                else:
                    line_words.append(word)
                    line_length = next_length

            lines.append(" ".join(line_words))

        return lines
