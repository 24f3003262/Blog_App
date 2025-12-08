# Blog App using Django

## Mostly made using the Django base templates and functionalities

Following "Django 5 By Example" by Antonio Melé, fully featured Blog application is built. Here is what is implemented:

1. Core Structure & Django 5 Features

• Batteries-Included: Leveraged Django’s vast built-ins to rapidly set up the project structure.
• Admin & ORM: Built a robust administration site and mastered the ORM for database interactions.
• Migrations: Managed database schema changes via Django's migration workflow.
• Django 5 Update: Implemented the new Facet Counts to display item counts in admin filters automatically.

2. Advanced Data Handling & Recommendations

• Optimization: Improved performance using proper database sorting and indexing.
• Tagging: Integrated django-taggit for a robust many-to-many tagging system.
• Recommendation Engine: Built a logic that suggests "Similar Posts" based on shared tags.

3. Content, SEO, and User Experience

• SEO: Engineered canonical URLs and dynamic sitemaps for better search indexing.
• Markdown Support: Integrated Markdown processing for rich-text blog formatting.
• Pagination: Added side pagination to split long post lists and improve load times.

4. Interaction & Security

• Comments: built a full comment system with validation, display logic, and moderation.
• Email: Configured a local SMTP server to send notifications via my email provider.
• Security: Managed sensitive SMTP credentials securely using Environment Variables.

5. DevOps & Database Migration

• Docker & PostgreSQL: Set up a production-grade PostgreSQL database inside a Docker container.
• Migration: Shifted the entire dataset from SQLite3 to PostgreSQL using dumpdata and loaddata commands.

6. The "Soul Connection": Search & NLP

My favorite part—bridging Web Dev and Machine Learning (NLP). I replaced basic filtering with a full-text search engine:
• Search Architecture: Utilized Django’s SearchVector, SearchQuery, and SearchRank.
• Weighted Queries: Prioritized matches in the Title over the Body for better relevance.
• Trigram Similarity: Implemented fuzzy matching to handle user typos effectively.


## Notes to use:-


first make a .env file in the root directory (/Blog_site/.env) containing the following lines of code:-

EMAIL_HOST_USER=email@gmail.com
EMAIL_HOST_PASSWORD=<get your password>
DEFAULT_FROM_EMAIL=My Blog <email@gmail.com>

the email you use will be used as the smtp host...you need to turn on two step verification for that email (must be gmail) and then turn on app password from [here](https://myaccount.google.com/apppasswords)


And then you need to go to Blog_site root directory and open cmd....then type python manage.py migrate. The app will be ready to run


