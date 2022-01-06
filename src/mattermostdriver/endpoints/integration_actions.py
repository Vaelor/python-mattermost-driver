from .base import Base


class IntegrationActions(Base):
    endpoint = "/actions"

    def open_dialog(self, options):
        return self.client.post(self.endpoint + "/dialogs/open", options=options)

    def submit_dialog(self, options):
        return self.client.post(self.endpoint + "/dialogs/submit", options=options)
