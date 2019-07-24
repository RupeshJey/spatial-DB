# Rupesh Jeyaram 
# Created July 23rd, 2019

# A superclass for Shape Layers (Also, the None Shape Layer)

# Each layer (US county, worldwide, Chinese Province, etc.) presents its 
# own shapes and averages onto the map, but performs the same essential 
# tasks. Thus, it makes sense to create a Shape Layer superclass that 
# each specific layer inherits. 

class ShapeLayer: 
    def __init__(self):
        self.name = 'None'

    def get_data_for_date_range(start_date, end_date):
        return 