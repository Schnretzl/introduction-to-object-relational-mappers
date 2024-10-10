# Task 1: Setting Up Flask with Flask-SQLAlchemy

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, validate
from marshmallow import ValidationError
from my_password import my_password

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{my_password}@localhost/fitness_center_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    name = fields.String(required=True)
    age = fields.Integer(required=True, validate=validate.Range(min=18, max=99))
    
    class Meta:
        fields = ('name', 'age', 'id')

class WorkoutSessionSchema(ma.Schema):
    member_id = fields.Integer(required=True)
    session_date = fields.Date()
    session_time = fields.String()
    activity = fields.String()
    duration_minutes = fields.Integer()
    calories_burned = fields.Integer()
    
    class Meta:
        fields = ('member_id', 'session_date', 'session_time', 'activity', 'duration_minutes', 'calories_burned', 'id')
        
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True)

class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    
class WorkoutSession(db.Model):
    __tablename__ = 'workout_sessions'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'))
    session_date = db.Column(db.Date)
    session_time = db.Column(db.String(10))
    activity = db.Column(db.String(50))
    duration_minutes = db.Column(db.Integer)
    calories_burned = db.Column(db.Integer)
    members = db.relationship('Member', backref='workout_sessions')
    
with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
    app.run(debug=True)
    
# Task 2: Implementing CRUD Operations for Members Using ORM

@app.route('/members', methods=['GET'])
def get_members():
    all_members = Member.query.all()
    return members_schema.jsonify(all_members)

@app.route('/members/<id>', methods=['GET'])
def get_member(id):
    member = Member.query.get(id)
    return member_schema.jsonify(member)

@app.route('/members', methods=['POST'])
def add_member():
    name = request.json['name']
    age = request.json['age']
    
    new_member = Member(name=name, age=age)
    db.session.add(new_member)
    db.session.commit()
    
    return jsonify({'message': 'Member added successfully'}), 201

@app.route('/members/<id>', methods=['PUT'])
def update_member(id):
    member = Member.query.get(id)
    
    name = request.json['name']
    age = request.json['age']
    
    member.name = name
    member.age = age
    
    db.session.commit()
    
    return jsonify({'message': 'Member updated successfully'}), 200

@app.route('/members/<id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get(id)
    
    db.session.delete(member)
    db.session.commit()
    
    return jsonify({'message': 'Member deleted successfully'}), 200

# Task 3: Managing Workout Sessions with ORM

@app.route('/workout_sessions', methods=['GET'])
def get_workout_sessions():
    all_workout_sessions = WorkoutSession.query.all()
    return workout_sessions_schema.jsonify(all_workout_sessions)

@app.route('/workout_sessions/<id>', methods=['GET'])
def get_workout_sessions_for_member(id):
    workout_sessions = WorkoutSession.query.filter_by(member_id=id).all()
    return workout_sessions_schema.jsonify(workout_sessions)

@app.route('/workout_sessions', methods=['POST'])
def schedule_workout_session():
    member_id = request.json['member_id']
    session_date = request.json['session_date']
    session_time = request.json['session_time']
    activity = request.json['activity']
    duration_minutes = request.json['duration_minutes']
    calories_burned = request.json['calories_burned']
    
    new_workout_session = WorkoutSession(member_id=member_id, session_date=session_date, session_time=session_time, activity=activity, duration_minutes=duration_minutes, calories_burned=calories_burned)
    db.session.add(new_workout_session)
    db.session.commit()
    
    return jsonify({'message': 'Workout session scheduled successfully'}), 201

@app.route('/workout_sessions/<id>', methods=['PUT'])
def update_workout_session(id):
    workout_session = WorkoutSession.query.get(id)
    
    member_id = request.json['member_id']
    session_date = request.json['session_date']
    session_time = request.json['session_time']
    activity = request.json['activity']
    duration_minutes = request.json['duration_minutes']
    calories_burned = request.json['calories_burned']
    
    workout_session.member_id = member_id
    workout_session.session_date = session_date
    workout_session.session_time = session_time
    workout_session.activity = activity
    workout_session.duration_minutes = duration_minutes
    workout_session.calories_burned = calories_burned
    
    db.session.commit()
    
    return jsonify({'message': 'Workout session updated successfully'}), 200