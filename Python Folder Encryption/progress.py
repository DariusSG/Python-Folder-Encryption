import progressbar


class ProgressBar():
    def __init__(self, length):
        self.widgets = [progressbar.Percentage(), progressbar.Bar()]
        self.bar = progressbar.ProgressBar(
            widgets=self.widgets, max_value=length).start()
        self.value, self.max_value = 0, length
        self.bar.update(0)

    def update(self):
        if self.value == self.max_value:
            self.bar.finish()
        else:
            self.bar.update(self.value + 1)

    def finish(self):
        self.bar.finish()
