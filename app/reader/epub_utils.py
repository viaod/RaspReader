from ebooklib import epub


SKIP_TOC = {
    "cover",
    "contents",
    "table of contents",
    "copyright",
    "ecopyright",
    "license",
    "title page",
    "titlepage",
    "introduction",
    "foreword",
    "preface",
    "acknowledgements",
    "acknowledgments",
    "about the author",
    "the full project gutenberg™ license",
    "donate",
}


def flatten_toc(entries):

    links = []

    for entry in entries:

        if isinstance(entry, epub.Link):
            links.append(entry)

        elif isinstance(entry, tuple):

            section, children = entry

            if getattr(section, "href", None):
                links.append(
                    epub.Link(section.href, section.title, "")
                )

            links.extend(flatten_toc(children))

    return links


def filtered_toc(book):

    return [
        entry
        for entry in flatten_toc(book.toc)
        if entry.title.strip().lower() not in SKIP_TOC
    ]