class File:
    """
    Class representing an audio file.

    It has the following properties:
        - path
        - site
        - date
        - meta_values
    """

    def __init__(
        self,
        path: str,
    ):
        self.__path = path

        self.__site = ''
        self.__date = ''
        self.__meta_values = []
