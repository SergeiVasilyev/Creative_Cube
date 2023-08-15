from .paypal_model import *


def create_paypal_data_request(order):
    currency_code = 'USD'
    unit = Unit_amount()
    items = []
    pre_sum = 0
    for item in order.items.all():
        print(item.product.name, item.quantity, item.product.price)
        unit = Unit_amount(currency_code, f'{item.product.price:.2f}')
        items.append(Item(name=item.product.name, quantity=str(item.quantity), unit_amount=unit))
        pre_sum += Decimal(unit.value) * int(item.quantity)

    amount = Amount(currency_code, f'{pre_sum:.2f}', Breakdown(Item_total(currency_code, f'{pre_sum:.2f}')))
    p = Purchase_units(items=items, amount=amount)

    data = Paypal_data(
        intent="CAPTURE",
        purchase_units=[p]
    )
    # print(data.toJson())
    return data.toJson()



