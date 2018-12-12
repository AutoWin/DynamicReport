from odoo import models, api


class GenerateReport(models.AbstractModel):
    _name = 'report.dynamic_report.generate_report_xlsx.xlsx'
    _inherit = 'report.report_xlsx.abstract'


