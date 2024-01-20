from odoo import models, fields


class Facultydetails(models.Model):
    _name = "supervisor.details"
    _description = "Exam supervisor related informations"

    supervisor_id = fields.Many2one("exam.details", string="Supervisor ID")

    supervisor_name = fields.Char(string="Exam supervisor Name")

    supervisor_fees = fields.Float(string="Supervisor Fees")

    supervisor_address = fields.Text(string="Supervisor Adress")

    total_no_of_supervisor = fields.Integer(string="Total Number of supervisors")

    supervisor_present_exam_date = fields.Date(string="Only exam Date")

    supervisor_present_exam_date_time = fields.Datetime(string="Exam Date Time")

    supervisor_gender = fields.Selection(
        selection=[
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other")
        ]
    )

    supervisor_present_on_exam_confirmation = fields.Boolean(
        string="Confirm to be present on exam day(True/False)"
    )

    supervisor_documents_attach = fields.Binary(
        string="Attach Supervisor Identity documents"
    )
