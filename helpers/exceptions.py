class FragmentException(Exception):
    def __init__(self, detail):
        self.detail = detail

    def __str__(self):
        return self.detail
