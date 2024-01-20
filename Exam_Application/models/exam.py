from odoo import models, fields, api
from . import student
from . import faculty
from . import supervisor
from . import subject
from odoo.exceptions import ValidationError


class Examdetails(models.Model):
    _name = "exam.details"
    _description = "Exam informations"

    name_field = fields.Char(string="Exam Details", required=True, size=10)

    date_field = fields.Date(string="Only Date")

    date_time_field = fields.Datetime(string="Date Time")

    boolean_field = fields.Boolean(string="(True/False)")
    boolean_rating_field = fields.Boolean(string="Ratings")

    amount_field = fields.Float(string="Amount")

    roll_number = fields.Integer(string="Roll Number")
    color_widget = fields.Integer(string="Color Picker")

    select_option = fields.Selection(selection=[("a", "A"), ("b", "B")])

    documents_attach = fields.Binary(string="Documents")

    exam_desc = fields.Text(string="Exam Description")
    term_cond = fields.Text(string="Term and conditions")

    exam_college_address = fields.Html(string="Examination address")

    relation_field1 = fields.Many2one(
        "res.partner", string="Many to one Relational field"
    )

    relation_field2 = fields.Many2many(
        "res.partner.category", string="Many to Many Relational field"
    )

    relation_field3 = fields.One2many(
        "student.details", "student_id", string="One to Many Relational field"
    )

    state_field = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("in progress", "In Progress"),
            ("done", "Done"),
        ],
        string="StatusBar",
        required=True,
        default="draft",
    )

    _sql_constraints = [
        (
            "unique_name",
            "unique (name_field)",
            "Name must be unique cannot enter same names",
        ),
        (
            "check_roll_number",
            "check(roll_number > 0)",
            "Roll Number should be positive",
        ),
    ]  # SQL Constraints

    @api.constrains("name_field", "exam_desc")  # python constraints
    def constraints_name_description(self):
        for record in self:
            if record.name_field == record.exam_desc:
                raise ValidationError(
                    "Name and Exam description field must be different"
                )

    def action_draft(self):
        self.state_field = "draft"

    def action_in_progress(self):
        self.state_field = "in progress"

    def action_done(self):
        self.state_field = "done"

    # student count
    student_count = fields.Integer(
        string="No of Student Data", compute="count_student_data"
    )

    def count_student_data(self):
        for rec in self:
            student_count = self.env["student.details"].search_count(
                [("student_id", "=", rec.id)]
            )
            rec.student_count = student_count

    def action_count_student(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Student-Exam details",
            "res_model": "student.details",
            "domain": [("student_id", "=", self.id)],
            "view_mode": "tree,form",
            "target": "current",
        }

    # faculty count
    faculty_count = fields.Integer(
        string="No of faculty Data", compute="count_faculty_data"
    )

    def count_faculty_data(self):
        for rec in self:
            faculty_count = self.env["faculty.details"].search_count(
                [("faculty_id", "=", rec.id)]
            )
            rec.faculty_count = faculty_count

    def action_count_faculty(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Faculty-Exam details",
            "res_model": "faculty.details",
            "domain": [("faculty_id", "=", self.id)],
            "view_mode": "tree,form",
            "target": "current",
        }

    # supervisor count
    supervisor_count = fields.Integer(
        string="No of supervisor Data", compute="count_supervisor_data"
    )

    def count_supervisor_data(self):
        for rec in self:
            supervisor_count = self.env["supervisor.details"].search_count(
                [("supervisor_id", "=", rec.id)]
            )
            rec.supervisor_count = supervisor_count

    def action_count_supervisor(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Supervisor-Exam deatils",
            "res_model": "supervisor.details",
            "domain": [("supervisor_id", "=", self.id)],
            "view_mode": "tree,form",
            "target": "current",
        }

    # subject count
    subject_count = fields.Integer(
        string="No of subject Data", compute="count_subject_data"
    )

    def count_subject_data(self):
        for rec in self:
            subject_count = self.env["subject.details"].search_count(
                [("subject_id", "=", self.id)]
            )
            rec.subject_count = subject_count

    def action_count_subject(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Subject-Exam details",
            "res_model": "subject.details",
            "domain": [("subject_id", "=", self.id)],
            "view_mode": "tree,form",
            "target": "current",
        }
