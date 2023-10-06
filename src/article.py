class Article():

    def __init__(self, article_data: dict):
        self._author = article_data["author"]
        self._title = article_data["title"]
        self._url = article_data["url"]
        self._source = article_data["source"]

        self._description = article_data["description"] # summary of content
        self._content = article_data["content"]  # full content of the article
        self._published_at = article_data["publishedAt"]

    def __repr__(self):
        return f"Author:{self._author}, Title:{self._title}, Url:{self._url},Description:{self._description}\n,Content:{self._content},PublishedAt:{self._published_at}"