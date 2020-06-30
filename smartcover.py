import appdaemon.plugins.hass.hassapi as hass
import time

class SmartCover(hass.Hass):
    """Smart cover control based on state"""
    
    def initialize(self):  
        self.entities = self.args["entities"]
        self.cover = self.entities["cover"]
        self.sensor_state = self.entities["sensor"]
        self.light = self.entities["light"]
        self.listen_state(self.statechange, self.sensor_state)
        self.listen_state(self.blindpositionchange, self.cover, attribute="current_position")
        
    def statechange(self, entity, attribute, old, new, kwargs):
        self.log(new)
        self.coverstate = self.get_state(self.cover)
        self.coverposition = self.get_state(self.cover, attribute="current_position")
        self.log("Position: " + str(self.coverposition))
        if new == "Key Held down" or new == "14":
           self.log(self.coverstate)
           # Don't toggle the light if using a dimmer state switch. Unfortunately the Switch/Switch 2 toggles the load when activating a scene.
           # The dimmer doesn't exhibit this behaviour so we can ignore it.
           if new != "14":
              self.call_service("light/toggle", entity_id = self.light)
           if self.coverstate == "opening" or self.coverstate == "closing":
              self.call_service("cover/stop_cover", entity_id=self.cover)
              self.log("Stopping Blind")
           elif self.coverstate == "closed":
              self.call_service("cover/open_cover", entity_id=self.cover)
              self.log("Opening Blind")
           elif self.coverposition > 50:
              self.call_service("cover/close_cover", entity_id=self.cover)
              self.log("Closing Blind")
           else:
              self.call_service("cover/open_cover", entity_id=self.cover)
              self.log("Opening Blind")
    
    def blindpositionchange(self, entity, attribute, old, new, kwargs):
        self.log(new)
        if new == 100 or new == 0:
           self.call_service("cover/stop_cover", entity_id=self.cover)
           self.log("Stopping Cover")
    
        
