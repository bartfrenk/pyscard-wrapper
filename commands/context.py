from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest


class CardContext(object):

    def __init__(self, card_type=None, timeout=1):
        self.cardservice = None
        self._card_type = card_type or AnyCardType()
        self._timeout = timeout

    def __enter__(self):
        """Set up context with a connection to the card."""
        cr = CardRequest(timeout=self._timeout, cardType=self._card_type)
        self.cardservice = cr.waitforcard()
        self.cardservice.connection.connect()
        return self

    def __exit__(self, exc_class, exc_instance, traceback):
        """Catch exceptions thrown in the context."""
        return False
