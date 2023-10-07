class Article:

    def __init__(self, article_data: dict):

        self._content_length_upper_bound = 25

        self._author = article_data["author"]
        self._title = article_data["title"]
        self._url = article_data["url"]
        self._source = article_data["source"]
        self._published_at = article_data["publishedAt"]

        self._description = article_data["description"]  # summary of content
        self._content = article_data["content"]

        # some news data provided by the API gives null description
        # get description from content(full article) for describing the article

        if self._description == None:

            self._content = self._get_content(article_data)


        # if description is not none
        # don't store content
        else:
            self._content = None

    def _get_content(self,article_data) -> str:
        if article_data["content"]:

            if len(article_data["content"]) >= self._content_length_upper_bound:

                # get the approximate words
                for i in range(len(article_data["content"])):
                    if i >= self._content_length_upper_bound and article_data["content"][i] == '.':
                        break

            # this is not an expected case but still included it because not sure what could be the API's response
            # if full article content is less than the determined upper bound length
            else:
                for i in range(-1, -1 * len(article_data["content"]) - 1, -1):
                    if article_data["content"][i] == '.':
                        # convert i to positive index
                        i = len(article_data["content"]) + i
                        break

            return article_data["content"][:i]  # full content of the article
    def __repr__(self):
        return f"Author:{self._author}, Title:{self._title}, Url:{self._url},Description:{self._description}\n,Content:{self._content},PublishedAt:{self._published_at}"
