from django.db import models
from operator import itemgetter
from django.db.models import Count

class Order(models.Model):
    FCM = 'FCM'
    PRI = 'PRI'
    SHIPPING_CHOICES = (
        ('FCM', 'First Class Mail'),
        ('PRI', 'Priority Mail'),
    )
    shipping_method = models.CharField(max_length=100, choices=SHIPPING_CHOICES)
    date_completed = models.DateTimeField()
    
    @staticmethod
    def split_by_shipping_method():
        fcm = list(Order.objects.filter(shipping_method='FCM').values_list('pk', flat=True))
        pri = list(Order.objects.filter(shipping_method='PRI').values_list('pk', flat=True))
        return [fcm, pri]

    
    @staticmethod
    def split_by_single_and_multiple():
        singles = []
        multiples = []
        orders = Order.objects.all()
        
        for order in orders:
            if order.items.count() == 1:
                singles.append(order.id)
            else:
                multiples.append(order.id)
        
        return [singles, multiples]

    
    @staticmethod
    def single_orders_are_sorted():
        unsorted_orders = []
        orders = Order.objects.annotate(item_count=Count('items')).filter(item_count=1)
        
        #Get priority (key, value) dictionary
        priority = orders[0].items.first().priority
        
        for order in orders:
            #since these are single orders, they can be found at items.first()
            only_order = order.items.first()
            
            #store the priority at index 0, and the order_id at index 1
            unsorted_orders.append([priority[only_order.product], only_order.order.id])
       
        #sort by using the priority number (stored at index 0) 
        sorted_orders = sorted(unsorted_orders, key=itemgetter(0))
        
       
        #create a new array with only the order_id
        sorted_ids = []
        for i in range (0, len(sorted_orders)):
            sorted_ids.append(sorted_orders[i][1])
         
        return sorted_ids     


    @staticmethod
    def orders_split_by_xxl_and_not():
        xxl = []
        no_xxl = []
        orders = Order.objects.annotate(item_count=Count('items')).filter(item_count__gt=1)

        for order in orders:
            has_xxl = False
	    for item in order.items.all():
		if item.product == 'XXL':
		    xxl.append(order.id)
		    has_xxl = True
		    break
	    if has_xxl == False:
		no_xxl.append(order.id)

        return [xxl, no_xxl] 

     
class OrderItem(models.Model):
    XS = 'XS'
    S = 'S'
    M = 'M'
    L = 'L'
    XL = 'XL'
    XXL = 'XXL'
    PRODUCT_CHOICES = (
        ('XS', 'Extra Small Tee'),
        ('S', 'Small Tee'),
        ('M', 'Medium Tee'),
        ('L', 'Large Tee'),
        ('XL', 'Extra Large Tee'),
        ('XXL', 'Double Extra Large Tee'),
    )
    priority = {'XS': 0, 'S': 1, 'M': 2, 'L': 3, 'XL': 4, 'XXL': 5}
    order = models.ForeignKey(Order, related_name='items')
    product = models.CharField(max_length=100, choices=PRODUCT_CHOICES)
    quantity = models.PositiveIntegerField(default=1)
