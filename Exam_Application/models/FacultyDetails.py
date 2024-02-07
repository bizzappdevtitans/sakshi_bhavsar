from odoo import models, fields, api


class FacultyDetails(models.Model):
    _name = "faculty.details"
    _description = "Faculty related Information"
    _rec_name = "faculty_name"

    faculty_id = fields.Many2one(comodel_name="exam.details", string="Exam details")

    faculty_sequence_number = fields.Integer(
        string="Faculty sequence number",
        required=True,
        readonly=True,
        copy=False,
        default=0,
    )

    @api.model
    def create(self, vals):
        # this will create sequence number
        vals["faculty_sequence_number"] = self.env["ir.sequence"].next_by_code(
            "faculty.details")
        return super(FacultyDetails, self).create(vals)

    faculty_unique_code = fields.Char(string="Unique code")

    def write(self, vals):
        """
        this will generate the unique code if the field is empty
        """
        if not self.faculty_unique_code and not vals.get("faculty_unique_code"):
            vals["faculty_unique_code"] = self.env["ir.sequence"].next_by_code(
                "faculty.details")
        return super(FacultyDetails, self).write(vals)

    faculty_paper_state_search = fields.Integer(
        string="Total Question paper ready for exam",
        compute="_compute_questionpaper_search_count",
        readonly=True,
    )

    @api.depends()
    def _compute_questionpaper_search_count(self):
        """
        this will generate the total count of papers whose state is Done
        """
        for record in self:
            search_count_paper_state = self.env["faculty.details"].search_count(
                [("faculty_states", "=", "done")])
            self.faculty_paper_state_search = search_count_paper_state

    @api.model
    def name_get(self):
        result = []
        for record in self:
            name = record.faculty_name + " - " + record.faculty_gender
            result.append((record.id, name))
        return result

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        if args is None:
            args = []
        domain = args + [
            "|",
            "|",
            ("faculty_name", operator, name),
            ("faculty_designation", operator, name),
            ("faculty_gender", operator, name),
        ]
        return super(FacultyDetails, self).search(domain, limit=limit).name_get()

    faculty_subject_id = fields.Many2one(
        comodel_name="subject.details", string="Exam subject details")

    faculty_name = fields.Char(string="Faculty Name")

    faculty_fees = fields.Float(string="Faculty salary")

    faculty_designation = fields.Text(string="Faculty Designation")

    faculty_subject_no = fields.Integer(string="Faculty subject code number")

    faculty_subject_starting_exam_date = fields.Date(string="Exam starting Date")

    faculty_subject_ending_exam_date_time = fields.Datetime(
        string="Exam ending Date & Time")

    faculty_gender = fields.Selection(
        string="Faculty gender",
        selection=[
            ("female", "Female"),
            ("male", "Male"),
            ("other", "Other"),
        ],
    )

    faculty_availability = fields.Boolean(string="Is faculty available", default=True)

    faculty_documents_attach = fields.Binary(string="Faculty Identity documents")

    faculty_states = fields.Selection(
        selection=[
            ("cancel", "Cancel"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
        ],
        string="Question paper state for exam",
        help="this is about the state of exam question paper.Are question papers ready for exam?",
        required=True,
        default="in_progress",
    )

    def faculty_action_button(self):
        self.write({"faculty_states": "cancel"})

    def faculty_in_progress_button(self):
        self.write({"faculty_states": "in_progress"})

    def faculty_action_done(self):
        self.write({"faculty_states": "done"})
