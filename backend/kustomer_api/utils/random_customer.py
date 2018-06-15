from faker import Factory

fake = Factory.create('es_ES')

def random_customer():
    """Create a customer with random data."""
    customer = fake.profile(fields=['mail', 'name'])
    return {
      'name': customer.get('name'),
      'emails': [{'email': customer.get('mail')}]
    }
