from odoo import models, fields, api


class Facultydetails(models.Model):
    _name = "faculty.details"
    _description = "Faculty Informations"
    _rec_name = "faculty_name"

    faculty_id = fields.Many2one(
        comodel_name="exam.details", string="Faculty's subject exam details")

    faculty_sequence_number = fields.Integer(
        string="Faculty sequence number",
        required=True,
        readonly=True,
        copy=False,
        default=0,
    )

    # -----------
    # sequence number generate
    # ----------
    @api.model
    def create(self, vals):
        vals["faculty_sequence_number"] = self.env["ir.sequence"].next_by_code(
            "faculty.details")
        return super(Facultydetails, self).create(vals)

    # -----
    # write()-orm method
    # -----
    @api.depends()
    def action_button_write(self):
        column_id = self.env["faculty.details"].browse(7)  # update single 7th record
        column_id.write(
            {
                "faculty_name": "BBBB",
                "faculty_fees": 30000.5,
                "faculty_address": "ADDRESS OF FACULTYSS",
                "faculty_gender": "male",
            }
        )

    # -----
    # search_count()-orm method
    # -----
    faculty_paper_state_search = fields.Integer(
        string="No. of Question paper ready for exam",
        compute="questionpaper_search_count",
        readonly=True,
    )

    @api.depends()
    def questionpaper_search_count(self):
        for record in self:
            search_count_paper_state = self.env["faculty.details"].search_count(
                [("faculty_states", "=", "done")])
            self.faculty_paper_state_search = search_count_paper_state

    faculty_subject_id = fields.Many2one(
        comodel_name="subject.details", string="Faculty's subject details")

    faculty_name = fields.Char(string="Faculty Name")

    faculty_fees = fields.Float(string="Faculty salary")

    faculty_designation = fields.Text(string="Faculty Designation")

    faculty_subject_no = fields.Integer(string="Faculty subject code number")

    faculty_subject_starting_exam_date = fields.Date(
        string="Faculty subject exam starting Date")

    faculty_subject_ending_exam_date_time = fields.Datetime(
        string="Faculty subject exam ending Date & Time")

    faculty_gender = fields.Selection(
        string="Faculty gender",
        selection=[
            ("female", "Female"),
            ("male", "Male"),
            ("other", "Other"),
        ],
    )

    faculty_availability = fields.Boolean(
        string="Confirm to available on the exam day(True/False)", default=True
    )

    faculty_documents_attach = fields.Binary(string="Attach Faculty Identity documents")

    faculty_states = fields.Selection(
        selection=[
            ("cancel", "Cancel"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
        ],
        string="State of Question paper for exam",
        required=True,
        default="in_progress",
    )

    # ---------
    # buttons state change- [widget statusbar]
    # ---------
    def faculty_action_button(self):
        self.write({"faculty_states": "cancel"})

    def faculty_in_progress_button(self):
        self.write({"faculty_states": "in_progress"})

    def faculty_action_done(self):
        self.write({"faculty_states": "done"})
