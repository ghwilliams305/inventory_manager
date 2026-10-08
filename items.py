#Defing Items class
class Item:
    name = "Unnamed Item"
    quantity = 1
    unit = "unit"
    building = "home"

    def __init__(self, *item_data):
        amount_of_data = len(item_data)

        if amount_of_data > 1: 
            self.name = item_data[1]

        else:
            self.name = "Unnamed Item"

        if amount_of_data > 2:
            self.quantity = item_data[2]

        else:
            self.quantity = 1

        if amount_of_data > 3: 
            self.unit = item_data[3]

        else:
            self.unit = "unit"

        if amount_of_data > 4: 
            self.building = item_data[4]
        
        else:
            self.building = "home"

        if amount_of_data > 5: 
            self.room = item_data[6]
                        
        else:
            self.room = "unknown"

        if amount_of_data > 6: 
            self.placement = item_data[5]

        else:
            self.placement = 'unknown'