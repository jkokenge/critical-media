class MediaURLFetchError(Exception):
     def __init__(self, url):
         self.url = url
     def __str__(self):
         return repr(self.url)