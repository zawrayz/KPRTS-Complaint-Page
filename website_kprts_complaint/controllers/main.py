from odoo import http
from odoo.http import request
import base64


class KprtsPublic(http.Controller):

    # ----------------------------
    # Online Complaints Home
    # ----------------------------
    @http.route("/online-complaints", type="http", auth="public", website=True)
    def online_complaints_home(self, **kw):
        return request.render(
            "website_kprts_complaint.kprts_online_complaints_home"
        )

    # ----------------------------
    # New Complaint Form
    # ----------------------------
    @http.route("/online-complaints/new", type="http", auth="public", website=True)
    def new_complaint_form(self, **kw):
        return request.render(
            "website_kprts_complaint.kprts_new_complaint_form"
        )

    # ----------------------------
    # Submit Complaint (SAFE FIXED)
    # ----------------------------
    @http.route(
        "/online-complaints/submit",
        type="http",
        auth="public",
        website=True,
        methods=["POST"],
        csrf=True,
    )
    def submit_complaint(self, **post):

        # 🔐 Basic safety (do NOT crash)
        if not post.get("complainant_name") or not post.get("subject"):
            return request.redirect("/online-complaints/new")

        # 🧩 Combine Department + Service safely
        department_value = ""
        if post.get("department") and post.get("notified_service"):
            department_value = f"{post.get('department')} - {post.get('notified_service')}"
        else:
            department_value = post.get("department") or ""

        # 1️⃣ Create complaint
        complaint = request.env["kprts.complaint"].sudo().create({
            "complainant_name": post.get("complainant_name"),
            "father_name": post.get("father_name"),
            "cnic": post.get("cnic"),
            "mobile": post.get("mobile"),
            "gender": post.get("gender"),
            "province": post.get("province"),
            "district": post.get("district"),
            "department_notified": department_value,
            "first_appeal_filed": post.get("first_appeal_filed"),
            "subject": post.get("subject"),
            "description": post.get("description"),
        })

        # ----------------------------
        # Attachment helper (SAFE)
        # ----------------------------
        def save_attachment(field_name, m2m_field):
            file = request.httprequest.files.get(field_name)
            if file:
                attachment = request.env["ir.attachment"].sudo().create({
                    "name": file.filename,
                    "datas": base64.b64encode(file.read()),
                    "res_model": "kprts.complaint",
                    "res_id": complaint.id,
                })
                complaint[m2m_field] = [(4, attachment.id)]

        # ----------------------------
        # Save attachments correctly
        # ----------------------------
        save_attachment("cnic_front", "cnic_front_attachment_ids")
        save_attachment("cnic_back", "cnic_back_attachment_ids")

        # First appeal attachment ONLY if yes
        if post.get("first_appeal_filed") == "yes":
            save_attachment("first_appeal_copy", "first_appeal_attachment_ids")

        # Supporting documents (multiple allowed)
        files = request.httprequest.files.getlist("supporting_documents")
        for file in files:
            attachment = request.env["ir.attachment"].sudo().create({
                "name": file.filename,
                "datas": base64.b64encode(file.read()),
                "res_model": "kprts.complaint",
                "res_id": complaint.id,
            })
            complaint.supporting_document_ids = [(4, attachment.id)]

        # ----------------------------
        # Redirect to success
        # ----------------------------
        return request.redirect(
            "/online-complaints/success?complaint_number=%s" % complaint.name
        )

    # ----------------------------
    # Complaint Success Page
    # ----------------------------
    @http.route(
        "/online-complaints/success",
        type="http",
        auth="public",
        website=True,
    )
    def complaint_success(self, **kw):
        return request.render(
            "website_kprts_complaint.kprts_complaint_success",
            {
                "complaint_number": kw.get("complaint_number")
            }
        )

    # ----------------------------
    # Track Complaint
    # ----------------------------
    @http.route("/online-complaints/track", type="http", auth="public", website=True)
    def track_complaint(self, **kw):
        return request.render(
            "website_kprts_complaint.kprts_track_complaint_form"
        )
