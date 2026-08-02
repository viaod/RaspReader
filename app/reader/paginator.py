from app.library.book import Chapter, Page


class Paginator:

    def __init__(
        self,
        chars_per_line=125,
        lines_per_page=11,
    ):
        self.chars_per_line = chars_per_line
        self.lines_per_page = lines_per_page


    def paginate_chapter(self, chapter: Chapter):

        lines = self.wrap_text(chapter.text)

        pages = []

        for i in range(
            0,
            len(lines),
            self.lines_per_page
        ):

            page_lines = lines[
                i:i + self.lines_per_page
            ]

            pages.append(
                Page(
                    number=len(pages) + 1,
                    text="\n".join(page_lines),
                )
            )

        chapter.pages = pages

        return pages


    def wrap_text(self, text):

        lines = []

        for paragraph in text.split("\n"):

            paragraph = paragraph.strip()

            if not paragraph:
                lines.append("")
                continue

            while len(paragraph) > self.chars_per_line:

                # Find a good word boundary
                split_at = paragraph.rfind(
                    " ",
                    0,
                    self.chars_per_line
                )

                if split_at == -1:
                    split_at = self.chars_per_line

                lines.append(
                    paragraph[:split_at]
                )

                paragraph = paragraph[
                    split_at:
                ].strip()

            lines.append(paragraph)

        return lines