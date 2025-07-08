# Operating Agreement Builder

A web application for creating and managing LLC operating agreements with an easy-to-use interface and professional Word document export.

## Features

- **Dynamic Form Interface**: Step-by-step wizard for entering agreement details
- **Member Management**: Add unlimited members with different classes (Anchor, Investor, Sweat Equity)
- **Capital Structure**: Define capital commitments and ownership percentages
- **Governance Settings**: Configure board seats and reserved matters
- **Word Document Export**: Generate professionally formatted .docx files
- **Template System**: Use custom Word templates for document generation
- **Data Persistence**: Save and edit agreements

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ahamawy/opagbuilder.git
cd opagbuilder
```

2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd ../frontend
npm install
```

### Running the Application

1. Start the backend server:
```bash
cd backend
python app.py
```
The backend will run on http://localhost:5001

2. In a new terminal, start the frontend:
```bash
cd frontend
npm start
```
The frontend will open at http://localhost:3000

## Usage

1. **Create New Agreement**: Click "New Agreement" on the home page
2. **Fill in Details**: Complete the multi-step form:
   - Company Information
   - Management Structure
   - Members & Capital
   - Governance
   - Financial Terms
3. **Save Agreement**: Click "Save Agreement" to store in database
4. **Generate Document**: From the agreement view, click "Generate Document" to export as Word

## Template Customization

To use your ETFIG TWO template:

1. Copy your template to `backend/templates/`
2. Rename it (e.g., `etfig_two.docx`)
3. The template will appear in the dropdown when generating documents

For best results, the template should include placeholders that match the app's field names.

## Project Structure

```
opagbuilder/
├── frontend/              # React TypeScript app
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API services
│   │   └── types/       # TypeScript types
│   └── package.json
├── backend/              # Python Flask API
│   ├── app.py           # Main application
│   ├── models.py        # Database models
│   ├── services/        # Business logic
│   └── templates/       # Word document templates
└── README.md
```

## API Endpoints

- `GET /api/agreements` - List all agreements
- `POST /api/agreements` - Create new agreement
- `GET /api/agreements/:id` - Get agreement details
- `PUT /api/agreements/:id` - Update agreement
- `POST /api/generate-doc/:id` - Generate Word document
- `GET /api/templates` - List available templates

## Development

### Adding New Fields

1. Update the TypeScript interface in `frontend/src/types/Agreement.ts`
2. Add form fields in `frontend/src/pages/AgreementForm.tsx`
3. Update the database model in `backend/models.py`
4. Modify document generation in `backend/services/document_generator.py`

### Custom Templates

Templates use the python-docx-template syntax:
- `{{ variable_name }}` for simple replacements
- `{% for item in list %}...{% endfor %}` for loops
- Rich text formatting is preserved from the template

## Troubleshooting

- **CORS errors**: Ensure backend is running on port 5001
- **Module not found**: Check all dependencies are installed
- **Template not found**: Place .docx files in `backend/templates/`
- **Database errors**: Delete `opag.db` and restart to recreate

## License

This project is for demonstration purposes.