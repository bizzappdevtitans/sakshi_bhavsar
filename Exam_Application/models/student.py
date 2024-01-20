from odoo import models, fields


class Studentdetails(models.Model):
    _name = "student.details"
    _description = "Student related informations"

    student_id = fields.Many2one("exam.details", string="Student ID")
    student_examsubject_id = fields.Many2one(
        "subject.details", string="Student Exam subject details"
    )

    student_name = fields.Char(string="Student Name")

    student_fees = fields.Float(string="Student Fees")

    student_address = fields.Text(string="Student Address")

    student_enrollment_no = fields.Integer(string="Student Enrollement")

    student_exam_date = fields.Date(string="Only exam Date")

    student_exam_date_time = fields.Datetime(string="Exam Date Time")

    student_other_exam_subject_name = fields.Selection(
        selection=[
            ("python", "Python"),
            ("xml", "XML"),
            ("javascript", "Javascript"),
            ("sql", "SQL"),
        ]
    )

    student_confirmation = fields.Boolean(
        string="Confirmation for giving exam(True/False)"
    )

    student_exam_hallticket_attach = fields.Binary(
        string="Attach Student Exam Hallticket"
    )

    subject_count = fields.Integer(
        string="No of subjects exam to be given", compute="count_subject_data"
    )

    def count_subject_data(self):
        for rec in self:
            subject_count = self.env["subject.details"].search_count(
                [("subject_id", "=", self.id)]
            )
            self.subject_count = subject_count

    def action_count_subject(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Subject details",
            "res_model": "subject.details",
            "domain": [("subject_id", "=", self.id)],
            "view_mode": "tree,form",
            "target": "current",
        }
