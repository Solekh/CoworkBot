

def send_order_to_employee():
    pass

def order_make_text(data):
    text = """Buyurtma raqami #{order_id}

Kategoriya: {category_name}

Proyektning nomi: {name}

{description}

Proyektning narxi: {price}"""
    return text.format(
       **data
    )

