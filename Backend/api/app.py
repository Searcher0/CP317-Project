from flask import Flask, request, jsonify
from api.models import db, Walmart, Loblaws, Superstore, Metro, NoFrills
from config import Config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)

@app.route('/getall', methods=['GET'])
def get_all():
    all_items = set(
        [item.generalized_name for item in Walmart.query.all()] +
        [item.generalized_name for item in Loblaws.query.all()] +
        # [item.generalized_name for item in Superstore.query.all()] +
        # [item.generalized_name for item in Metro.query.all()]+
        [item.generalized_name for item in NoFrills.query.all()]
    )
    return jsonify(list(all_items))

@app.route('/cheapest', methods=['POST'])
def get_cheapest_store():
    items = request.json.get('items', [])
    store_data = {'Walmart': {}, 'Loblaws': {}, 'NoFrills': {}}
    total_prices = {'Walmart': 0, 'Loblaws': 0,  'NoFrills': 0}
    missing_items = {'Walmart': [], 'Loblaws': [],  'NoFrills': []}

    for item in items:
        for store in store_data.keys():
            store_items = globals()[store].query.filter_by(generalized_name=item).all()
            if store_items:
                lowest_price_item = min(store_items, key=lambda x: x.price)
                store_data[store][item] = {
                    'name': lowest_price_item.name,
                    'price': lowest_price_item.price
                }
                total_prices[store] += lowest_price_item.price
            else:
                missing_items[store].append(item)

    sorted_stores = sorted(total_prices.items(), key=lambda x: (x[1], len(missing_items[x[0]])))

    print(sorted_stores)
    return jsonify({
        'sorted_stores': sorted_stores,
        'store_data': store_data,
        'missing_items': missing_items
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5001)  # Ensure the port here matches the one in run.py