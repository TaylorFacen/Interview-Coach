from bson.json_util import dumps

from .helper import app, DB

@app.route('/api/categories')
def get_categories():
	db = DB() 
	categories = list(map(lambda category: {
            'id': str(category['_id']),
            'category': category['category'],
            'description': category['description']
			}, db.get_categories())) 

	return {'categories': dumps(categories)}