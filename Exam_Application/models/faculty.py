from odoo import models, fields


class Facultydetails(models.Model):
    _name = "faculty.details"
    _description = "Faculty related informations"

    faculty_id = fields.Many2one("exam.details", string="Faculty ID")
    faculty_subject_id = fields.Many2one(
        "subject.details", string="Faculty subject details"
    )

    faculty_name = fields.Char(string="Faculty Name")

    faculty_fees = fields.Float(string="Faculty Fees")

    faculty_address = fields.Text(string="Faculty Adress")

    faculty_subject_no = fields.Integer(string="Faculty subject number")

    faculty_subject_exam_date = fields.Date(string="Only exam Date")

    faculty_subject_exam_date_time = fields.Datetime(string="Exam Date Time")

    faculty_other_subject_name = fields.Selection(
        selection=[
            ("python", "Python"),
            ("xml", "XML"),
            ("javascript", "Javascript"),
            ("sql", "SQL"),
        ]
    )

    faculty_present_on_exam_confirmation = fields.Boolean(
        string="Confirm to be present on exam day(True/False)"
    )

    faculty_documents_attach = fields.Binary(string="Attach Faculty Identity documents")
