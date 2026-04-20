from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from decimal import Decimal

# Create your models here.
class User(AbstractUser):
    pass

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_count = models.IntegerField(default=0)

    """ 
    Meta class is a Django class that is used to define metadata for the model.
    In models, the class Meta is used to define Model Meta options that change how the model interacts with
    the database and the Django admin interface. 
    This is a Django constraint that is used to ensure that the price and stock count are always positive.
    """
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="price_gt_0",
            ),
            models.CheckConstraint(
                condition=models.Q(stock_count__gte=0),
                name="stock_count_gt_0",
            ),
        ]

    def get_discounted_price(self, discount_percentage: int) -> Decimal:
        """ Calculate the discounted price of the product """
        return self.price * (1 - discount_percentage / 100)

    #  The property decorator is a Django decorator that is used to define a property on the model.
    # This makes the method act like a property, meaning it can be accessed like an attribute on the
    #  model instance. for example, if you have a product instance, you can access the in_stock property 
    # like this: product.in_stock.
    @property
    def in_stock(self) -> bool:
        # return True if the product is in stock, otherwise return False
        return self.stock_count > 0

    #  The Clean Method is a Django method that is used to perform validation on the model data.
    #  It is called before the model is saved to the database.
    def clean(self):
        # perform validation on the model data
        if self.price < 0:
            raise ValidationError("Price cannot be negative")
        if self.stock_count < 0:
            raise ValidationError("Stock count cannot be negative")
        

