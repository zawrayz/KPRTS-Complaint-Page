from odoo import models, fields, api

class PublicComplaint(models.Model):
    _name = 'public.complaint'
    _description = 'Public Complaint Record'
    # Use 'name' as the record name, which will be the Complaint ID
    _rec_name = 'name' 

    # Renamed from 'ref' to 'name'
    name = fields.Char(string='Complaint ID', required=True, copy=False, readonly=True,
                             default=lambda self: 'New')
    
    complainant_name = fields.Char('Complainant Name', required=True)
    complainant_contact = fields.Char('Contact/Email', required=True)

    subject = fields.Char('Subject/Title', required=True)
    description = fields.Text('Detailed Complaint Description')
    date_filed = fields.Date('Date Filed', default=fields.Date.today)

    department = fields.Char('Department')
    province = fields.Char('Province')
    district = fields.Char('District')
    tehsil = fields.Char('Tehsil')

    cnic = fields.Char('CNIC')
    gender = fields.Selection([('male','Male'),('female','Female')], string='Gender')
    priority = fields.Selection([('low','Low'),('medium','Medium'),('high','High')], string='Priority')
    attachment = fields.Binary('Attachment')
    attachment_name = fields.Char('Attachment Filename')

    status = fields.Selection([
        ('draft', 'New'),
        ('investigating', 'Under Investigation'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ], default='draft', string='Status', required=True)

    def action_start_investigation(self):
        for record in self:
            record.status = 'investigating'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Check for 'name' instead of 'ref'
            if vals.get('name', 'New') == 'New':
                # Assign the sequence number to the 'name' field
                vals['name'] = self.env['ir.sequence'].next_by_code('public.complaint') or 'New'
        return super().create(vals_list)