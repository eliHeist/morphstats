from django.test import SimpleTestCase

from facilitators.forms import FacilitatorTagNameForm


class FacilitatorTagNameFormTests(SimpleTestCase):
    def test_form_uses_tag_names_for_tags_field(self):
        form = FacilitatorTagNameForm()

        self.assertIn('tags', form.fields)
        self.assertTrue(callable(form.fields['tags'].label_from_instance))
