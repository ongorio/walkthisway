from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from pathlib import Path
from PIL import Image

def image_upload_handler(instance, filename) -> str:
    result = 'products'
    extension = Path(filename).suffix
    result = Path(result, instance.name + extension)
    return str(result)

class Product(models.Model):
    name = models.CharField('Name', max_length=255, unique=True)
    slug = models.SlugField('Slug', max_length=255, unique=True)
    description = models.TextField('Description')
    price = models.DecimalField('Price', max_digits=8, decimal_places=2)
    image = models.ImageField('Image', upload_to=image_upload_handler)
    quantity = models.IntegerField('Quantity', default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        
        if Path(self.image.path).exists():
            img = Image.open(self.image.path)
            if img.height > 500 or img.width > 500:
                img.thumbnail((500, 500))
                img.save(self.image.path)
        
        super().save(*args, **kwargs)
        
        
    def delete(self, *args, **kwargs):
        img_path = Path(self.image.path)
        if img_path.exists():
            img_path.unlink()

        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self) -> str:
        return f'{self.name}'
    

    def __repr__(self) -> str:
        return f'<Product> {self.__str__}'
    

