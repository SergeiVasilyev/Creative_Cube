from dataclasses import dataclass, asdict, field
from typing import List, Dict
from decimal import *
import json
import os

# https://www.youtube.com/watch?v=Fu0swCLAJ8E
# https://youtu.be/zN4VCb0LbQI

# print(os.getcwdb())

# getcontext().prec = 2
# print(getcontext())

@dataclass
class Unit_amount:
    currency_code: str ='USD'
    value: Decimal = 0


@dataclass
class Item:
    name: str
    quantity: int
    unit_amount: Unit_amount = field(default_factory=dict)
    # unit_amount: Dict[str, Unit_amount]

    # def __post_init__(self):
    #     self.unit_amount = Unit_amount(**self.unit_amount.__dict__)

@dataclass
class Item_total(Unit_amount):
    pass

@dataclass
class Breakdown:
    item_total: Item_total = field(default_factory=None)

@dataclass
class Amount:
    currency_code: str
    value: Decimal
    breakdown: str

@dataclass
class Purchase_units:
    items: list[Item] = field(default_factory=list)
    amount: Amount = field(default_factory=None)

    # def __post_init__(self):
    #     self.items = [Item(**item.__dict__) for item in self.items]
    
    def toJson(self):
        return json.dumps(asdict(self))
    
@dataclass
class Paypal_data:
    intent: str
    purchase_units: list[Purchase_units] = field(default_factory=list)

    # def __post_init__(self):
    #     self.purchase_units = [Purchase_units(**purchase_unit) for purchase_unit in self.purchase_units]
    
    def toJson(self):
        return json.dumps(asdict(self), indent=2)
    

if __name__ == "__main__":
    f = open('Backend/shop/request.json')
    responseJSON = json.load(f) # Make a dict
    print(responseJSON)

    items = Paypal_data(**responseJSON)
    print(items.toJson()) # Make json 