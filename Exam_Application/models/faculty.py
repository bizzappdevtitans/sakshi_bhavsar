from odoo import models, fields


class Facultydetails(models.Model):
    _name = "faculty.details"
    _description = "Faculty related informations"
    _order = "faculty_fees asc"
    _rec_name = "faculty_name"

    faculty_id = fields.Many2one(
        "exam.details", string="Faculty's subject exam details"
    )
    faculty_subject_id = fields.Many2one(
        "subject.details", string="Faculty's subject details"
    )

    faculty_name = fields.Char(string="Faculty Name")

    faculty_fees = fields.Float(string="Faculty salary")

    faculty_address = fields.Text(string="Faculty Designation")

    faculty_subject_no = fields.Integer(string="Faculty subject code number")

    faculty_subject_exam_date = fields.Date(string="Faculty subject exam Date")

    faculty_subject_exam_date_time = fields.Datetime(
        string="Faculty subject exam Date & Time"
    )

    faculty_gender = fields.Selection(
        string="Faculty gender",
        selection=[
            ("female", "Female"),
            ("male", "Male"),
            ("other", "Other"),
        ],
    )

    faculty_present_on_exam_confirmation = fields.Boolean(
        string="Confirm to be present on the exam day(True/False)"
    )

    faculty_documents_attach = fields.Binary(string="Attach Faculty Identity documents")

    faculty_state_field = fields.Selection(
        selection=[
            ("cancel", "Cancel"),
            ("in progress", "In Progress"),
            ("done", "Done"),
        ],
        string="State of Question paper for exam",
        required=True,
        default="cancel",
    )

    # buttons state change- [widget statusbar]
    def faculty_action_button(self):
        self.faculty_state_field = "cancel"

    def faculty_in_progress_button(self):
        self.faculty_state_field = "in progress"

    def faculty_action_done(self):
        self.faculty_state_field = "done"
