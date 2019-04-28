class Player(object):
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def get_name(self):
        """
        This function returns player name
        """
        return self.name

    def get_color(self):
        """
        This function return player color
        """
        return self.color
