from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, backref
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin,RoleMixin
from datetime import datetime,timezone,timedelta
# =================================== kolkata time ==================================================
def kolkata_time():
    return datetime.now(timezone(timedelta(hours=5, minutes=30)))
# ==================================== Model ========================================================
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.role_id'))
)
class Followers(db.Model):
    __tablename__ = 'followers'
    follower_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=kolkata_time())

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(1))
    status = db.Column(db.String(10), default="private")
    pic = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    category = db.Column(db.String(50))
    niche = db.Column(db.String(100))
    followers_count = db.Column(db.Integer, default=0)
    following = db.Column(db.Integer, default=0)
    activity_level = db.Column(db.Integer, default=0)
    flagged = db.Column(db.Boolean, default=False)
    revenue = db.Column(db.Float, default=0.0)
    # Relationships
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete-orphan")
    reports = db.relationship('Report', backref='user', lazy=True, cascade="all, delete-orphan")
    followers = db.relationship(
        'User', secondary='followers',
        primaryjoin=(Followers.followed_id == user_id),
        secondaryjoin=(Followers.follower_id == user_id),
        backref=db.backref('followed', lazy='dynamic'), lazy='dynamic'
    )

    def to_dict(self):
        return {
            'user_id': self.user_id,
            "username": self.username,
            "email": self.email,
            "active": self.active,
            "gender": self.gender,
            "password": self.password,
            "pic": self.pic,
            "niche": self.niche,
            "status": self.status,
            "followers": self.followers_count,
            "following": self.following,
            "activity_level": self.activity_level,
            "flagged": self.flagged,
            "revenue": self.revenue,
            "posts": [post.to_dict() for post in self.posts],
            "roles": [role.name for role in self.roles],
            "notifications" : [notification.to_dict() for notification in self.notifications],
            "complaints": len(self.reports)
        }
    def has_role(self, role):
        return super().has_role(role)
    def get_auth_token(self) -> str | bytes:
        return super().get_auth_token()
class Role(db.Model, RoleMixin):
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))

    def to_dict(self):
        return {"role_id": self.role_id,"name" : self.name}
class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=kolkata_time())
    def to_dict(self):
        return {
                "comment_id": self.comment_id,
                "user_id": self.user_id,
                "post_id": self.post_id,
                "comment": self.comment,
                "likes": self.likes,
                "dislikes": self.dislikes,
                "timestamp": self.timestamp
                }    

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    pic_path = db.Column(db.String(255), nullable=True)  # Path to the picture file
    views = db.Column(db.Integer,default =0)
    description = db.Column(db.String(255), nullable=True)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=kolkata_time())  # Timestamp field
    comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete-orphan")
    def is_added_today(self):
        return self.timestamp.date() == datetime.now(timezone.utc).date()
    def to_dict(self):
        return {
                "user_id": self.user_id,
                "post_id": self.post_id,
                "title": self.title,
                "description":self.description,
                "views" : self.views,
                "likes": self.likes,
                "dislikes": self.dislikes,
                "timestamp": self.timestamp,
                "comments" : self.comments
                }    
    
campaign_category = db.Table('campaign_category',
    db.Column('campaign_id', db.Integer, db.ForeignKey('campaign.campaign_id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.category_id'), primary_key=True)
)

class Campaign(db.Model):
    campaign_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name        = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date  = db.Column(db.Date)
    end_date    = db.Column(db.Date)
    budget      = db.Column(db.Float)
    visibility  = db.Column(db.String(10))  # 'public' or 'private'
    goals = db.Column(db.Text)
    # Relationships
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.sponsor_id', onupdate='CASCADE'), nullable=False)
    sponsor = db.relationship('Sponsor', backref=db.backref('campaigns', lazy=True, cascade="all, delete-orphan"))
    categories = db.relationship('Category', secondary=campaign_category, lazy='subquery',
                                 backref=db.backref('campaigns', lazy=True))
    reports = db.relationship('ReportCamapaign', backref='campaign', lazy=True, cascade="all, delete-orphan")
    flagged = db.Column(db.Boolean, default=False)
    def is_added_today(self):
        return datetime.today().date() == self.start_date
    def is_ongoing(self):
        return datetime.today().date() < self.end_date
    def is_completed_today(self):
        return datetime.today().date() == self.end_date
    def to_dict(self):
        return {
            "campaign_id": self.comment_id,
            "name": self.name,
            "description":self.description,
            "flagged": self.flagged,
            "sponsor": self.sponsor.to_dict(),
            "start_date": self.start_date,
            "end_date": self.end_date,
            "budget": self.budget,
            "visibility":self.visibility,
            "goals": self.goals,
            "categories":[c.to_dict() for c in self.categories],
            "status": "Completed" if self.is_completed_today() else "Ongoing" if self.is_ongoing() else "Started"
            }    

class Sponsor(db.Model):
    sponsor_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False) 
    company_name = db.Column(db.String(100), unique=True)
    contact_person = db.Column(db.String(50))
    industry = db.Column(db.String(100))
    budget = db.Column(db.Float)
 # Foreign key to User
    flagged = db.Column(db.Boolean, default=False)
    is_approved =db.Column(db.Boolean, default=False)  # New field
    user = db.relationship('User', backref=db.backref('sponsor', lazy=True))
    def to_dict(self):
        user = User.query.get(self.user_id)
        return {
            "sponsor_id" : self.sponsor_id,
            'user_id': self.user_id,
            "company_name": self.company_name,
            "email": user.email,
            "contact_person":self.contact_person,
            "active": user.active,
            "gender": user.gender,
            "password": user.password,
            "activity_level": user.activity_level,
            "role": "sponsor",
            "budget" : self.budget,
            "is_approved": self.is_approved,
            "industry": self.industry,
            "campaigns": [c.to_dict() for c in self.campaigns],
            "TotalCampaigns" : len(self.campaigns),
            "TotalCampaignsAddedToday": len([c for c in self.campaigns if c.is_added_today()==True])
        }

class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)
    def to_dict(self):
       return {
                "category_id":self.category_id,
                "name" : self.name,
                "description": self.description
            } 

class AdRequest(db.Model):
    adRequest_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.campaign_id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    requirements = db.Column(db.Text)
    payment_amount = db.Column(db.Float)
    status = db.Column(db.String(20), default='Pending')  # Pending, Accepted, Rejected
    # Relationships
    campaign = db.relationship('Campaign', backref=db.backref('ad_requests', lazy=True, cascade="all, delete-orphan"))
    user = db.relationship('User', backref=db.backref('ad_requests', lazy=True, cascade="all, delete-orphan"))
    
    def to_dict(self):
        return {
                "adRequest_id": self.adRequest_id,
                "campaign_id": self.campaign_id,
                "user_id": self.user_id,
                "requirements":self.requirements,
                "payment_amount":self.payment_amount,
                "status" :self.status,
                "campaign":self.campaign,
                "user": self.user
                }

class Notification(db.Model):
    notification_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=kolkata_time())
    unread = db.Column(db.Boolean, default=True)
    user = db.relationship('User', backref=db.backref('notifications', lazy=True))

    def to_dict(self):
        return {
                "notification_id": self.notification_id,
                "user_id" : self.user_id,
                "message" : self.message,
                "timestamp" : self.timestamp,
                "unread":self.unread
                }

class SponsorUserConversation(db.Model):
    __tablename__ = 'sponsor_user_conversation'
    conversation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.sponsor_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    sender_type = db.Column(db.String(10), nullable=False)  # 'sponsor' or 'user'
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=kolkata_time())
    # Relationships
    sponsor = db.relationship('Sponsor', backref=db.backref('conversations', lazy=True))
    user = db.relationship('User', backref=db.backref('conversations', lazy=True))

    def to_dict(self):
        return  {
                "conversation_id":self.conversation_id,
                "sponsor_id":self.sponsor_id,
                "user_id":self.user_id,
                "message":self.message,
                "sender_type" : self.sender_type,
                "timestamp":self.timestamp
                }
    

class Report(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer,db.ForeignKey('user.user_id'), nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=kolkata_time())
    def __repr__(self):
        return f"Report(id={self.report_id}, reporter_id={self.reporter_id}, content_id={self.post_id})"
class ToxicityScore(db.Model):
    toxic_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  
    post_id = db.Column(db.Integer, nullable=False)  
    toxicity_score = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=kolkata_time())
class ReportCamapaign(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer,db.ForeignKey('user.user_id'), nullable=False)
    campaign_id = db.Column(db.Integer,db.ForeignKey('campaign.campaign_id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=kolkata_time())
    def __repr__(self):
        return f"Report(id={self.report_id}, reporter_id={self.reporter_id}, content_id={self.campaign_id})"
class ToxicityCamapaignScore(db.Model):
    toxic_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'), nullable=False)  
    campaign_id = db.Column(db.Integer,db.ForeignKey('campaign.campaign_id'), nullable=False)
    toxicity_score = db.Column(db.Float,nullable=False)
    timestamp = db.Column(db.DateTime, default=kolkata_time())