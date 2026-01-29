from odoo import models, fields, api
from datetime import timedelta


class KprtsComplaint(models.Model):
    _name = "kprts.complaint"
    _description = "KPRTS Complaint"
    _order = "create_date desc"

    name = fields.Char(
        string="Complaint Number",
        required=True,
        readonly=True,
        copy=False,
        default="New",
    )

    # ----------------------------
    # PERSONAL INFO
    # ----------------------------
    complainant_name = fields.Char(string="Full Name", required=True)
    father_name = fields.Char(string="Father / Husband Name")

    id_type = fields.Selection(
        [
            ("cnic", "CNIC"),
            ("passport", "Passport"),
        ],
        string="ID Type",
        default="cnic",
        required=True,
    )

    cnic = fields.Char(string="CNIC Number")
    cnic_expiry_date = fields.Date(string="CNIC Expiry Date")
    passport_number = fields.Char(string="Passport Number")

    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
        ],
        string="Gender",
    )

    mobile = fields.Char(string="Mobile Number")
    email = fields.Char(string="Email")
    address = fields.Text(string="Residential Address")

    # ----------------------------
    # LOCATION & SERVICE INFO
    # ----------------------------
    province = fields.Selection(
        [
            ("punjab", "Punjab"),
            ("sindh", "Sindh"),
            ("kpk", "Khyber Pakhtunkhwa"),
            ("balochistan", "Balochistan"),
            ("gilgit", "Gilgit Baltistan"),
            ("ajk", "AJK"),
        ],
        string="Province",
    )

    district = fields.Selection(
        [
            ("lahore", "Lahore"),
            ("rawalpindi", "Rawalpindi"),
            ("karachi", "Karachi"),
            ("peshawar", "Peshawar"),
        ],
        string="District",
    )

    postal_code = fields.Char(string="Postal Code")
    department_notified = fields.Char(string="Department / Notified Service")

    complaint_category = fields.Selection(
        [
            ("service_delay", "Service Delay"),
            ("misconduct", "Misconduct"),
            ("corruption", "Corruption"),
            ("other", "Other"),
        ],
        string="Complaint Category",
    )

    # ----------------------------
    # COMPLAINT INFO
    # ----------------------------
    subject = fields.Char(string="Subject", required=True)
    description = fields.Text(string="Complaint Description", required=True)

    first_appeal_filed = fields.Selection(
        [
            ("yes", "Yes"),
            ("no", "No"),
        ],
        string="First Appeal Filed",
    )

    first_appeal_details = fields.Text(string="First Appeal Details")

    state = fields.Selection(
        [
            ("new", "New"),
            ("in_progress", "In Progress"),
            ("disposed", "Disposed"),
            ("rejected", "Rejected"),
        ],
        string="Status",
        default="new",
        required=True,
    )

    # ----------------------------
    # DISPOSAL TIMESTAMP
    # ----------------------------
    disposed_date = fields.Datetime(
        string="Disposed Date",
        readonly=True,
        copy=False,
    )

    # ----------------------------
    # ATTACHMENTS
    # ----------------------------
    cnic_front_attachment_ids = fields.Many2many(
        "ir.attachment",
        "kprts_cnic_front_rel",
        "complaint_id",
        "attachment_id",
        string="CNIC Front",
    )

    cnic_back_attachment_ids = fields.Many2many(
        "ir.attachment",
        "kprts_cnic_back_rel",
        "complaint_id",
        "attachment_id",
        string="CNIC Back",
    )

    first_appeal_attachment_ids = fields.Many2many(
        "ir.attachment",
        "kprts_first_appeal_rel",
        "complaint_id",
        "attachment_id",
        string="First Appeal Document",
    )

    supporting_document_ids = fields.Many2many(
        "ir.attachment",
        "kprts_supporting_docs_rel",
        "complaint_id",
        "attachment_id",
        string="Supporting Documents",
    )

    # ----------------------------
    # SEQUENCE
    # ----------------------------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("kprts.complaint")
                    or "New"
                )
        return super().create(vals_list)

    # ----------------------------
    # DASHBOARD KPIs (SAFE EXTENDED)
    # ----------------------------
    def get_dashboard_stats(self):
        total = self.search_count([])
        disposed = self.search_count([("state", "=", "disposed")])

        within_60 = self.search_count([
            ("state", "=", "disposed"),
            ("disposed_date", ">=", fields.Datetime.now() - timedelta(days=60)),
        ])

        beyond_60 = disposed - within_60

        # ✅ GENDER AGGREGATION (SAFE)
        male = self.search_count([("gender", "=", "male")])
        female = self.search_count([("gender", "=", "female")])
        other = self.search_count([("gender", "=", "other")])

        return {
            "total": total,
            "open": self.search_count([("state", "=", "new")]),
            "progress": self.search_count([("state", "=", "in_progress")]),
            "disposed": disposed,
            "disposed_within_60": within_60,
            "disposed_beyond_60": beyond_60,

            # 👇 NEW (for gender pie)
            "gender_male": male,
            "gender_female": female,
            "gender_other": other,
        }

    # ----------------------------
    # FORM BUTTON ACTIONS
    # ----------------------------
    def action_mark_in_progress(self):
        for rec in self:
            rec.state = "in_progress"

    def action_mark_disposed(self):
        for rec in self:
            rec.state = "disposed"
            if not rec.disposed_date:
                rec.disposed_date = fields.Datetime.now()

    def action_mark_rejected(self):
        for rec in self:
            rec.state = "rejected"

    def action_reset_new(self):
        for rec in self:
            rec.state = "new"
            rec.disposed_date = False
