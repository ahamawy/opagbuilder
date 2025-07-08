from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
# Handle Heroku's postgres:// to postgresql:// URL change
database_url = os.getenv('DATABASE_URL', 'sqlite:///opag.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

db = SQLAlchemy(app)

# Import models and services after db initialization
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Agreement, Member, CapitalCommitment, CapitalStructure
from services.document_generator import DocumentGenerator

# Create tables
with app.app_context():
    db.create_all()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})

@app.route('/api/agreements', methods=['GET'])
def get_agreements():
    agreements = Agreement.query.all()
    return jsonify([{
        'id': a.id,
        'company_name': a.company_name,
        'created_at': a.created_at.isoformat(),
        'updated_at': a.updated_at.isoformat()
    } for a in agreements])

@app.route('/api/agreements', methods=['POST'])
def create_agreement():
    data = request.json
    
    agreement = Agreement(
        company_name=data['company_name'],
        state=data.get('state', 'Delaware'),
        formation_date=datetime.fromisoformat(data['formation_date']),
        effective_date=datetime.fromisoformat(data['effective_date']),
        manager_name=data['manager_name'],
        manager_entity=data.get('manager_entity'),
        principal_place_of_business=data.get('principal_place_of_business'),
        registered_agent=data.get('registered_agent'),
        purpose=data.get('purpose'),
        data=data
    )
    
    db.session.add(agreement)
    
    # Add members
    for member_data in data.get('members', []):
        member = Member(
            agreement=agreement,
            name=member_data['name'],
            entity_name=member_data.get('entity_name'),
            member_class=member_data['class'],
            units=member_data.get('units', 0),
            capital_commitment=member_data.get('capital_commitment', 0),
            percentage_interest=member_data.get('percentage_interest', 0)
        )
        db.session.add(member)
    
    db.session.commit()
    
    return jsonify({
        'id': agreement.id,
        'company_name': agreement.company_name,
        'message': 'Agreement created successfully'
    }), 201

@app.route('/api/agreements/<int:agreement_id>', methods=['GET'])
def get_agreement(agreement_id):
    agreement = Agreement.query.get_or_404(agreement_id)
    
    return jsonify({
        'id': agreement.id,
        'company_name': agreement.company_name,
        'state': agreement.state,
        'formation_date': agreement.formation_date.isoformat(),
        'effective_date': agreement.effective_date.isoformat(),
        'manager_name': agreement.manager_name,
        'manager_entity': agreement.manager_entity,
        'data': agreement.data,
        'members': [{
            'id': m.id,
            'name': m.name,
            'entity_name': m.entity_name,
            'class': m.member_class,
            'units': m.units,
            'capital_commitment': m.capital_commitment,
            'percentage_interest': m.percentage_interest
        } for m in agreement.members]
    })

@app.route('/api/agreements/<int:agreement_id>', methods=['PUT'])
def update_agreement(agreement_id):
    agreement = Agreement.query.get_or_404(agreement_id)
    data = request.json
    
    agreement.company_name = data.get('company_name', agreement.company_name)
    agreement.state = data.get('state', agreement.state)
    agreement.manager_name = data.get('manager_name', agreement.manager_name)
    agreement.data = data
    agreement.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({'message': 'Agreement updated successfully'})

@app.route('/api/generate-doc/<int:agreement_id>', methods=['POST'])
def generate_document(agreement_id):
    agreement = Agreement.query.get_or_404(agreement_id)
    template_name = request.json.get('template', 'default')
    
    generator = DocumentGenerator()
    file_path = generator.generate(agreement, template_name)
    
    return send_file(
        file_path,
        as_attachment=True,
        download_name=f"{agreement.company_name}_Operating_Agreement_{datetime.now().strftime('%Y%m%d')}.docx",
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

@app.route('/api/templates', methods=['GET'])
def get_templates():
    templates_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    templates = []
    
    if os.path.exists(templates_dir):
        for file in os.listdir(templates_dir):
            if file.endswith('.docx'):
                templates.append({
                    'name': file.replace('.docx', ''),
                    'filename': file
                })
    
    return jsonify(templates)

if __name__ == '__main__':
    app.run(debug=True, port=5001)