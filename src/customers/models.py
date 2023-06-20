from django.db import models

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField('First Name', max_length=255)
    last_name = models.CharField('Last Name', max_length=255)
    email = models.EmailField('Email', unique=True)
    user = models.OneToOneField('auth.User',models.SET_NULL, related_name='customer', null=True, blank=True)
    date_registered = models.DateField()

    def __str__(self) -> str:
        return f'{self.email}'
    

    def __repr__(self) -> str:
        return f'<Customer> {self.__str__}'

    # zip_code = models.CharField('Zip Code', max_length=20)
    # city = models.CharField('City', max_length=255)
    # state = models.CharField('State', max_length=255)
    # address_line1 = models.CharField('Address Line 1', max_length=500)
    # address_line2 = models.CharField('Address Line 2', max_length=500)