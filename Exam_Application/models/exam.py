from odoo import models, fields


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

    product_desc = fields.Text(string="Exam Description")

    term_cond = fields.Text(string="Term and conditions")

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

    def action_draft(self):
        self.state_field = "draft"

    def action_in_progress(self):
        self.state_field = "in progress"

    def action_done(self):
        self.state_field = "done"

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


class Studentdetails(models.Model):
    _name = "student.details"
    _description = "Student related informations"

    student_id = fields.Many2one("exam.details", string="Student ID")
    student_name = fields.Char(string="Student Name")
    student_fees = fields.Float(string="Student Fees")
    student_subject = fields.Char(string="Subject")
