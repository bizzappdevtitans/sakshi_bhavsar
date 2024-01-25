from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Supervisordetails(models.Model):
    _name = "supervisor.details"
    _description = "Exam supervisor related informations"
    _rec_name = "supervisor_name"

    supervisor_id = fields.Many2one(
        comodel_name="exam.details", string="Supervisor Supervising exam details"
    )

    supervisor_name = fields.Char(string="Supervisor Name")

    supervisor_fees = fields.Float(string="Supervisor supervising Fees")

    supervisor_address = fields.Text(string="Supervisor Adress")

    supervisor_start_exam_date = fields.Date(string="Supervisor Supervising Date")

    supervisor_age = fields.Integer(string="Supervisor age")

    @api.constrains("supervisor_age")
    def constraints_supervisor_age(self):
        for record in self:
            if record.supervisor_age > 50:
                raise ValidationError("Supervisors age must be less than 50")
            elif record.supervisor_age < 25:
                raise ValidationError(
                    "Supervisors age limit is 25 years,Age must be 25 or greater"
                )

    supervisor_end_exam_date_time = fields.Datetime(
        string="Supervisor Supervising Date & Time"
    )

    supervisor_gender = fields.Selection(
        string="Supervisor gender",
        selection=[("male", "Male"), ("female", "Female"), ("other", "Other")],
    )

    supervisor_available_on_exam = fields.Boolean(
        string="Confirm to be present for supervising(True/False)"
    )

    supervisor_documents_attach = fields.Binary(
        string="Attach Supervisor Identity documents"
    )
