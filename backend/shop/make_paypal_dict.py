from .paypal_model import *

def gen_test_data():
    unit = Unit_amount()
    items = []
    pre_sum = 0
    for n in range(3):
        unit.currency_code = 'USD'
        unit.value = f'{5:.2f}'
        items.append(Item(f'item {n}', str(n+2), unit))
        pre_sum += Decimal(unit.value) * (n+2)

    amount = Amount('USD', f'{pre_sum:.2f}', Breakdown(Item_total('USD', f'{pre_sum:.2f}')))
    p = Purchase_units(items=items, amount=amount)

    data = Paypal_data(
        intent="CAPTURE",
        purchase_units=[p]
    )

    print(data.toJson())
    return data.toJson()


if __name__ == "__main__":
    gen_test_data()
