class QueueStats:
    def __init__(self, pending=0, success=0, dlq=0):
        self.pending = pending
        self.success = success
        self.dlq = dlq
