from odoo import models, fields, api


class StudentDetails(models.Model):
    _name = "student.details"
    _description = "Student related information"
    _rec_name = "student_name"

    student_sequence_number = fields.Integer(
        string="Student sequence",
        required=True,
        readonly=True,
        copy=False,
        default=0,
    )

    @api.model
    def create(self, vals):
        # this will create sequence number
        vals["student_sequence_number"] = self.env["ir.sequence"].next_by_code(
            "student.details")
        return super(StudentDetails, self).create(vals)

    gender_unlink = fields.Char(
        string="Male gender Data(Deleted)",
        compute="_compute_action_gender_male_unlink",
        readonly=True,
    )

    @api.depends()
    def _compute_action_gender_male_unlink(self):
        """
        this will delete all the records whose gender will be male
        """
        for record in self:
            unlink_gender_male_record = self.env["student.details"].search(
                [("student_gender", "=", "male")])
            self.gender_unlink = unlink_gender_male_record
            unlink_gender_male_record.unlink()

    student_unique_code = fields.Char(string="Unique code")

    def write(self, vals):
        """
        this will write the unique code if the field will be empty
        """
        if not self.student_unique_code and not vals.get('student_unique_code'):
            vals['student_unique_code'] = self.env['ir.sequence'].next_by_code('student.details')
        return super(StudentDetails, self).write(vals)

    student_fees_count = fields.Integer(
        string="Total Count whose fees(15,000+)",
        compute="_compute_action_student_fees_count",
        readonly=True,
    )

    @api.depends()
    def _compute_action_student_fees_count(self):
        """
        this will give the total count of students whose fees are greater than 15000
        """
        for record in self:
            search_count_total_students = self.env["student.details"].search_count(
                [("student_fees", ">=", 15000)])
            self.student_fees_count = search_count_total_students

    student_id = fields.Many2one(
        comodel_name="exam.details", string="Student's Exam details")

    student_examsubject_id = fields.Many2one(
        comodel_name="subject.details", string="Student's Exam subject details")

    student_name = fields.Char(string="Student Name")

    student_fees = fields.Float(string="Total Fees(exam fees [+500])")

    student_address = fields.Text(string="Student Address")

    student_enrollment_no = fields.Integer(string="Student Enrollement number")

    student_exam_end_date_time = fields.Datetime(string="Exam Ending Date & Time")

    student_gender = fields.Selection(
        string="Select Student gender",
        selection=[
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
        ],
    )

    students_exam_seatings = fields.One2many(
        comodel_name="exam.details",
        inverse_name="assign_students_exam",
        string="Exam seating Arrangement")

    student_confirmation = fields.Boolean(
        string="Confirm for giving exam(True/False)", required=True, default=True)

    student_exam_hallticket_attach = fields.Binary(
        string="Attach Student Exam Hallticket")

    def action_fees_calculation(self):
        """
        this function is used for calculating student fees, excluding(500) as exam fees
        """
        for rec in self:
            student_fees = rec.student_fees - 500
            rec.student_exam_fees = student_fees

    student_exam_fees = fields.Float(string="Student fees(exam fees [-500])")

    exam_count = fields.Integer(string="Total Exams", compute="_compute_exam_data")

    def _compute_exam_data(self):
        """
        this will generate total count of exams
        """
        for rec in self:
            exam_count = self.env["exam.details"].search_count(
                [("assign_students_exam", "=", rec.id)])
            rec.exam_count = exam_count

    def action_count_exam(self):
        if self.exam_count == 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Exam Details",
                "res_model": "exam.details",
                "view_type": "form",
                "view_mode": "form",
                "res_id": self.student_id.id,
                "domain": [("assign_students_exam", "=", self.id)],
                "target": "new",
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "name": "Exam Details",
                "res_model": "exam.details",
                "view_mode": "tree,form",
                "domain": [("assign_students_exam", "=", self.id)],
                "target": "new",
            }

    student_exam_start_date = fields.Date(
        string="Exam starting Date",
        compute="_compute_onchange_date_method",
        store=True,
        readonly=True,
    )

    @api.onchange("student_fees")
    def _compute_onchange_date_method(self):
        """
        this will automatically set the exam date as today
        date on changing the student_fees field
        """
        todays_date = fields.Date.today()
        for rec in self:
            if rec.student_exam_start_date != todays_date:
                rec.student_exam_start_date = todays_date
                return {
                    "warning": {
                        "title": "Date will change by method [onchange]",
                        "message": "you have changed your exam fees, now the exam date"
                        " will be automatically changed with todays date.",
                    }
                }
