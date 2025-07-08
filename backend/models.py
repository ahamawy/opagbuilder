from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON

db = SQLAlchemy()

class Agreement(db.Model):
    __tablename__ = 'agreements'
    
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(50), default='Delaware')
    formation_date = db.Column(db.Date, nullable=False)
    effective_date = db.Column(db.Date, nullable=False)
    manager_name = db.Column(db.String(200))
    manager_entity = db.Column(db.String(200))
    principal_place_of_business = db.Column(db.Text)
    registered_agent = db.Column(db.Text)
    purpose = db.Column(db.Text)
    data = db.Column(JSON)  # Store complete agreement data as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    members = db.relationship('Member', back_populates='agreement', cascade='all, delete-orphan')
    capital_structure = db.relationship('CapitalStructure', back_populates='agreement', uselist=False, cascade='all, delete-orphan')

class Member(db.Model):
    __tablename__ = 'members'
    
    id = db.Column(db.Integer, primary_key=True)
    agreement_id = db.Column(db.Integer, db.ForeignKey('agreements.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    entity_name = db.Column(db.String(200))  # If member is an entity
    member_class = db.Column(db.String(50))  # A, B, C, etc.
    units = db.Column(db.Float, default=0)
    capital_commitment = db.Column(db.Float, default=0)
    percentage_interest = db.Column(db.Float, default=0)
    is_manager = db.Column(db.Boolean, default=False)
    address = db.Column(db.Text)
    email = db.Column(db.String(200))
    
    # Relationships
    agreement = db.relationship('Agreement', back_populates='members')
    capital_commitments = db.relationship('CapitalCommitment', back_populates='member', cascade='all, delete-orphan')

class CapitalCommitment(db.Model):
    __tablename__ = 'capital_commitments'
    
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    paid = db.Column(db.Boolean, default=False)
    paid_date = db.Column(db.Date)
    
    # Relationships
    member = db.relationship('Member', back_populates='capital_commitments')

class CapitalStructure(db.Model):
    __tablename__ = 'capital_structure'
    
    id = db.Column(db.Integer, primary_key=True)
    agreement_id = db.Column(db.Integer, db.ForeignKey('agreements.id'), nullable=False)
    
    # Class A - Anchor Units
    class_a_authorized = db.Column(db.Float, default=0)
    class_a_pre_money_valuation = db.Column(db.Float, default=0)
    class_a_rights = db.Column(db.Text)
    
    # Class B - Investor Units
    class_b_authorized = db.Column(db.Float, default=0)
    class_b_pre_money_valuation = db.Column(db.Float, default=0)
    class_b_rights = db.Column(db.Text)
    
    # Class C - Sweat Equity Units
    class_c_pool_percentage = db.Column(db.Float, default=25)
    class_c_vesting_terms = db.Column(db.Text)
    
    # Waterfall
    carry_percentage = db.Column(db.Float, default=20)
    preferred_return = db.Column(db.Float, default=0)
    
    # Relationships
    agreement = db.relationship('Agreement', back_populates='capital_structure')