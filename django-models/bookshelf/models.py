from django.db import models


class Book(models.Model):
    
    IN_STOCK = 'in stock'
    OUT_OF_STOCK = 'out of stock'
    RESERVED = 'reserved'
    LOST = 'lost'
    STATUS_CHOICES = [
        (IN_STOCK, 'In Stock'),
        (OUT_OF_STOCK, 'Out of Stock'),
        (RESERVED, 'Reserved'),
        (LOST, 'Lost'),
    ]
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)

    publication_year = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.title} by {self.author}"
