import appdaemon.plugins.hass.hassapi as hass

class ResetCover(hass.Hass):
    """Set the cover state based on position"""
    
    def initialize(self):  
        self.entities = self.args["entities"]
        self.cover = self.entities["cover"]
        self.listen_state(self.blindpositionchange, self.cover, attribute="current_position")
        
    def blindpositionchange(self, entity, attribute, old, new, kwargs):
        self.log(new)
        if new == 100 or new == 0:
           self.call_service("cover/stop_cover", entity_id=self.cover)
           self.log("Stopping Cover")
