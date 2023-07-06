from django.test import TestCase
from app.models import Stage
# Create your tests here.

class StageModelTest(TestCase):
    def test_save_method_created_slug(self):
        stage = Stage.objects.create(stage_name = "First Test")
        test_slug = 'first-test'
        self.assertEqual(stage.slug, test_slug)

    def test_save_method_with_slug(self):
        stage = Stage.objects.create(stage_name = "First Test", slug = "first-test")
        self.assertEqual(stage.slug, 'first-test')
        stage.stage_name = "Second Test"
        stage.save()
        test_slug = 'second-test'
        self.assertEqual(stage.slug, test_slug)

    def test_save_method_to_replace(self):
        stage = Stage.objects.create(stage_name = "Əli")
        self.assertEqual(stage.slug, 'eli')

    def test_str_method(self):
        stage = Stage.objects.create(stage_name = "First Test", slug = "first-test")
        self.assertEqual(str(stage), 'First Test')