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
        "student.details", "relation_id_field3", string="One to Many Relational field"
    )

    state_field = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
        ],
        string="StatusBar",
        required=True,
        default="draft",
    )


class Studentdetails(models.Model):
    _name = "student.details"
    _description = "Student related informations"

    relation_id_field3 = fields.Many2one("exam.details")
    student_id = fields.Many2one("exam.details", string="Student ID")
    student_fees = fields.Float(string="Student Fees")
