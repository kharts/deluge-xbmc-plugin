class StatesEnum(object):

    def __init__(self):
        self.All = 'All'
        self.Finished = 'Finished'
        self.Unfinished = 'Unfinished'
        self.Unstarted = 'Unstarted'
        self.Active = 'Active'
        self.Downloading = 'Downloading'
        self.Seeding = 'Seeding'
        self.Paused = 'Paused'
        self.Queued = 'Queued'

States = StatesEnum()
