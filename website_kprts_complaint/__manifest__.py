{
    "name": "Website KPRTS Complaint Form",
    "version": "19.0.1.0.0",
    "category": "Website",
    "summary": "KPRTS-style public complaints frontend",
    "depends": ["base", "web", "website"],

    "data": [
        "security/ir.model.access.csv",
        "data/sequence.xml",

        "views/complaint_views.xml",
        "views/complaint_search_view.xml",
        "views/complaint_action.xml",

        # ⚠️ MUST be before assets execution
        "views/website_templates.xml",

        "views/kprts_dashboard_action.xml",
        "views/backend_menu.xml",
    ],

    "assets": {
       "web.assets_frontend": [
     "website_kprts_complaint/static/src/js/province_district.js",
],


        "web.assets_backend": [
            "website_kprts_complaint/static/src/xml/kprts_dashboard.xml",
            "website_kprts_complaint/static/src/js/kprts_dashboard.js",
            "website_kprts_complaint/static/src/css/kprts_dashboard.css",
        ],
    },

    "application": True,
    "license": "LGPL-3",
}
