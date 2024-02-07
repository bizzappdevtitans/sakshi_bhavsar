from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SubjectDetails(models.Model):
    _name = "subject.details"
    _description = "Subject related information"
    _order = "subject_chapters asc"
    _rec_name = "subject_name"

    subject_id = fields.Many2one(
        comodel_name="exam.details", string="Subject Exam details")

    subject_faculty_id = fields.Many2many(
        comodel_name="faculty.details", string="Subject Faculty details")

    subject_sequence_number = fields.Char(
        string="Subject sequence",
        required=True,
        record=True,
        copy=False,
        default="New Sequence",
    )

    @api.model
    def create(self, vals):
        # this will create sequence number
        vals["subject_sequence_number"] = self.env["ir.sequence"].next_by_code(
            "subject.details")
        return super(SubjectDetails, self).create(vals)

    subject_chapters_search = fields.Char(
        string="subject having chapters(8+)",
        compute="_compute_action_chapter_count_search",
        readonly=True,
    )

    @api.depends()
    def _compute_action_chapter_count_search(self):
        """
        this will return the id whose subject_chapters are greater than 8
        """
        for record in self:
            search_subject_chapters = self.env["subject.details"].search(
                [("subject_chapters", ">=", 8)])
            self.subject_chapters_search = search_subject_chapters

    subject_search_read = fields.Char(
        string="Subject Data(ID,SubjectName,SubjectChapters)",
        compute="_compute_action_search_read_method",
        readonly=True,
    )

    @api.depends()
    def _compute_action_search_read_method(self):
        """
        this will return all the records with fields(id,subject_name,subject_chapters)
        """
        for record in self:
            record_values = self.env["subject.details"].search_read(
                [], ["subject_name", "subject_chapters"])
            self.subject_search_read = record_values

    @api.model
    def name_get(self):
        result = []
        for record in self:
            name = record.subject_name + " - " + record.subject_sequence_number
            result.append((record.id, name))
        return result

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        if args is None:
            args = []
        domain = args + [
            "|",
            "|",
            ("subject_name", operator, name),
            ("subject_chapters", operator, name),
            ("exam_subject_confirmation", operator, name),
        ]
        return super(SubjectDetails, self).search(domain, limit=limit).name_get()

    subject_name = fields.Char(string="Subject Name")

    subject_chapters = fields.Float(string="Chapters for exam")

    subject_description = fields.Text(string="Subject description")

    subject_textbooks_no = fields.Integer(string="No of textbooks for the exam")

    subject_exam_start_date = fields.Date(string="Exam starting Date")

    subject_exam_end_date_time = fields.Datetime(string="Exam ending Date & Time")

    exam_subject_confirmation = fields.Boolean(
        string="Confirm to take exam of this subject(True/False)")

    subject_textbooks = fields.Binary(string="Attach subject textbooks")

    @api.constrains("subject_textbooks_no")
    def constraints_subject_textbook_no(self):
        """
        this will give validation error if the number of subject_textbook is 0 or
        having negative number or greater than 3
        """
        for record in self:
            if record.subject_textbooks_no > 3:
                raise ValidationError(
                    "No of textbooks for exam to study,It cannot be more than 3")
            elif record.subject_textbooks_no < 0:
                raise ValidationError("Enter positive numbers")
            elif record.subject_textbooks_no == 0:
                raise ValidationError("Enter atleast 1 textbook")
