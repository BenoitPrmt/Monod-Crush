from unittest import skip

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from authentication.models import CustomUser
from blog.models.post import Post
from blog.models.postReport import PostReport


def create_user(username: str = "username_test",
                password: str = "password_test",
                date_of_birth: str = "2000-01-01") -> CustomUser:
    return CustomUser.objects.create_user(username=username, password=password, date_of_birth=date_of_birth)


class PostModelTests(TestCase):

    def setUp(self) -> None:
        self.user = create_user()

    def test_create_post(self):
        post = Post.objects.create(text="Test post", author=self.user)
        self.assertEqual(post.text, "Test post")
        self.assertEqual(post.author, self.user)
        self.assertTrue(post.is_anonymous)
        self.assertEqual(post.status, Post.PostStatus.NORMAL)

        self.assertIsNotNone(post.id)
        self.assertIsNotNone(post.created_at)
        self.assertIsNotNone(post.updated_at)

    def test_create_post_with_anonymous_flag(self):
        post1 = Post.objects.create(text="Anonymous post", author=self.user, is_anonymous=True)
        post2 = Post.objects.create(text="Non-anonymous post", author=self.user, is_anonymous=False)

        self.assertTrue(post1.is_anonymous)
        self.assertFalse(post2.is_anonymous)

    def test_short_text(self):
        post = Post.objects.create(text="a" * 50, author=self.user)
        self.assertEqual(post.short_text, "a" * 37 + "...")

    def test_visible_statuses(self):
        post1 = Post.objects.create(text="Visible post", author=self.user, status=Post.PostStatus.NORMAL)
        post2 = Post.objects.create(text="Hidden post", author=self.user, status=Post.PostStatus.HIDDEN)
        post3 = Post.objects.create(text="Awaiting verification post", author=self.user,
                                    status=Post.PostStatus.AWAITING_VERIFICATION)

        self.assertEqual(post1.status, Post.PostStatus.NORMAL)
        self.assertEqual(post2.status, Post.PostStatus.HIDDEN)
        self.assertEqual(post3.status, Post.PostStatus.AWAITING_VERIFICATION)

        visible_posts = Post.objects.filter(status__in=Post.VISIBLE_STATUSES)
        self.assertIn(post1, visible_posts)
        self.assertNotIn(post2, visible_posts)
        self.assertNotIn(post3, visible_posts)

    def test_reset_report(self):
        u1 = create_user("user1")

        post = Post.objects.create(text="Test post", author=self.user)
        PostReport.objects.create(post=post, user=self.user)
        PostReport.objects.create(post=post, user=u1)

        self.assertEqual(post.reports.count(), 2)

        post.reset_report()
        self.assertEqual(post.reports.count(), 0)

    def test_create_post_with_no_text(self):
        with self.assertRaises(ValidationError):
            post = Post.objects.create(text="", author=self.user)
            post.full_clean()

    @skip("Does not work with SQLite")
    def test_create_post_with_too_long_text(self):
        long_text = "A" * 501
        with self.assertRaises(ValidationError):
            post = Post.objects.create(text=long_text, author=self.user)
            post.full_clean()

    def test_create_post_with_no_author(self):
        with self.assertRaises(IntegrityError):
            post = Post(text="Test post")
            post.save()

    def test_create_post_with_no_content(self):
        with self.assertRaises(ValidationError):
            post = Post.objects.create(text="", author=self.user)
            post.full_clean()


class PostIndexViewTests(TestCase):
    def test_no_post(self):
        """
        If no post exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Il n'y pas encore de post soyez le premier à en poster un")
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_post_list(self):
        """
        If posts exist, they are displayed.
        """
        user = create_user()
        p1 = Post.objects.create(author=user, text='test1')
        p2 = Post.objects.create(author=user, text='test2')

        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, p1.text)
        self.assertContains(response, p2.text)
        self.assertNotContains(response, "Il n'y pas encore de post soyez le premier à en poster un")
        self.assertQuerySetEqual(response.context['object_list'], [p1, p2], ordered=False)

    def test_post_list_anonymous(self) -> None:
        """
        If posts exist, they are displayed.
        """

        user1 = create_user("user1")
        Post.objects.create(author=user1, text='test', is_anonymous=False)
        user2 = create_user("user2")
        Post.objects.create(author=user2, text='test')

        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user1.username)
        self.assertNotContains(response, user2.username)

    def test_post_list_hidden(self) -> None:
        """
        If posts exist, they are displayed.
        """

        user = create_user()
        Post.objects.create(author=user, text='test1', status=Post.PostStatus.NORMAL)
        Post.objects.create(author=user, text='test2', status=Post.PostStatus.HIDDEN)
        Post.objects.create(author=user, text='test3', status=Post.PostStatus.AWAITING_VERIFICATION)

        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test1')
        self.assertNotContains(response, 'test2')
        self.assertNotContains(response, 'test3')

    def test_post_list_pagination(self) -> None:
        """
        If posts exist, they are displayed.
        """

        page_size = 15

        user = create_user()
        for i in range(1, page_size * 2 + 1):
            Post.objects.create(author=user, text=f"test{i}!")

        response = self.client.get(reverse('blog:index'))
        self.assertEqual(len(response.context['object_list']), page_size)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"test{page_size * 2}!")
        self.assertContains(response, f"test{page_size + 1}!")

        self.assertNotContains(response, f"test{page_size}!")
        self.assertNotContains(response, "test1!")

        self.assertContains(response, "Suivant")
        self.assertNotContains(response, "Précédent")

        response = self.client.get(reverse('blog:index') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), page_size)

        self.assertContains(response, f"test{page_size}!")
        self.assertContains(response, "test1!")

        self.assertNotContains(response, f"test{page_size + 15}!")
        self.assertNotContains(response, f"test{page_size + 1}!")

        self.assertNotContains(response, "Suivant")
        self.assertContains(response, "Précédent")

    def test_post_list_order(self) -> None:
        """
        If posts exist, they are displayed.
        """

        user = create_user()
        p1 = Post.objects.create(author=user, text='test1')
        p2 = Post.objects.create(author=user, text='test2')
        p3 = Post.objects.create(author=user, text='test3')

        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['object_list'], [p3, p2, p1], ordered=False)
