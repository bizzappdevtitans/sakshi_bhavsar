from odoo import models, fields, api


class Studentdetails(models.Model):
    _name = "student.details"
    _description = "Student related informations"
    _order = "student_name asc"
    _rec_name = "student_name"

    student_id = fields.Many2one("exam.details", string="Student's exam details")
    student_examsubject_id = fields.Many2one(
        "subject.details", string="Student's Exam subject details"
    )

    student_name = fields.Char(string="Student Name")

    student_fees = fields.Float(string="Student Fees")

    student_address = fields.Text(string="Student Address")

    student_enrollment_no = fields.Integer(string="Student Enrollement number")

    student_exam_date_time = fields.Datetime(string="Student Exam Date & Time")

    student_gender = fields.Selection(
        string="Select student gender",
        selection=[
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
        ],
    )

    student_confirmation = fields.Boolean(
        string="Confirmation for giving exam(True/False)"
    )

    student_exam_hallticket_attach = fields.Binary(
        string="Attach Student Exam Hallticket"
    )

    # for smart button-[exam count]
    exam_count = fields.Integer(string="No of exam Data", compute="count_exam_data")

    def count_exam_data(self):
        for rec in self:
            exam_count = self.env["exam.details"].search_count(
                [("relation_field3", "=", rec.id)]
            )
            rec.exam_count = exam_count

    def action_count_exam(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Exam details count",
            "res_model": "exam.details",
            "domain": [("relation_field3", "=", self.id)],
            "view_mode": "tree,form",
            "target": "current",
        }

    student_exam_date = fields.Date(
        string="Student exam Date",
        compute="onchange_date_method",
        store=True,
        readonly=False,
    )

    # [onchange]- Decorator
    @api.onchange("student_id")
    def onchange_date_method(self):
        date_today = fields.Date.today()
        if self.student_exam_date != date_today:
            self.student_exam_date = date_today
            return {
                "warning": {
                    "title": "Date will change by method onchange",
                    "message": "you have changed the student id, now the exam date"
                    " will be automatically changed with todays date.",
                }
            }

    # [depends]- Decorator
    # @api.depends("student_id")
    # def depends_date_method(self):
    # date_today = fields.Date.today()
    # if self.student_exam_date != date_today:
    # self.student_exam_date = date_today
    # return
    # {
    # "warning": {
    # "title": "Date will change ny method depends",
    # "message": "you have changed the student id, now the exam date"
    # " will be automatically changed with todays date.",
    # }
    # }
