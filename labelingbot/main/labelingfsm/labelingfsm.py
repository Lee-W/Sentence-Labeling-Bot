from .botfsm import BotGraphMachine


class LabelingMachine(BotGraphMachine):
    def on_enter_ask_usage(self, event):
        raise NotImplementedError

    def on_enter_user(self, event):
        raise NotImplementedError

    def on_enter_wait_user_alternative(self, event):
        raise NotImplementedError

    def on_enter_wait_user_binary_response(self, event):
        raise NotImplementedError

    def on_enter_wait_user_similarity_score(self, event):
        raise NotImplementedError

    def is_asking_usage(self, event):
        raise NotImplementedError

    def is_answering_alternative(self, event):
        raise NotImplementedError

    def is_answering_binary(self, event):
        raise NotImplementedError

    def is_answering_score(self, event):
        raise NotImplementedError

    def is_answering(self, event):
        raise NotImplementedError

    def is_quitting(self, event):
        raise NotImplementedError
