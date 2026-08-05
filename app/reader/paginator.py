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

        lines = []

        for paragraph in text.splitlines():

            words = paragraph.split()

            if not words:
                lines.append("")
                continue

            current_line = words[0]

            for word in words[1:]:

                test_line = current_line + " " + word

                if self.font.getlength(test_line) <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word

            lines.append(current_line)

        return lines
