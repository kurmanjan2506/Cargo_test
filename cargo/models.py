from django.db import models
import random
import string

def gen_unique_num():
    num = random.randint(1000,9999)
    letter = random.choice(string.ascii_uppercase)
    res = f'{num}{letter}'
    return res

class Location(models.Model):
    '''Модель для хранения информации о локациях'''
    city = models.CharField(max_length=50)
    state_name = models.CharField(max_length=50)
    zip = models.CharField(max_length=30)
    lat = models.CharField(max_length=30)
    lng = models.CharField(max_length=30)

    def __str__(self):
        return f'Location of №{self.city}'
    
    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

class Cargo(models.Model):
    '''Модель для хранения информации о грузах'''
    pick_up_loc = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='pick_up_locs')
    delivery_loc = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='delivery_locs')
    weight = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f'Cargo №{self.id}'
    
    class Meta:
        verbose_name = 'Груз'
        verbose_name_plural = 'Грузы'


class Car(models.Model):
    '''Модель для хранения информации о машинах'''
    unique_num = models.CharField(max_length=5, unique=True, default=gen_unique_num())
    curr_loc = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='cars_loc')
    load_cap = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'Car №{self.unique_num}'
    
    def save(self, *args, **kwargs):
        '''
        Если текущая локация машины не задана, выбирает случайную локацию 
        и присваивает ее текущей локации машины
        '''
        if not self.curr_loc:
            self.curr_loc = self.random_location()
        super().save(*args, **kwargs)

    def random_location(self):
        '''Возвращает случайную локацию из существующих локаций'''
        all_locations = Location.objects.all()
        random_location = random.choice(all_locations)
        return random_location

    def __str__(self):
        return f'Car №{self.unique_num}'
    
    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'