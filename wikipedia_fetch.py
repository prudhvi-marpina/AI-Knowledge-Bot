import wikipediaapi

wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent="EduBot"
)

def fetch_wikipedia(entity, multiple=False):
    """
    Fetch content from Wikipedia. If multiple=True, return a list of paragraphs.
    """
    page = wiki_wiki.page(entity)
    if not page.exists():
        return "Page not found!" if not multiple else []

    if multiple:
        # Combine summary and up to 10 paragraphs
        paragraphs = [page.summary] + [p.strip() for p in page.text.split("\n")[:10] if p.strip()]
        return paragraphs
    return page.summary
