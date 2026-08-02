from bs4 import BeautifulSoup
from ebooklib import epub, ITEM_DOCUMENT

from app.library.book import Chapter
from app.reader.epub_utils import filtered_toc


def extract_between(soup, start_id=None, end_id=None):

    if start_id:
        start = soup.find(id=start_id)

        if start is None:
            return ""

    else:
        start = soup.body or soup

    text = []

    node = start

    while node:

        if (
            end_id
            and node is not start
            and getattr(node, "attrs", None)
            and node.get("id") == end_id
        ):
            break

        if hasattr(node, "get_text"):

            t = node.get_text(" ", strip=True)

            if t:
                text.append(t)

        node = node.find_next()

    return "\n".join(text)


def load_chapters(path):

    book = epub.read_epub(str(path))

    documents = {}

    for item in book.get_items():

        if item.get_type() != ITEM_DOCUMENT:
            continue

        soup = BeautifulSoup(item.get_content(), "xml")

        for tag in soup(["script", "style"]):
            tag.decompose()

        documents[item.get_name()] = soup

    id_to_name = {
        item.get_id(): item.get_name()
        for item in book.get_items()
        if item.get_type() == ITEM_DOCUMENT
    }

    spine = [
        id_to_name[idref]
        for idref, _ in book.spine
        if idref != "nav" and idref in id_to_name
    ]

    toc = filtered_toc(book)

    chapters = []

    for i, entry in enumerate(toc):

        next_entry = toc[i + 1] if i + 1 < len(toc) else None

        start_file, _, start_anchor = entry.href.partition("#")

        if next_entry:
            end_file, _, end_anchor = next_entry.href.partition("#")
        else:
            end_file = None
            end_anchor = None

        pieces = []

        start_index = spine.index(start_file)

        end_index = (
            spine.index(end_file)
            if end_file
            else len(spine) - 1
        )

        for index in range(start_index, end_index + 1):

            filename = spine[index]

            soup = documents[filename]

            if filename == start_file == end_file:

                pieces.append(
                    extract_between(
                        soup,
                        start_anchor,
                        end_anchor,
                    )
                )

            elif filename == start_file:

                pieces.append(
                    extract_between(
                        soup,
                        start_anchor,
                    )
                )

            elif filename == end_file:

                pieces.append(
                    extract_between(
                        soup,
                        None,
                        end_anchor,
                    )
                )

            else:

                pieces.append(
                    soup.get_text("\n", strip=True)
                )

        chapters.append(
            Chapter(
                title=entry.title,
                text="\n\n".join(pieces),
            )
        )

    return chapters