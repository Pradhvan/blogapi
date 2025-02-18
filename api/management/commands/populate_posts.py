import random
from django.core.management.base import BaseCommand
from api.models import Post, Author
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = "Populate the Post table with dummy data, including authors"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Number of posts to create")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        posts = []
        authors = []

        # Create a set of authors if needed
        for _ in range(100):  # Number of authors to create (adjust as necessary)
            author = Author.objects.create(name=fake.name(), email=fake.email())
            authors.append(author)

        for _ in range(count):
            post = Post(
                title=fake.sentence(),
                content=fake.paragraph(nb_sentences=5),
                author=random.choice(authors),  # Randomly assign an author
            )
            posts.append(post)

        # Bulk create posts in the database
        Post.objects.bulk_create(posts)
        self.stdout.write(self.style.SUCCESS(f"Successfully added {count} posts!"))
