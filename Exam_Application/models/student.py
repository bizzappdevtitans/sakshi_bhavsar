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

    # --------------
    # sequence number generate
    # --------------
    @api.model
    def create(self, vals):
        vals["student_sequence_number"] = self.env["ir.sequence"].next_by_code(
            "student.details")
        return super(Studentdetails, self).create(vals)

    # --------------
    # unlink()-orm method
    # --------------
    gender_unlink = fields.Char(
        string="Male gender Data(Deleted)",
        compute="action_gender_male_unlink",
        readonly=True,
    )

    @api.depends()
    def action_gender_male_unlink(self):
        for record in self:
            unlink_gender_male_record = self.env["student.details"].search(
                [("student_gender", "=", "male")])
            self.gender_unlink = unlink_gender_male_record
            unlink_gender_male_record.unlink()
        # column_id = self.env["student.details"].browse(19)-->delete single 19th record
        # column_id.unlink()

    # -----------------
    # write()-orm method
    # -----------------
    """@api.model
    def write(self, vals):
        for record in self:
            vals = self.env["student.details"].search([("student_name", "=", "SSDE")])
            vals.write({"student_name": "Sakshi"})"""

    # -----------------
    # search_count()-orm method
    # -----------------
    student_fees_count = fields.Integer(
        string="Students Count whose fees(more than 15000)",
        compute="action_student_fees_count",
        readonly=True,
    )

    @api.depends()
    def action_student_fees_count(self):
        for record in self:
            search_count_total_students = self.env["student.details"].search_count(
                [("student_fees", ">=", 15000)])
            self.student_fees_count = search_count_total_students

    student_id = fields.Many2one(
        comodel_name="exam.details", string="Student's exam details")

    # ------------------
    # name_get and name_search function
    # ------------------
    @api.depends("student_id")
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        args = []
        if name:
            record = self.search([("exam_fees", operator, name)] + args, limit=limit)
            return record.name_get()
        return super(Studentdetails, self).name_search(
            name=name, args=args, operator=operator, limit=limit
        )

    student_examsubject_id = fields.Many2one(
        comodel_name="subject.details", string="Student's Exam subject details")

    student_name = fields.Char(string="Student Name")

    student_fees = fields.Float(string="Total Fees(exam fees +500)")

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
        string="Confirmation for giving exam(True/False)", required=True, default=True)

    student_exam_hallticket_attach = fields.Binary(
        string="Attach Student Exam Hallticket")

    # ----------------
    # function of fees calculation on button click
    # ----------------
    def action_fees_calculation(self):
        for rec in self:
            student_fees = rec.student_fees - 500
            rec.student_exam_fees = student_fees

    student_exam_fees = fields.Float(string="Student fees(-500 exam fees)")

    # -------------
    # smart button-[exam count]
    # -------------
    exam_count = fields.Integer(string="Total Exams", compute="count_exam_data")

    def count_exam_data(self):
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

    # -------------------
    # [onchange]- Decorator
    # -------------------
    student_exam_start_date = fields.Date(
        string="Student exam Date", compute="onchange_date_method", store=True)

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
