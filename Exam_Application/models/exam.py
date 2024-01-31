from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Examdetails(models.Model):
    _name = "exam.details"
    _description = "Exam Informations"
    _rec_name = "seating_option"

    exam_sequence_number = fields.Char(
        string="Exam sequence",
        required=True,
        readonly=True,
        copy=False,
        default="New Sequence",
    )

    # sequence number generate using create() (orm method) and api.model(decorator)
    @api.model
    def create(self, vals):
        vals["exam_sequence_number"] = self.env["ir.sequence"].next_by_code(
            "exam.details"
        )
        return super(Examdetails, self).create(vals)

    exam_name = fields.Char(string="Enter exam name")

    exam_start_date = fields.Date(string="Exam Starting Date")

    exam_end_date_time = fields.Datetime(string="Exam ending Date & Time")

    exam_confirmation = fields.Boolean(string="Confirm to held the exam(True/False)")

    exam_fees = fields.Float(string="Exam helding fee")

    students_number = fields.Integer(string="Enter total students giving this exam")
    color_widget = fields.Integer(string="Color Picker")

    seating_option = fields.Selection(
        string="Select sections for seating",
        selection=[
            ("a", "A"),
            ("b", "B"),
            ("c", "C"),
            ("d", "D"),
            ("e", "E"),
            ("f", "F"),
            ("g", "G"),
        ],
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

    assign_supervisors_exam = fields.One2many(
        comodel_name="supervisor.details",
        inverse_name="supervisor_id",
        string="Assign supervisor for exam",
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
    @api.constrains("term_conditions", "exam_description")
    def constraints_college_name_description(self):
        for record in self:
            if record.term_conditions == record.exam_description:
                raise ValidationError(
                    "term conditions box and Exam description fields content must be different"
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
        if self.student_count == 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Students",
                "res_model": "student.details",
                "view_type": "form",
                "view_mode": "form",
                "res_id": self.assign_students_exam.id,
                "domain": [("student_id", "=", self.id)],
                "target": "new",
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "name": "Students",
                "res_model": "student.details",
                "view_mode": "tree,form",
                "domain": [("student_id", "=", self.id)],
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
        if self.supervisor_count == 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Supervisors",
                "res_model": "supervisor.details",
                "view_type": "form",
                "view_mode": "form",
                "res_id": self.assign_supervisors_exam.id,
                "domain": [("supervisor_id", "=", self.id)],
                "target": "new",
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "name": "Supervisors",
                "res_model": "supervisor.details",
                "view_mode": "tree,form",
                "domain": [("supervisor_id", "=", self.id)],
                "target": "new",
            }
