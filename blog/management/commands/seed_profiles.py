from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profiles.models import Profile
from faker import Faker
import random


class Command(BaseCommand):
    help = "Seed the database with mock user profiles"

    def handle(self, *args, **kwargs):
        fake = Faker()

        num_profiles = 9

        profile_pictures = [
            'https://res.cloudinary.com/ddms7cvqu/image/upload/v1731569320/blog_media/profile_pictures/pexels-olenkabohovyk-3646160_uictjl.jpg',
            'https://res.cloudinary.com/ddms7cvqu/image/upload/v1731569320/blog_media/profile_pictures/pexels-olly-762020_nn81v1.jpg',
            'https://res.cloudinary.com/ddms7cvqu/image/upload/v1731569319/blog_media/profile_pictures/pexels-shvetsa-5682847_f8byjn.jpg',
            'https://res.cloudinary.com/ddms7cvqu/image/upload/v1731569318/blog_media/profile_pictures/cesar-rincon-XHVpWcr5grQ-unsplash_ywpp97.jpg',
            'https://res.cloudinary.com/ddms7cvqu/image/upload/v1731569318/blog_media/profile_pictures/masi-mohammadi-FgGVblkZTyA-unsplash_wiqrup.jpg',
            'https://res.cloudinary.com/ddms7cvqu/image/upload/v1731569317/blog_media/profile_pictures/fatane-rahimi-Agv-xPQBO60-unsplash_jor7pb.jpg',
            'https://res.cloudinary.com/ddms7cvqu/image/upload/v1731569317/blog_media/profile_pictures/pexels-vinicius-wiesehofer-289347-1090387_mvfgth.jpg',
            'https://res.cloudinary.com/ddms7cvqu/image/upload/v1731569317/blog_media/profile_pictures/pexels-ono-kosuki-6000065_yzoifg.jpg',
            'https://res.cloudinary.com/ddms7cvqu/image/upload/v1731569317/blog_media/profile_pictures/pexels-dziana-hasanbekava-7275385_d2tnqi.jpg',
            'https://res.cloudinary.com/ddms7cvqu/image/upload/v1731569317/blog_media/profile_pictures/linh-le-gl8rpxObEUE-unsplash_ecs8qz.jpg',
        ]

        cover_pictures = [
            'https://res.cloudinary.com/ddms7cvqu/image/upload/v1731569732/blog_media/cover_pictures/pexels-stywo-1261728_hovkk4.jpg',
            'https://res.cloudinary.com/ddms7cvqu/image/upload/v1731569729/blog_media/cover_pictures/pexels-todd-trapani-488382-1198817_pbxox3.jpg',
            'https://res.cloudinary.com/ddms7cvqu/image/upload/v1731569728/blog_media/cover_pictures/pexels-lucaspezeta-2529375_wsouua.jpg',
            'https://res.cloudinary.com/ddms7cvqu/image/upload/v1731569728/blog_media/cover_pictures/pexels-pixabay-531756_macuvf.jpg',
            'https://res.cloudinary.com/ddms7cvqu/image/upload/v1731569727/blog_media/cover_pictures/pexels-stywo-1054218_urhhje.jpg',
            'https://res.cloudinary.com/ddms7cvqu/image/upload/v1731569727/blog_media/cover_pictures/pexels-iriser-1366957_iuxbnl.jpg',
            'https://res.cloudinary.com/ddms7cvqu/image/upload/v1731569882/blog_media/cover_pictures/daniel-roe-lpjb_UMOyx8-unsplash_wcnh3b.jpg',
            'https://res.cloudinary.com/ddms7cvqu/image/upload/v1731569881/blog_media/cover_pictures/luca-micheli-ruWkmt3nU58-unsplash_ixpde9.jpg',
            'https://res.cloudinary.com/ddms7cvqu/image/upload/v1731569732/blog_media/cover_pictures/pexels-stywo-1261728_hovkk4.jpg',
            'https://res.cloudinary.com/ddms7cvqu/image/upload/v1731570071/blog_media/cover_pictures/samsommer-vddccTqwal8-unsplash_gbxwt7.jpg',
        ]

        for _ in range(num_profiles):
            username = fake.unique.user_name()
            email = fake.unique.email()
            user = User.objects.create_user(
                username=username,
                email=email,
                password='1234'
            )

            profile_picture = random.choice(profile_pictures)
            cover_picture = random.choice(cover_pictures)

            Profile.objects.create(
                user=user,
                bio=fake.sentence(),
                profile_picture=profile_picture,
                cover_picture=cover_picture,
                location=fake.city() + ", " + fake.country(),
                website=fake.url()
            )

            self.stdout.write(self.style.SUCCESS(
                f"Created profile for {user.username}"))

        self.stdout.write(self.style.SUCCESS(
            f"Successfully created {num_profiles} profiles!"))
