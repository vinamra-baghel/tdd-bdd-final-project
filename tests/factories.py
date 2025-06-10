# Copyright 2016, 2022 John J. Rofrano. All Rights Reserved.
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

# pylint: disable=too-few-public-methods

"""
Test Factory to make fake objects for testing
"""
import factory
from faker import Faker
from factory.fuzzy import FuzzyChoice, FuzzyDecimal, FuzzyAttribute
from service.models import Product, Category

faker = Faker()


class ProductFactory(factory.Factory):
    """Creates fake products for testing"""

    class Meta:
        """Maps factory to data model"""

        model = Product

    id = factory.Sequence(lambda n: n)
    # Add code to create Fake Products
    name = FuzzyChoice([
        "Hat", "Pants", "Shirt",
        "Apple", "Banana",
        "Pots", "Towels",
        "Ford", "Chevy",
        "Hammer", "Wrench"
    ])
    # faker = Faker()
    description = FuzzyAttribute(lambda: faker.sentence(nb_words=6))
    price = FuzzyDecimal(0.5, 2000.0, precision=2)
    available = FuzzyChoice([True, False])
    category = FuzzyChoice([
        Category.UNKNOWN,
        Category.CLOTHS,
        Category.FOOD,
        Category.HOUSEWARES,
        Category.AUTOMOTIVE,
        Category.TOOLS
    ])
