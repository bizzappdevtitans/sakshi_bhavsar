from odoo import models, fields, api


class Studentdetails(models.Model):
    _name = "student.details"
    _description = "Student related informations"
    _rec_name = "student_name"

    student_sequence_number = fields.Integer(
        string="Student sequence",
        required=True,
        readonly=True,
        copy=False,
        default=0,
    )

    # sequence number generate using create() (orm method) and api.model(decorator)
    @api.model
    def create(self, vals):
        vals["student_sequence_number"] = self.env["ir.sequence"].next_by_code(
            "student.details"
        )
        return super(Studentdetails, self).create(vals)

    student_id = fields.Many2one(
        comodel_name="exam.details",
        string="Student's exam details",
    )
    student_examsubject_id = fields.Many2one(
        comodel_name="subject.details", string="Student's Exam subject details"
    )

    student_name = fields.Char(string="Student Name")

    student_fees = fields.Float(string="Total Fees (including exam fees-500)")

    student_address = fields.Text(string="Student Address")

    student_enrollment_no = fields.Integer(string="Student Enrollement number")

    student_exam_end_date_time = fields.Datetime(string="Student Exam Date & Time")

    student_gender = fields.Selection(
        string="Select student gender",
        selection=[
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
        ],
    )

    students_exam_seatings = fields.One2many(
        comodel_name="exam.details",
        inverse_name="assign_students_exam",
        string="Student exam seatings",
    )

    student_confirmation = fields.Boolean(
        string="Confirmation for giving exam(True/False)"
    )

    student_exam_hallticket_attach = fields.Binary(
        string="Attach Student Exam Hallticket"
    )

    # function of fees calculation on button click
    def action_fees_calculation(self):
        for rec in self:
            student_fees = rec.student_fees - 500
            rec.student_exam_fees = student_fees

    student_exam_fees = fields.Float(string="Student fees(excluding 500 exam fees)")

    # for smart button-[exam count]
    exam_count = fields.Integer(string="Total Exams", compute="count_exam_data")

    def count_exam_data(self):
        for rec in self:
            exam_count = self.env["exam.details"].search_count(
                [("assign_students_exam", "=", rec.id)]
            )
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
        string="Student exam Date",
        compute="onchange_date_method",
        store=True,
        readonly=False,
    )

    # [onchange]- Decorator
    @api.onchange("student_fees")
    def onchange_date_method(self):
        todays_date = fields.Date.today()
        for rec in self:
            if rec.student_exam_start_date != todays_date:
                rec.student_exam_start_date = todays_date
                return {
                    "warning": {
                        "title": "Date will change by method onchange",
                        "message": "you have changed your exam fees, now the exam date"
                        " will be automatically changed with todays date.",
                    }
                }
