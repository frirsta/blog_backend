import cloudinary.uploader
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from posts.models import Post, Category, Tag
from faker import Faker
import random
import os


class Command(BaseCommand):
    help = "Seed the database with mock travel-related posts and upload images to Cloudinary"

    def handle(self, *args, **kwargs):
        fake = Faker()
        num_posts = 10
        num_categories = 5
        num_tags = 10

        image_dir = os.path.join(os.path.dirname(__file__), "../../../images")

        local_images = [
            os.path.join(image_dir, "travel_1.jpg"),
            os.path.join(image_dir, "travel_2.jpg"),
            os.path.join(image_dir, "travel_3.jpg"),
            os.path.join(image_dir, "travel_4.jpg"),
            os.path.join(image_dir, "travel_5.jpg"),
            os.path.join(image_dir, "travel_6.jpg"),
            os.path.join(image_dir, "travel_7.jpg"),
            os.path.join(image_dir, "travel_8.jpg"),
            os.path.join(image_dir, "travel_9.jpg"),
            os.path.join(image_dir, "travel_10.jpg"),
        ]

        if Category.objects.count() == 0:
            categories = ['Travel', 'Adventure', 'Nature', 'City', 'Culture']
            for name in categories:
                Category.objects.create(name=name)

        if Tag.objects.count() == 0:
            tags = ['Explore', 'Wanderlust',
                    'Photography', 'Vacation', 'Roadtrip']
            for name in tags:
                Tag.objects.create(name=name)

        categories = list(Category.objects.all())
        tags = list(Tag.objects.all())

        users = list(User.objects.all())

        if not users:
            self.stdout.write(self.style.ERROR(
                "No users found. Please seed users first."))
            return

        for _ in range(num_posts):
            user = random.choice(users)
            title = fake.sentence(nb_words=6)
            content = fake.paragraph(nb_sentences=10)
            local_image = random.choice(local_images)
            try:
                upload_result = cloudinary.uploader.upload(
                    local_image, folder="blog_media/posts/")
                image_url = upload_result.get("secure_url")
                post = Post.objects.create(
                    user=user,
                    title=title,
                    content=content,
                    image=image_url
                )

                selected_categories = random.sample(
                    categories, k=min(2, len(categories)))
                selected_tags = random.sample(tags, k=min(3, len(tags)))
                post.category.set(selected_categories)
                post.tags.set(selected_tags)

                self.stdout.write(self.style.SUCCESS(
                    f"Created post '{title}' with image uploaded to Cloudinary"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"Failed to upload image for post '{title}': {str(e)}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully created {
                          num_posts} posts with images uploaded to Cloudinary!"))
