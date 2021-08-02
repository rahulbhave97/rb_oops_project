

class ViewModelBase:
    def __init__(self, event):
        self.body_json = event.get('body-json')
