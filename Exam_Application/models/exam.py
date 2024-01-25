from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Examdetails(models.Model):
    _name = "exam.details"
    _description = "Exam Informations"
    _rec_name = "seating_option"

    exam_start_date = fields.Date(string="Exam Starting Date")

    exam_end_date_time = fields.Datetime(string="Exam ending Date & Time")

    exam_confirmation = fields.Boolean(string="Confirm to held the exam(True/False)")

    exam_fees = fields.Float(string="Exam helding fee")

    students_number = fields.Integer(string="Enter total students giving this exam")
    color_widget = fields.Integer(string="Color Picker")

    seating_option = fields.Selection(
        string="Select sections for students seating",
        selection=[("a", "A"), ("b", "B")],
    )

    attach_documents = fields.Binary(string="Exam Hall picture")

    exam_description = fields.Text(string="Held Exam Description")
    term_conditions = fields.Text(string="Term and conditions related examination")

    exam_college_address = fields.Html(string="Examination hall address")

    select_names_options = fields.Many2one(
        comodel_name="res.partner", string="Many to one Relational field"
    )

    select_categories_options = fields.Many2many(
        comodel_name="res.partner.category", string="Many to Many Relational field"
    )

    assign_students_exam = fields.One2many(
        comodel_name="student.details",
        inverse_name="student_id",
        string="Assign student for exam",
    )

    states = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
        ],
        string="State after giving exam",
        required=True,
        default="in_progress",
    )

    # SQL constrains
    _sql_constraints = [
        (
            "unique_exam_description",
            "unique (exam_description)",
            "Exam description must be unique cannot enter same ",
        ),
        (
            "check_students_number",
            "check(students_number > 0)",
            "Number of students must be positive",
        ),
    ]

    # [Decorator]-python constains
    @api.constrains("exam_college_address", "exam_description")
    def constraints_college_name_description(self):
        for record in self:
            if record.exam_college_address == record.exam_description:
                raise ValidationError(
                    "Exam address and Exam description fields content must be different"
                )

    # buttons state change- [widget statusbar]
    def action_draft(self):
        self.write({"states": "draft"})

    def action_in_progress(self):
        self.write({"states": "in_progress"})

    def action_done(self):
        self.write({"states": "done"})

    # for smart button-[student count]
    student_count = fields.Integer(
        string="Total Students", compute="count_student_data"
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
            "name": "Students",
            "res_model": "student.details",
            "domain": [
                "|",
                ("student_id", "in", [self.id]),
                "|",
                ("student_count", "=", 1),
                ("student_count", ">", 1),
            ],
            "view_mode": "form,tree",
            "target": "new",
        }

    # for smart button-[supervisor count]
    supervisor_count = fields.Integer(
        string="Total Supervisors", compute="count_supervisor_data"
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
            "name": "Supervisors",
            "res_model": "supervisor.details",
            "domain": [("supervisor_id", "=", self.id)],
            "view_mode": "tree,form",
            "target": "new",
        }
