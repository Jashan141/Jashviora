"""
Automated Test Suite for JASHVIORA Website & REST API
"""

import unittest
import json
import os
from app import app, PRODUCTS_FILE, read_json

class TestJashvioraApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'JASHVIORA', response.data)
        self.assertIn(b'Discover Your Style, Create Your World', response.data)
        self.assertIn(b'YOUR WORLD OF', response.data)
        self.assertIn(b'BEAUTY & STYLE', response.data)

    def test_health_check(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get('brand'), 'JASHVIORA')

    def test_get_products(self):
        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertGreater(data.get('count'), 0)
        self.assertIsInstance(data.get('products'), list)

        # Check required fields in the first product
        first = data['products'][0]
        self.assertIn('title', first)
        self.assertIn('category', first)
        self.assertIn('price', first)
        self.assertIn('store', first)
        self.assertIn('externalUrl', first)
        self.assertIn('image', first)

    def test_filter_products_by_category(self):
        response = self.client.get('/api/products?category=Beauty')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(all(p['category'] == 'Beauty' for p in data['products']))

    def test_filter_products_by_store(self):
        response = self.client.get('/api/products?store=Nykaa')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(all(p['store'] == 'Nykaa' for p in data['products']))

    def test_create_and_delete_product(self):
        new_prod = {
            "title": "Test Gold Huggie Hoops",
            "category": "Jewellery",
            "price": 1499,
            "originalPrice": 1999,
            "store": "Amazon India",
            "externalUrl": "https://www.amazon.in/test-hoops",
            "image": "https://images.unsplash.com/test.jpg",
            "description": "Minimal 18k gold hoop earrings.",
            "isTrending": True,
            "tags": ["Gold", "Test"]
        }
        res = self.client.post('/api/products', json=new_prod)
        self.assertEqual(res.status_code, 201)
        created = json.loads(res.data)
        self.assertTrue(created.get('success'))
        prod_id = created['product']['id']

        # Verify it appears in products
        res_get = self.client.get(f'/api/products/{prod_id}')
        self.assertEqual(res_get.status_code, 200)

        # Clean up / delete
        res_del = self.client.delete(f'/api/products/{prod_id}')
        self.assertEqual(res_del.status_code, 200)

    def test_newsletter_subscription(self):
        res = self.client.post('/api/newsletter', json={"email": "testuser@gmail.com"})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data.get('success'))

    def test_contact_submission(self):
        res = self.client.post('/api/contact', json={
            "name": "Priya Sharma",
            "email": "priya@example.com",
            "subject": "Brand Collaboration",
            "message": "Love your curated beauty collection!"
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data.get('success'))

    def test_pins_endpoint(self):
        response = self.client.get('/api/pins')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertGreater(len(data.get('pins')), 0)

    def test_assets_serving(self):
        # Check that cropped images exist and are served
        for asset in ['beauty.jpg', 'fashion.jpg', 'jewellery.jpg', 'home-decor.jpg']:
            res = self.client.get(f'/assets/collections/{asset}')
            self.assertEqual(res.status_code, 200, f"Failed serving {asset}")

if __name__ == '__main__':
    unittest.main()
