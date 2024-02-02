from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Subjectdetails(models.Model):
    _name = "subject.details"
    _description = "Examination Subject related informations"
    _order = "subject_chapters asc"
    _rec_name = "subject_name"

    subject_id = fields.Many2one(
        comodel_name="exam.details", string="Subject Exam details")
    subject_faculty_id = fields.Many2one(
        comodel_name="faculty.details", string="Subject Faculty details")

    subject_sequence_number = fields.Char(
        string="Subject sequence",
        required=True,
        record=True,
        copy=False,
        default="New Sequence",
    )

    # ------------------
    # sequence number generate
    # ------------------
    @api.model
    def create(self, vals):
        vals["subject_sequence_number"] = self.env["ir.sequence"].next_by_code(
            "subject.details")
        return super(Subjectdetails, self).create(vals)

    # -------------
    # search()-orm method
    # -------------
    subject_chapters_search = fields.Char(
        string="subject having chapters(more than 8)",
        compute="action_chapter_count_search",
        readonly=True,
    )

    @api.depends()
    def action_chapter_count_search(self):
        for record in self:
            search_subject_chapters = self.env["subject.details"].search(
                [("subject_chapters", ">=", 8)])
            self.subject_chapters_search = search_subject_chapters

    # ---------------
    # search_read()-orm method
    # ---------------
    subject_search_read = fields.Char(
        string="Subject Data(ID,SubjectName,SubjectChapters)",
        compute="action_search_read_method",
        readonly=True,
    )

    @api.depends()
    def action_search_read_method(self):
        for record in self:
            record_values = self.env["subject.details"].search_read(
                [], ["subject_name", "subject_chapters"])
            self.subject_search_read = record_values

    subject_name = fields.Char(string="Subject Name")

    subject_chapters = fields.Float(string="Subject chapters included for exam")

    subject_description = fields.Text(string="Subject exam description")

    subject_textbooks_no = fields.Integer(
        string="No of textbooks to be read for the exam")

    subject_exam_start_date = fields.Date(string="Exam starting Date")

    subject_exam_end_date_time = fields.Datetime(string="Exam ending Date & Time")

    exam_subject_confirmation = fields.Boolean(
        string="Confirm to take exam of this subject(True/False)")

    subject_textbooks = fields.Binary(string="Attach subject textbooks")

    # ----------------------
    # constraints()- Decorator
    # ----------------------
    @api.constrains("subject_textbooks_no")
    def constraints_subject_textbook_no(self):
        for record in self:
            if record.subject_textbooks_no > 3:
                raise ValidationError(
                    "No of textbooks for exam to study,cannot be more than 3"
                )
            elif record.subject_textbooks_no < 0:
                raise ValidationError("Enter positive numbers")
            elif record.subject_textbooks_no == 0:
                raise ValidationError("Enter atleast 1 textbook")
