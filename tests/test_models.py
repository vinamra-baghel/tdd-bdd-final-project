# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Product Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_models.py:TestProductModel

"""
import os
import logging
import unittest
from decimal import Decimal
from service.models import Product, Category, db
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertEqual(product.available, True)
        self.assertEqual(product.price, 12.50)
        self.assertEqual(product.category, Category.CLOTHS)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = ProductFactory()
        product.id = None
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)
        # Check that it matches the original product
        new_product = products[0]
        self.assertEqual(new_product.name, product.name)
        self.assertEqual(new_product.description, product.description)
        self.assertEqual(Decimal(new_product.price), product.price)
        self.assertEqual(new_product.available, product.available)
        self.assertEqual(new_product.category, product.category)

    #
    # ADD YOUR TEST CASES HERE
    #

    def test_read_product(self):
        """Test reading a product"""
        product = ProductFactory()
        print(f"DEBUG_LOG: Created product = {product}")
        product.id = None
        product.create()
        self.assertIsNotNone(product.id, "Assign product ID")
        found_product = Product.find(product.id)
        self.assertIsNotNone(found_product, "Product not found in the database")
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.description, product.description)
        self.assertEqual(found_product.price, product.price)
        self.assertEqual(found_product.available, product.available)
        self.assertEqual(found_product.category, product.category)

    def test_update_a_product(self):
        """Test updating a product"""
        product = ProductFactory()
        product.id = None
        product.create()
        print(f"DEBUG: Product after creation = {product}")
        self.assertIsNotNone(product.id, "Assign product ID")

        product.description = "New description"
        original_id = product.id
        product.update()
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.description, "New description")

        products = Product.all()
        self.assertEqual(len(products), 1, "Multiple products found")
        self.assertEqual(products[0].id, original_id)
        self.assertEqual(products[0].description, "New description")

    def test_delete_a_product(self):
        """Test deleting a product"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertEqual(len(Product.all()), 1)
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_list_all_products(self):
        """Test listing all products"""
        products = Product.all()
        self.assertEqual(len(products), 0)

        for _ in range(5):
            product = ProductFactory()
            product.create()

        products = Product.all()
        self.assertEqual(len(products), 5)

    def test_find_by_name(self):
        """Test finding a product by name"""
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()

        name = products[0].name
        prod_count = len([product for product in products if product.name == name])
        found_products = Product.find_by_name(name)
        self.assertEqual(found_products.count(), prod_count)

        for product in found_products:
            self.assertEqual(product.name, name)

    def test_find_by_availability(self):
        """Test finding a product by availability"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()

        available = products[0].available
        prod_count = len([product for product in products if product.available == available])
        found_products = Product.find_by_availability(available)
        self.assertEqual(found_products.count(), prod_count)

        for product in found_products:
            self.assertEqual(product.available, available)

    def test_find_by_category(self):
        """Test finding a product by category"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()

        category = products[0].category
        prod_count = len([product for product in products if product.category == category])
        found_products = Product.find_by_category(category)
        self.assertEqual(found_products.count(), prod_count)

        for product in found_products:
            self.assertEqual(product.category, category)

    def test_find_by_price(self):
        """Test finding a product by price"""
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()

        target_price = products[0].price
        prod_count = len([product for product in products if product.price == target_price])

        found_product = Product.find_by_price(target_price)
        self.assertEqual(found_product.count(), prod_count)

        for product in found_product:
            self.assertEqual(product.price, target_price)

    def test_find_by_price_when_str(self):
        """Test finding a product by string price"""
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()

        products[0].price = str(products[0].price)
        target_price = products[0].price
        prod_count = len([product for product in products if product.price == target_price])

        found_product = Product.find_by_price(target_price)
        self.assertEqual(found_product.count(), prod_count)

        for product in found_product:
            self.assertEqual(product.price, target_price)
