from flask import Flask, request, jsonify
from api.models import db, Walmart, Loblaws, Superstore, Metro
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/getall', methods=['GET'])
def get_all():
    all_items = set(
        [item.generalized_name for item in Walmart.query.all()] +
        [item.generalized_name for item in Loblaws.query.all()] +
        [item.generalized_name for item in Superstore.query.all()] +
        [item.generalized_name for item in Metro.query.all()]
    )
    return jsonify(list(all_items))

@app.route('/cheapest', methods=['POST'])
def cheapest():
    items = request.json.get('items', [])
    results = []

    for item in items:
        walmart_item = Walmart.query.filter_by(generalized_name=item).first()
        loblaws_item = Loblaws.query.filter_by(generalized_name=item).first()
        superstore_item = Superstore.query.filter_by(generalized_name=item).first()
        metro_item = Metro.query.filter_by(generalized_name=item).first()

        prices = [
            (walmart_item.price, 'Walmart') if walmart_item else (float('inf'), 'Walmart'),
            (loblaws_item.price, 'Loblaws') if loblaws_item else (float('inf'), 'Loblaws'),
            (superstore_item.price, 'Superstore') if superstore_item else (float('inf'), 'Superstore'),
            (metro_item.price, 'Metro') if metro_item else (float('inf'), 'Metro')
        ]
        cheapest = min(prices, key=lambda x: x[0])
        results.append({'item': item, 'store': cheapest[1], 'price': cheapest[0]})
    
    return jsonify(results)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5001)  # Ensure the port here matches the one in run.py