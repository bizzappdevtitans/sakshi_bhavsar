from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SupervisorDetails(models.Model):
    _name = "supervisor.details"
    _description = "Supervisor related information"
    _rec_name = "supervisor_name"

    supervisor_id = fields.Many2one(
        comodel_name="exam.details",
        string="Supervising Exam details", readonly=True)

    supervisor_sequence_number = fields.Char(
        string="Supervisor sequence",
        required=True,
        readonly=True,
        copy=False,
        default="New Sequence")

    @api.model
    def create(self, vals):
        """
        this will create sequence number
        """
        vals["supervisor_sequence_number"] = self.env["ir.sequence"].next_by_code(
                        "supervisor.details")
        return super(SupervisorDetails, self).create(vals)

    supervisor_name = fields.Char(string="Supervisor Name")

    supervisor_age_search_count = fields.Char(
        string="Total count whose age(40+) :",
        compute="_compute_supervisor_age_search_count",
        readonly=True)

    @api.depends()
    def _compute_supervisor_age_search_count(self):
        """
        this will return total count of supervisor whose age is greater than 40
        """
        for record in self:
            search_count_supervisor_age = self.env["supervisor.details"].search_count(
                [("supervisor_age", ">=", 40)])
            self.supervisor_age_search_count = search_count_supervisor_age

    supervisor_fees = fields.Float(string="Supervising Fees")

    supervisor_start_exam_date = fields.Date(string="Supervising Start Date")

    supervisor_address = fields.Text(string="Supervisor Adress")

    supervisor_age = fields.Integer(string="Supervisor age")

    @api.constrains("supervisor_age")
    def constraints_supervisor_age(self):
        """
        this will give the validation on age where the age must be greater than 25 years
        """
        for record in self:
            if record.supervisor_age > 50:
                raise ValidationError("Supervisors age must be less than 50")
            elif record.supervisor_age < 25:
                raise ValidationError(
                    "Supervisors age limit is 25 years,Age must be 25 or greater")

    supervisor_end_exam_date_time = fields.Datetime(
        string="Supervising end Date & Time")

    supervisor_gender = fields.Selection(
        string="Supervisor gender",
        selection=[("male", "Male"), ("female", "Female"), ("other", "Other")],)

    supervisor_available_on_exam = fields.Boolean(
        string="Confirm for supervising(True/False)")

    supervisor_documents_attach = fields.Binary(
        string="Attach Identity documents")

    @api.depends("supervisor_id")
    def depends_date_method(self):
        """
        this will automatically set the exam date as today date on changing the
        supervisor_id field
        """
        date_today = fields.Date.today()
        if self.supervisor_start_exam_date != date_today:
            self.supervisor_start_exam_date = date_today
            return
            {
                "warning": {
                    "title": "Date will change by method [depends]",
                    "message": "you have changed the supervisor id, now the exam date"
                    "will be automatically changed with todays date.",
                }
            }
