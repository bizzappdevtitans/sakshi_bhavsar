from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Supervisordetails(models.Model):
    _name = "supervisor.details"
    _description = "Exam supervisor related informations"
    _rec_name = "supervisor_name"
    _inherit = "exam.details"

    supervisor_id = fields.Many2one(
        comodel_name="exam.details",
        string="Supervisor Supervising exam details")

    supervisor_sequence_number = fields.Char(
        string="Supervisor sequence",
        required=True,
        readonly=True,
        copy=False,
        default="New Sequence")

    # ----------------------
    # sequence number generate
    # ----------------------
    @api.model
    def create(self, vals):
        vals["supervisor_sequence_number"] = self.env["ir.sequence"].next_by_code(
                        "supervisor.details")
        return super(Supervisordetails, self).create(vals)

    # ------------------
    # create()-orm method
    # ------------------
    supervisor_name = fields.Char(string="Supervisor Name")
    # @api.model
    """def create(self, vals):
        res = super(Supervisordetails, self).create(vals)
        if vals.get("supervisor_gender") == "male":
            res["supervisor_name"] = "Mr. " + res["supervisor_name"]
        elif vals.get("supervisor_gender") == "female":
            res["supervisor_name"] = "Miss. " + res["supervisor_name"]
        else:
            return res
        return res"""

    # -------------
    # search_count()-orm method
    # -------------
    supervisor_age_search_count = fields.Char(
        string="Supervisors count whose age(more than 40) :",
        compute="action_supervisor_age_search_count",
        readonly=True,
    )

    @api.depends()
    def action_supervisor_age_search_count(self):
        for record in self:
            search_count_supervisor_age = self.env["supervisor.details"].search_count(
                [("supervisor_age", ">=", 40)]
            )
            self.supervisor_age_search_count = search_count_supervisor_age


    supervisor_fees = fields.Float(string="Supervisor supervising Fees")

    supervisor_start_exam_date = fields.Date(string="Supervising Starting Date")

    supervisor_address = fields.Text(string="Supervisor Adress")

    supervisor_age = fields.Integer(string="Supervisor age")

    # ---------------------
    # constraints()- Decorator
    # ---------------------
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
        string="Supervising ending Date & Time")

    supervisor_gender = fields.Selection(
        string="Supervisor gender",
        selection=[("male", "Male"), ("female", "Female"), ("other", "Other")],)

    supervisor_available_on_exam = fields.Boolean(
        string="Confirm to be present for supervising(True/False)")

    supervisor_documents_attach = fields.Binary(
        string="Attach Supervisor Identity documents")

    # -------------------
    # depends()- Decorator
    # -------------------
    @api.depends("supervisor_id")
    def depends_date_method(self):
        date_today = fields.Date.today()
        if self.supervisor_start_exam_date != date_today:
            self.supervisor_start_exam_date = date_today
            return
            {
                "warning": {
                    "title": "Date will change ny method depends",
                    "message": "you have changed the supervisor id, now the exam date"
                    "will be automatically changed with todays date.",
                }
            }
