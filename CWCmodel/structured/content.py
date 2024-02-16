class Content:
    """
    Common base class for all articles/pages
    """
    def __init__(self, topic, title, body, url):
        self.topic = topic
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        print('-------------------------------')
        """
        Flexible printing function controls output
        """
        print("New article found for topic: {}".format(self.topic))
        print("URL: {}".format(self.url))
        print("TITLE: {}".format(self.title))
        print("BODY:\n{}".format(self.body))