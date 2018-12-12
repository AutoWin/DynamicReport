from odoo import api, models, fields

class report_sale_preview(models.Model):
    _inherit = 'sale.order'
    preview = fields.Html('Report Preview')

    @api.multi
    def generate_preview(self):
        html = self.env['report'].get_html(self, 'sale.report_saleorder')
        self.write({'preview': html})
        return True

