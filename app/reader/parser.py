from lxml import html


class Parser:

    def parse_book(self, documents):

        chapters = []
        
        print(f"Documents: {len(documents)}")

        # for chapter_number, document in enumerate(documents, start=1):

        #     if not document or not document.strip():
        #         print(f"Skipping empty document {chapter_number}")
        #         continue

        #     tree = html.fromstring(document)

        #     heading = tree.xpath("//h1|//h2|//h3")

        #     if heading:
        #         title = heading[0].text_content().strip()
        #     else:
        #         title = f"Chapter {chapter_number}"

        #     content = tree.text_content().strip()

        #     chapters.append({
        #         "title": title,
        #         "content": content,
        #     })

        # return chapters
        
        for chapter_number, document in enumerate(documents, start=1):

            print(f"Document {chapter_number}: type={type(document)}")

            if isinstance(document, bytes):
                print("Length:", len(document))
                print("First 50 bytes:", document[:50])
            else:
                print("Length:", len(str(document)))
                print("First 50 chars:", repr(str(document)[:50]))

            if not document:
                print("Skipping empty document")
                continue

            if isinstance(document, bytes):
                document = document.decode("utf-8", errors="ignore")

            if not document.strip():
                print("Skipping whitespace-only document")
                continue

            tree = html.fromstring(document)