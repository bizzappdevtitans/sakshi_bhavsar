from odoo import models, fields


class Facultydetails(models.Model):
    _name = "subject.details"
    _description = "Examination Subject related informations"

    subject_id = fields.Many2one("exam.details", string="Subject ID")
    subject_faculty_id = fields.Many2one("faculty.details", string="Faculty details")

    subject_name = fields.Char(string="Subject Name")

    subject_chapters = fields.Float(string="Exam subject chapters")

    subject_description = fields.Text(string="Subject description")

    subject_textbooks_no = fields.Integer(string="No of textbooks to be read for exam")

    subject_exam_date = fields.Date(string="Only exam Date")

    subject_exam_date_time = fields.Datetime(string="Exam Date Time")

    other_subject_name = fields.Selection(
        selection=[
            ("python", "Python"),
            ("xml", "XML"),
            ("javascript", "Javascript"),
            ("sql", "SQL"),
        ]
    )

    exam_subject_confirmation = fields.Boolean(
        string="Confirm to take exam of this subject(True/False)"
    )

    subject_textbooks = fields.Binary(string="Attach textbooks")
