from django.core.exceptions import ValidationError
from django.test import TestCase

from projectshop.main.models import Profile, AppUser


class ProfileTests(TestCase):
    VALID_PROFILE_DATA = {
            'first_name': 'Test',
            'last_name': 'Tested',
            'user_id': 1,
            'gender': 'Male',
    }

    VALID_USER_DATA = {
        'email': 'aqwer@abv.bg',
        'password': 'helloWorld242',
        'id': 1
    }

    def test_profile_create__when_first_name_contains_only_letters__expect_success(self):
        user = AppUser(**self.VALID_USER_DATA)
        user.save()
        profile = Profile(**self.VALID_PROFILE_DATA)
        profile.save()

    def test_profile_create__when_first_and_last_name_contains_only_letters__expect_success(self):
        user = AppUser(**self.VALID_USER_DATA)
        user.save()
        profile = Profile(**self.VALID_PROFILE_DATA)
        profile.save()

    def test_profile_create__when_last_name_contains_only_letters__expect_success(self):
        user = AppUser(**self.VALID_USER_DATA)
        user.save()
        profile = Profile(**self.VALID_PROFILE_DATA)
        profile.save()

    def test_profile_create__when_first_name_contains_a_digit__expect_fail(self):
        user = AppUser(**self.VALID_USER_DATA)
        user.save()

        first_name = 'Test1'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            user_id=self.VALID_PROFILE_DATA['user_id'],
            gender=self.VALID_PROFILE_DATA['gender'],
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_dollar__expect_fail(self):
        user = AppUser(**self.VALID_USER_DATA)
        user.save()

        first_name = 'Test$'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            user_id=self.VALID_PROFILE_DATA['user_id'],
            gender=self.VALID_PROFILE_DATA['gender'],
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_space__expect_fail(self):
        user = AppUser(**self.VALID_USER_DATA)
        user.save()

        first_name = 'Test ddd'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            user_id=self.VALID_PROFILE_DATA['user_id'],
            gender=self.VALID_PROFILE_DATA['gender'],
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)