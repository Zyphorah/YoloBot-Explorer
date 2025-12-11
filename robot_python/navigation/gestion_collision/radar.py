from navigation.gestion_collision.interfaces.i_radar import i_radar

class Radar(i_radar):
    def __init__(self, radar):
        self.radar = radar

    def obtenir_distance(self):
        return self.radar.distance * 100  # distance en cm
