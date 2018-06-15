from random import randint

from faker import Factory

fake = Factory.create('es_ES')

def random_conversation():
    """Create a customer with random data."""
    return {
        "app": "postmark",
        "channel": ["email", "sms", "chat"][randint(0, 2)],
        "preview": fake.sentence(
            nb_words=6, variable_nb_words=True, ext_word_list=None
        ),
        "subject": "Question",
        "status": ["sent", "received", "error"][randint(0, 2)],
        "size": 1,
    }
