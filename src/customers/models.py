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
    
    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
