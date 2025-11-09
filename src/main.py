import time
from navigation import facade_navigation
from navigation.gestion_collision.radar import Radar

navigation = facade_navigation.FacadeNavigation()

navigation.avancer()
time.sleep(20)
