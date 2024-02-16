# import inspect



class Website:
    """
    Contains information about website structure
    """

    def __init__(self, name, url, targetPattern, absoluteUrl,
        titleTag, bodyTag):
        self.name = name
        self.url = url
        self.targetPattern = targetPattern
        self.absoluteUrl=absoluteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag

        # print(str(self))
        # print(str(self.name))
        # print(str(self.searchUrl))

    def __repr__(self): 
        return "This is class {}".format(self.bodyTag)

# signature = inspect.signature(Website.__init__).parameters
# for name, parameter in signature.items():
#     print(name, parameter.default, parameter.annotation, parameter.kind)