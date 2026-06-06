from datetime import datetime
from app import db
from enum import Enum

class UserRole(Enum):
    """User roles in the system"""
    GENERAL_USER = "general_user"
    CENTER_ADMIN = "center_admin"
    MASTER_ADMIN = "master_admin"

class User(db.Model):
    """User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(256), unique=True, nullable=False, index=True)
    email = db.Column(db.String(256), unique=True, nullable=False, index=True)
    name = db.Column(db.String(256), nullable=False)
    profile_picture = db.Column(db.String(512))
    role = db.Column(db.String(50), default=UserRole.GENERAL_USER.value)
    
    # Location data
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    address = db.Column(db.String(512))
    
    # Relationships
    books = db.relationship('Book', backref='owner', lazy='dynamic', foreign_keys='Book.owner_id')
    center_admin_for = db.relationship('LocalCenter', backref='admin', lazy='dynamic')
    book_requests = db.relationship('BookRequest', backref='borrower', lazy='dynamic', foreign_keys='BookRequest.borrower_id')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'profile_picture': self.profile_picture,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
        }


class LocalCenter(db.Model):
    """Local center where books are exchanged"""
    __tablename__ = 'local_centers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(512), nullable=False)
    city = db.Column(db.String(128), nullable=False, index=True)
    state = db.Column(db.String(128))
    postal_code = db.Column(db.String(10))
    
    # Location for proximity search
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    # Admin relationship
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Contact
    phone = db.Column(db.String(20))
    email = db.Column(db.String(256))
    
    # Operating hours (store as JSON or separate fields)
    operating_hours = db.Column(db.String(256))
    
    # Relationships
    book_requests = db.relationship('BookRequest', backref='center', lazy='dynamic')
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<LocalCenter {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'phone': self.phone,
            'email': self.email,
            'operating_hours': self.operating_hours,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
        }


class BookStatus(Enum):
    """Book status states"""
    AVAILABLE = "available"
    REQUESTED = "requested"
    AT_CENTER = "at_center"
    BORROWED = "borrowed"
    RETURNED = "returned"


class Book(db.Model):
    """Book model"""
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    title = db.Column(db.String(256), nullable=False)
    author = db.Column(db.String(256), nullable=False)
    genre = db.Column(db.String(128))
    language = db.Column(db.String(128), default='English')
    isbn = db.Column(db.String(20))
    description = db.Column(db.Text)
    
    # Condition: Excellent, Good, Fair, Poor
    condition = db.Column(db.String(50), default='Good')
    
    # Status
    status = db.Column(db.String(50), default=BookStatus.AVAILABLE.value)
    
    # Location info (stored at book level for faster queries)
    nearest_center_id = db.Column(db.Integer, db.ForeignKey('local_centers.id'))
    nearest_center = db.relationship('LocalCenter', lazy='joined')
    
    # Cover image
    cover_image = db.Column(db.String(512))
    
    # Relationships
    requests = db.relationship('BookRequest', backref='book', lazy='dynamic', cascade='all, delete-orphan')
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Book {self.title}>'
    
    def to_dict(self, include_owner=True):
        data = {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'language': self.language,
            'isbn': self.isbn,
            'description': self.description,
            'condition': self.condition,
            'status': self.status,
            'cover_image': self.cover_image,
            'nearest_center': self.nearest_center.to_dict() if self.nearest_center else None,
            'created_at': self.created_at.isoformat(),
        }
        if include_owner:
            data['owner'] = self.owner.to_dict()
        return data


class RequestStatus(Enum):
    """Book request status states"""
    PENDING = "pending"  # Awaiting lender confirmation
    CONFIRMED = "confirmed"  # Lender confirmed, awaiting drop-off
    AWAITING_DROPOFF = "awaiting_dropoff"  # Ready for lender to drop off
    AT_CENTER = "at_center"  # At center, ready for pickup
    READY_FOR_PICKUP = "ready_for_pickup"  # Confirmed at center
    BORROWED = "borrowed"  # Handed over to borrower
    RETURNED = "returned"  # Returned to center
    COMPLETED = "completed"  # Fully completed
    CANCELLED = "cancelled"  # Request cancelled


class BookRequest(db.Model):
    """Book request model - tracks the handover workflow"""
    __tablename__ = 'book_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    borrower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    center_id = db.Column(db.Integer, db.ForeignKey('local_centers.id'), nullable=False)
    
    # Status tracking
    status = db.Column(db.String(50), default=RequestStatus.PENDING.value)
    
    # Dates
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    lender_confirmed_at = db.Column(db.DateTime)
    dropped_off_at = db.Column(db.DateTime)
    center_confirmed_at = db.Column(db.DateTime)
    handed_over_at = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)  # When book needs to be returned
    returned_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Borrowing period (in days)
    borrowing_period_days = db.Column(db.Integer, default=14)
    
    # Notes
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<BookRequest book_id={self.book_id} borrower_id={self.borrower_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'book': self.book.to_dict(),
            'borrower': self.borrower.to_dict(),
            'center': self.center.to_dict(),
            'status': self.status,
            'requested_at': self.requested_at.isoformat(),
            'lender_confirmed_at': self.lender_confirmed_at.isoformat() if self.lender_confirmed_at else None,
            'dropped_off_at': self.dropped_off_at.isoformat() if self.dropped_off_at else None,
            'center_confirmed_at': self.center_confirmed_at.isoformat() if self.center_confirmed_at else None,
            'handed_over_at': self.handed_over_at.isoformat() if self.handed_over_at else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'returned_at': self.returned_at.isoformat() if self.returned_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'borrowing_period_days': self.borrowing_period_days,
            'notes': self.notes,
        }
