from odoo import models, api
import datetime
from datetime import datetime
import pytz


class GenerateReport(models.AbstractModel):
    _name = 'report.dynamic_report.generate_report'
    _inherit = 'report.report_xlsx.abstract'

    @api.multi
    def generate_xlsx_report(self, workbook, data, lines):
        # print (data)
        form = data.get('form', False)
        # print(form)
        # List field name selected
        field_name = form.get('field_name', False)
        # print(type(field_name))
        field_sel = []
        for item in field_name:
            f_name = self.env['ir.model.fields'].browse(item).name
            field_sel.append(f_name)
        # print(field_sel)
        # Domain
        domain = []
        domain_lines = self.env['dynamic.domain.line'].browse(form.get('domain_lines', False))
        for d_line in domain_lines:
            temp = ()
            # print(type(temp))
            d_val = str(d_line.value) or False
            if d_val in ('false', 'False'):
                d_val = False
            if d_val in ('true', 'True'):
                d_val = True
            temp = (str(d_line.field_name.name), str(d_line.operator), d_val)
            domain.append(temp)
        # print('Domain: ', domain)
        model_obj = self.env['ir.model'].browse(form.get('model_name', False)).model
        model_name = self.env['ir.model'].browse(form.get('model_name', False)).name
        # print(model_obj)
        off_set = form.get('set_offset', False)
        limit = form.get('limit_rec', False)
        order = form.get('order_on_field', False)
        order_field = self.env['ir.model.fields'].browse(order).name
        if order and form.get('order_type', False):
            order_field = order_field + ' desc'
        header = form.get('header_text', False)
        sheet_name = form.get('sheet_name', False)
        recs = self.env[model_obj].search_read(domain, field_sel, offset=off_set, limit=limit, order=order_field)

        sheet = workbook.add_worksheet(str(sheet_name))
        format0 = workbook.add_format({'font_size': 20, 'align': 'center', 'bold': True, 'border': 1})
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True, 'border': 1})
        format21 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True, 'border': 1})
        font_size_8_l = workbook.add_format({'font_size': 8, 'align': 'left', 'border': 1})

        sheet.set_header(header)
        sheet.merge_range(1, 7, 2, 10, str(model_name) + ' Report', format0)
        user = self.env['res.users'].browse(self.env.uid)
        # print (user.tz)
        tz = pytz.timezone(user.tz)
        time = pytz.utc.localize(datetime.now()).astimezone(tz)
        sheet.merge_range('A5:G5', 'Report Date: ' + str(time.strftime("%Y-%m-%d %H:%M %p")), format1)
        col = 0
        for item in field_sel:
            sheet.write(6, col, item, format21)
            col = col + 1
        row = 7
        col = 0
        for key in recs:
            for item in field_sel:
                if item is False:
                    row_data = None
                else:
                    row_data = key[item]
                sheet.write(row, col, str(row_data), font_size_8_l)
                col = col + 1
            row = row + 1
            col = 0
