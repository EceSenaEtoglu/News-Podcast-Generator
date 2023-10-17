class Article:

    def __init__(self, author:str,title:str,source:str,published_at:str,url:str,description:str,content:str):

        self._author = author
        self._title = title
        self._source = source
        self._url = url
        self._published_at = published_at

        self._description = description # summary of content
        self._content = content

    def __get_text(self) -> str:
        """Return description (short summary from API) if exits else return content

        If content also does not exist return none"""
        if self._description:
            return self._description

        else:
            return self._content

    def __repr__(self):
        return f"Author:{self._author}, Title:{self._title}, Url:{self._url},Description:{self._description}\n,Content:{self._content},PublishedAt:{self._published_at}"
