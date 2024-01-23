from odoo import models, fields


class Facultydetails(models.Model):
    _name = "supervisor.details"
    _description = "Exam supervisor related informations"

    supervisor_id = fields.Many2one(
        "exam.details", string="Supervisor Supervising exam details"
    )

    supervisor_name = fields.Char(string="Supervisor Name")

    supervisor_fees = fields.Float(string="Supervisor supervising Fees")

    supervisor_address = fields.Text(string="Supervisor Adress")

    supervisor_present_exam_date = fields.Date(string="Supervisor Supervising Date")

    supervisor_age = fields.Integer(string="Supervisor age")

    supervisor_present_exam_date_time = fields.Datetime(
        string="Supervisor Supervising Date & Time"
    )

    supervisor_gender = fields.Selection(
        string="Supervisor gender",
        selection=[("male", "Male"), ("female", "Female"), ("other", "Other")],
    )

    supervisor_present_on_exam_confirmation = fields.Boolean(
        string="Confirm to be present for supervising(True/False)"
    )

    supervisor_documents_attach = fields.Binary(
        string="Attach Supervisor Identity documents"
    )
