from lxml import html


class Parser:

    def parse_book(self, documents):

        chapters = []

        for chapter_number, document in enumerate(documents, start=1):

            tree = html.fromstring(document)

            heading = tree.xpath("//h1|//h2|//h3")

            if heading:
                title = heading[0].text_content().strip()
            else:
                title = f"Chapter {chapter_number}"

            content = tree.text_content().strip()

            chapters.append({
                "title": title,
                "content": content,
            })

        return chapters