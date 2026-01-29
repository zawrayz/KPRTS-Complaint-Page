# my_complaints_app/__manifest__.py
{
    'name': "Complaint Management System",
    'version': '1.0',
    'depends': ['base'],
    'category': 'Services',
    'data': [
        'security/ir.model.access.csv',
        'data/complaint_sequence.xml',  # New File for Unique ID
        'views/complaint_views.xml',
    ],
    'installable': True,
    'application': True,
}