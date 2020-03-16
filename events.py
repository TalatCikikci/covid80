
class EVENT_MAX_ERROR(Exception):
    pass

class Event(object):
    priority = 0
    message = ""
    effects = ()
    instance_max = -1
    instance_count = 0

    def __init__(self):
        from game import Game
        if self.instance_max > 0:
            if self.instance_count < self.instance_max:
                Game.new_events.append(self)
            else:
                raise EVENT_MAX_ERROR

class VirusMutated(Event):
    message = "There is now another mutation of the virus."

class VirusSequenced(Event):
    message = "Scientists have succesfully sequenced a virus variation. You can now start testing people."
    instance_max = 1

class InitialVirus(Event):
    message = "Doctors are suspecting that a new type of virus is making people sick in %s."
    instance_max = 1

    def __init__(self, country):
        super(InitialVirus, self).__init__()
        self.message = self.message % country.name


