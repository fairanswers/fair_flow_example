import fair_flow

class FeedDog(fair_flow.Activity):
    def execute(self, context=None):
        print("Starting feed dog")
        # Put feed dog code here

class CheckWater(fair_flow.Activity):
    def execute(self, context=None):
        print("Checking the dog's water")
        # We'll hard-code this to true for now.
        self.returned=True


class WaterDog(fair_flow.Activity):
    def execute(self, context=None):
        print("Starting water dog")
        # Put water dog code here

class MedicateDog(fair_flow.Activity):
    def execute(self, context=None):
        print("Starting medicate dog")
        # Put medicate dog code here
        # Set Pills Left in context

class OrderMedication(fair_flow.Activity):
    def execute(self, context=None):
        print("Starting order_medication dog")
        # Put order_medication dog code here

