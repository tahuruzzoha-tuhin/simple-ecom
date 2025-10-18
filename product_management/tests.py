# Product Model Tests
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.text import slugify
from .models import Product, Category 
from PIL import Image
import tempfile
import os


#Django Test Cases class based tests
class CategoryModelTest(TestCase):
    def setUp(self):
        Category.objects.create(
            name="Test-Category", 
            slug="test-category", 
            description="A category for testing."
        )

    def test_category_created_successfully(self):
        category = Category.objects.get(name="Test-Category")
        self.assertEqual(category.slug, "test-category")

    def test_str_method(self):
        category = Category.objects.get(name="Test-Category")
        self.assertEqual(str(category), "Test-Category")






class ProductModelTest(TestCase):

    def setUp(self):
        # Create a temporary category
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )

        # Create a temporary image for testing
        temp_image = Image.new('RGB', (800, 800), color='red')
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        temp_image.save(temp_file)
        temp_file.seek(0)

        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open(temp_file.name, 'rb').read(),
            content_type='image/jpeg'
        )
        os.remove(temp_file.name)

        # Create a Product
        self.product = Product.objects.create(
            category=self.category,
            name="Smartphone",
            slug=slugify("Smartphone"),
            description="Latest 5G smartphone",
            price=999.99,
            available=True,
            stock=10,
            rating=5,
            image=self.image
        )

    def test_product_creation(self):
        """Test product is created successfully and linked to category"""
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(self.product.category.name, "Electronics")
        self.assertEqual(self.product.name, "Smartphone")
        self.assertTrue(self.product.available)

    def test_product_str_method(self):
        """Test the __str__ method"""
        self.assertEqual(str(self.product), "Smartphone")

    def test_product_ordering(self):
        """Test ordering by created_at"""
        product2 = Product.objects.create(
            category=self.category,
            name="Laptop",
            slug=slugify("Laptop"),
            description="Gaming laptop",
            price=1500.00,
            available=True,
            stock=5
        )
        products = Product.objects.all()
        self.assertEqual(products[0], self.product)  # oldest first



    def test_image_resized_on_save(self):
        """Test that image is resized if too large"""
        img_path = self.product.image.path
        with Image.open(img_path) as img:
            self.assertLessEqual(img.width, 600)
            self.assertLessEqual(img.height, 600)

    def tearDown(self):
        """Clean up image files after test"""
        if self.product.image:
            if os.path.exists(self.product.image.path):
                os.remove(self.product.image.path)




# Using Pytest Funtional Tests
import pytest
from django.utils.text import slugify
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Category, Product
from PIL import Image
import tempfile
import os

@pytest.mark.django_db
def test_category_creation_and_str():
    category = Category.objects.create(
        name="Electronics",
        slug=slugify("Electronics"),
        description="Electronic devices"
    )
    assert str(category) == "Electronics"
    assert Category.objects.count() == 1
    assert category.slug == "electronics"


@pytest.mark.django_db
def test_product_creation_and_str():
    # Create category first
    category = Category.objects.create(
        name="Gadgets",
        slug=slugify("Gadgets"),
        description="All gadgets"
    )

    # Create a temporary test image
    temp_image = Image.new('RGB', (800, 800), color='red')
    temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    temp_image.save(temp_file)
    temp_file.seek(0)

    image = SimpleUploadedFile(
        name='test_image.jpg',
        content=open(temp_file.name, 'rb').read(),
        content_type='image/jpeg'
    )
    os.remove(temp_file.name)

    # Create product
    product = Product.objects.create(
        category=category,
        name="Smartphone",
        slug=slugify("Smartphone"),
        description="Latest 5G smartphone",
        price=999.99,
        available=True,
        stock=20,
        rating=5,
        image=image
    )

    # Assertions
    assert str(product) == "Smartphone"
    assert product.category == category
    assert product.price == 999.99
    assert product.available is True
    assert Product.objects.count() == 1

    # Check image resizing
    img_path = product.image.path
    with Image.open(img_path) as img:
        assert img.width <= 600
        assert img.height <= 600

    # Cleanup
    if os.path.exists(product.image.path):
        os.remove(product.image.path)
