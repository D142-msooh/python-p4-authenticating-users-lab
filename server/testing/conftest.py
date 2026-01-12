#!/usr/bin/env python3

import pytest
from app import app
from models import db, User

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))

@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        
        # Create a test user
        user = User(username='testuser')
        db.session.add(user)
        db.session.commit()
        
        yield app.test_client()
        
        db.session.remove()
        db.drop_all()