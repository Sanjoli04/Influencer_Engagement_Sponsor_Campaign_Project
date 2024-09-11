from application.model import db,User,Role,Category
from flask_security.utils import hash_password
from main import *
import uuid
# ===================================================  INITIALIZATION STARTS HERE =====================================================================
categories = {
    "Fashion": "Focuses on clothing, accessories, footwear, and personal style. This niche often includes trend analysis, outfit inspiration, and fashion news.",
    "Beauty": "Covers skincare, makeup, hair care, and cosmetic products. It often includes tutorials, product reviews, and beauty tips.",
    "Health & Fitness": "Dedicated to physical health, mental well-being, exercise routines, nutrition, and wellness advice.",
    "Travel": "Involves sharing experiences, tips, and guides related to traveling. This niche covers destinations, travel planning, and cultural experiences.",
    "Food & Cooking": "Focuses on recipes, cooking tips, food reviews, and culinary techniques. It often includes content on different cuisines, diet plans, and food culture.",
    "Technology": "Encompasses gadgets, software, apps, and the latest developments in the tech industry. It includes product reviews, tech tutorials, and industry news.",
    "Personal Finance": "Covers financial planning, budgeting, investing, and money management. It often includes tips on saving money, debt reduction, and wealth-building strategies.",
    "Parenting": "Focuses on child-rearing, family life, and parenting advice. This niche often includes tips for managing family dynamics, child development, and educational resources.",
    "Lifestyle": "A broad niche that can cover various aspects of daily life, including hobbies, home decor, DIY projects, and general life advice.",
    "Entertainment": "Covers movies, TV shows, music, celebrity news, and pop culture. It often includes reviews, commentary, and fan discussions.",
    "Education": "Focuses on learning resources, educational content, online courses, and teaching techniques. It often includes tutorials, study tips, and academic advice.",
    "Business & Entrepreneurship": "Dedicated to business strategies, startup advice, leadership, and entrepreneurship. This niche often includes case studies, interviews, and tips for business growth.",
    "Gaming": "Involves video games, board games, eSports, and gaming culture. It often includes game reviews, tutorials, live streaming, and commentary.",
    "Photography": "Covers photography techniques, camera equipment, photo editing, and visual storytelling. It often includes tutorials, gear reviews, and inspiration.",
    "Environment & Sustainability": "Focuses on environmental issues, sustainability practices, eco-friendly products, and conservation efforts.",
    "Art & Design": "Dedicated to visual arts, graphic design, painting, and creative processes. This niche often includes tutorials, inspiration, and artist profiles.",
    "Automotive": "Covers cars, motorcycles, automotive technology, and car culture. It often includes reviews, maintenance tips, and industry news.",
    "Real Estate": "Focuses on property buying, selling, real estate investment, and market trends. It often includes tips for home buyers, sellers, and real estate professionals.",
    "DIY & Crafting": "Involves creating handmade items, DIY projects, and crafts. This niche often includes tutorials, project ideas, and crafting techniques.",
    "Pets": "Dedicated to pet care, training, pet products, and animal behavior. It often includes tips for pet owners, product reviews, and pet health advice."
}

with app.app_context():
    db.create_all()
    # Create roles
    if not Role.query.filter_by(name="admin").first():
        admin_role = datastore.create_role(name="admin", description="I am the admin of the website. I look at stats of the website and manage everything.")
    if not Role.query.filter_by(name="user").first():
        datastore.create_role(name="user", description="I am a user of this website. I like to use this website.")
    if not Role.query.filter_by(name="sponsor").first():
        datastore.create_role(name="sponsor", description="I am a sponsor of this website. I like to make campaigns.")
    db.session.commit()
    
    # Create admin user
    if not User.query.filter_by(email="vashisthsanjoli@gmail.com").first():
        admin_role = Role.query.filter_by(name="admin").first()
        admin = User(
            username="Sanjoli",
            email="vashisthsanjoli@gmail.com",
            password=hash_password("Sa130406"), 
            fs_uniquifier=str(uuid.uuid4()),
            gender='F' # Assign the correct role_id
        )
        datastore.add_role_to_user(admin,admin_role)
        db.session.add(admin)
        db.session.commit()
    if Category.query.all()==[]:
        for i in categories:
            new = Category(name = i,description=categories[i])
            db.session.add(new)
        db.session.commit()