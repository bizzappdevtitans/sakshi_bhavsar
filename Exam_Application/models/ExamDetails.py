from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ExamDetails(models.Model):
    _name = "exam.details"
    _description = "Exam related Information"
    _rec_name = "exam_name"

    exam_sequence_number = fields.Char(
        string="Exam sequence",
        required=True,
        readonly=True,
        copy=False,
        default="New Sequence",
    )

    @api.model
    def create(self, vals):
        """
        this will create sequence number
        """
        vals["exam_sequence_number"] = self.env["ir.sequence"].next_by_code(
            "exam.details")
        return super(ExamDetails, self).create(vals)

    exam_search_count = fields.Integer(
        string="No. of students giving the exam(7+) :",
        compute="_compute_exam_search_count",
        readonly=True,
    )

    @api.depends()
    def _compute_exam_search_count(self):
        """
        this will return total number of students whose count is greater than 7
        """
        for record in self:
            search_count_total_students = self.env["exam.details"].search_count(
                [("students_number", ">=", 7)])
            self.exam_search_count = search_count_total_students

    exam_name = fields.Char(string="Exam name")

    exam_start_date = fields.Date(string="Exam Starting Date")

    exam_end_date_time = fields.Datetime(string="Exam ending Date & Time")

    exam_confirmation = fields.Boolean(string="Is exam confirmed")

    exam_fees = fields.Float(string="Exam holding fee")

    students_number = fields.Integer(string="Total students for exam")
    # color_widget = fields.Integer(string="Color Picker")

    seating_option = fields.Selection(
        string="Sections for Students exam",
        selection=[
            ("a", "A"),
            ("b", "B"),
            ("c", "C"),
            ("d", "D"),
            ("e", "E"),
            ("f", "F"),
            ("g", "G"),
        ],
    )

    attach_documents = fields.Binary(string="Attach Exam related documents")

    exam_description = fields.Text(string="Exam Description")
    term_conditions = fields.Text(string="Term and conditions for exam")

    exam_college_address = fields.Html(string="Examination address")

    assign_students_exam = fields.One2many(
        comodel_name="student.details",
        inverse_name="student_id",
        string="Assign students for exam",
    )

    @api.model
    def name_get(self):
        result = []
        for record in self:
            name = record.seating_option + " - " + record.exam_name
            result.append((record.id, name))
        return result

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        if args is None:
            args = []
        domain = args + [
            "|",
            ("exam_name", operator, name),
            ("exam_fees", operator, name),
        ]
        return super(ExamDetails, self).search(domain, limit=limit).name_get()

    assign_supervisors_exam = fields.One2many(
        comodel_name="supervisor.details",
        inverse_name="supervisor_id",
        string="Assign supervisors for exam",
    )

    states = fields.Selection(
        selection=[
            ("in_progress", "In Progress"),
            ("done", "Done"),
        ],
        string="Exam State",
        help="this describe about the exam state.examination is done or is in_progress",
        required=True,
        default="in_progress",
    )

    _sql_constraints = [
        (
            "unique_exam_description",
            "unique (exam_description)",
            "Exam description must be unique cannot enter same as already entered",
        ),
        (
            "check_students_number",
            "check(students_number > 0)",
            "Number of students must be positive",
        ),
    ]

    @api.constrains("term_conditions", "exam_description")
    def constraints_college_name_description(self):
        """
        this will compare term conditions box with the exam description box.
        both the fields content should be different
        """
        for record in self:
            if not record.term_conditions == record.exam_description:
                ()
            else:
                raise ValidationError(
                    "term conditions box and Exam description fields content must be different"
                )

    def action_in_progress(self):
        self.write({"states": "in_progress"})

    def action_done(self):
        self.write({"states": "done"})

    student_count = fields.Integer(
        string="Total Students", compute="_compute_count_student_data"
    )

    @api.depends()
    def _compute_count_student_data(self):
        """
        this will return the total count of students giving the exam
        """
        for rec in self:
            student_count = self.env["student.details"].search_count(
                [("student_id", "=", rec.id)])
            rec.student_count = student_count

    def action_count_student(self):
        if self.student_count == 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Students",
                "res_model": "student.details",
                "view_type": "form",
                "view_mode": "form",
                "res_id": self.assign_students_exam.id,
                "domain": [("student_id", "=", self.id)],
                "target": "new",
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "name": "Students",
                "res_model": "student.details",
                "view_mode": "tree,form",
                "domain": [("student_id", "=", self.id)],
                "target": "new",
            }

    supervisor_count = fields.Integer(
        string="Total Supervisors", compute="_compute_count_supervisor_data")

    def _compute_count_supervisor_data(self):
        """
        this will return total supervisors count who will supervise the exam
        """
        for rec in self:
            supervisor_count = self.env["supervisor.details"].search_count(
                [("supervisor_id", "=", rec.id)])
            rec.supervisor_count = supervisor_count

    def action_count_supervisor(self):
        if self.supervisor_count == 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Supervisors",
                "res_model": "supervisor.details",
                "view_type": "form",
                "view_mode": "form",
                "res_id": self.assign_supervisors_exam.id,
                "domain": [("supervisor_id", "=", self.id)],
                "target": "new",
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "name": "Supervisors",
                "res_model": "supervisor.details",
                "view_mode": "tree,form",
                "domain": [("supervisor_id", "=", self.id)],
                "target": "new",
            }
