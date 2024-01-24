from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Examdetails(models.Model):
    _name = "exam.details"
    _description = "Exam informations"
    _order = "date_field asc"
    _rec_name = "name_field"

    name_field = fields.Char(string="Exam name", required=True, size=10)

    date_field = fields.Date(string="Exam Date")

    date_time_field = fields.Datetime(string="Exam Date & Time")

    boolean_field = fields.Boolean(string="Confirm to held the exam(True/False)")

    amount_field = fields.Float(string="Exam helding fee")

    students_number = fields.Integer(
        string="Enter total Number of students who are giving this exam"
    )
    color_widget = fields.Integer(string="Color Picker")

    select_option = fields.Selection(
        string="Select sections for students seating",
        selection=[("a", "A"), ("b", "B")],
    )

    documents_attach = fields.Binary(string="Exam Hall picture")

    exam_desc = fields.Text(string="Held Exam Description")
    term_cond = fields.Text(string="Term and conditions related examination")

    exam_college_address = fields.Html(string="Examination hall address")

    relation_field1 = fields.Many2one(
        "res.partner", string="Many to one Relational field"
    )

    relation_field2 = fields.Many2many(
        "res.partner.category", string="Many to Many Relational field"
    )

    relation_field3 = fields.One2many(
        "student.details", "student_id", string="Assign student for exam"
    )

    state_field = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("in progress", "In Progress"),
            ("done", "Done"),
        ],
        string="State after giving exam",
        required=True,
        default="draft",
    )

    # SQL constrains
    _sql_constraints = [
        (
            "unique_name",
            "unique (name_field)",
            "Exam Name must be unique cannot enter same names",
        ),
        (
            "check_students_number",
            "check(students_number > 0)",
            "Number of students must be positive",
        ),
    ]

    # [Decorator]-python constains
    @api.constrains("name_field", "exam_desc")
    def constraints_name_description(self):
        for record in self:
            if record.name_field == record.exam_desc:
                raise ValidationError(
                    "Exam name and Exam description fields content must be different"
                )

    # buttons state change- [widget statusbar]
    def action_draft(self):
        self.state_field = "draft"

    def action_in_progress(self):
        self.state_field = "in progress"

    def action_done(self):
        self.state_field = "done"

    # for smart button-[student count]
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

    # for smart button-[faculty count]
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
            "domain": [("faculty_id", "=", self.id), ("faculty_count", "=", 1)],
            "view_mode": "tree,form",
            "target": "current",
        }

    # for smart button-[supervisor count]
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

    # for smart button-[subject count]
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
