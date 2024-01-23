from odoo import models, fields


class Facultydetails(models.Model):
    _name = "subject.details"
    _description = "Examination Subject related informations"

    subject_id = fields.Many2one("exam.details", string="Subject Exam details")
    subject_faculty_id = fields.Many2one(
        "faculty.details", string="Subject Faculty details"
    )

    subject_name = fields.Char(string="Subject Name")

    subject_chapters = fields.Float(string="Subject chapters included for exam")

    subject_description = fields.Text(string="Subject exam description")

    subject_textbooks_no = fields.Integer(
        string="No of textbooks to be read for the exam"
    )

    subject_exam_date = fields.Date(string="Subject Exam Date")

    subject_exam_date_time = fields.Datetime(string="Subject Exam Date & Time")

    other_subject_name = fields.Selection(
        string="Select another subject for second exam",
        selection=[
            ("python", "Python"),
            ("xml", "XML"),
            ("javascript", "Javascript"),
            ("sql", "SQL"),
        ],
    )

    exam_subject_confirmation = fields.Boolean(
        string="Confirm to take exam of this subject(True/False)"
    )

    subject_textbooks = fields.Binary(string="Attach subject textbooks")
