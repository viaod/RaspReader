from bs4 import BeautifulSoup


class Parser:

    def parse_book(self, documents):

        chapters = []

        for chapter_number, document in enumerate(documents, start=1):

            soup = BeautifulSoup(document, "html.parser")

            heading = soup.find(["h1", "h2", "h3"])

            if heading:
                title = heading.get_text(strip=True)
            else:
                title = f"Chapter {chapter_number}"

            content = soup.get_text("\n", strip=True)

            chapters.append({
                "title": title,
                "content": content,
            })

        return chapters