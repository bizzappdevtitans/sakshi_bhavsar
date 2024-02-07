from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    allowed_name_field = fields.Char(
        string="Allowed Name Field",
        config_parameter="Exam_Application.allowed_name_field",
    )
    allowed_number_field = fields.Integer(
        string="Allowed Number Field",
        config_parameter="Exam_Application.allowed_number_field",
    )
