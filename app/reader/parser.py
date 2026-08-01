from lxml import html

from app.library.chapter import Chapter


class Parser:

    def parse_book(self, documents):

        chapters = []

        for number, document in enumerate(documents, start=1):

            if not document or not document.strip():
                continue

            tree = html.fromstring(document)

            heading = tree.xpath("//h1|//h2|//h3")

            title = (
                heading[0].text_content().strip()
                if heading
                else f"Chapter {number}"
            )

            content = tree.text_content().strip()

            if content:
                chapters.append(
                    Chapter(
                        title=title,
                        content=content,
                    )
                )

        return chapters