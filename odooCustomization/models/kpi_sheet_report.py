from odoo import models, fields, api
from odoo.exceptions import UserError

import base64
import contextlib
import io
import xlwt
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import serialize_exception,content_disposition
import base64

import StringIO
import logging
_logger = logging.getLogger(__name__)

class kpi_sheet_report(models.Model):
    _name = 'kpi_sheet.report'
    _description = 'KPI SHEET REPORTS'
    date_from  =  fields.Date('From')
    date_to =  fields.Date('To')
    location_id =  fields.Many2one('stock.location', string="Location")

    @api.multi
    def action_test_connection(self):
        self.ensure_one()
        if self.date_from and self.date_to and self.location_id:
            return {
                'type': 'ir.actions.act_url',
                'url': '/web/binary/download_xls_document?model=kpi_sheet.report&id=%s&date_from=%s&date_to=%s&location_id=%s&filename=kpi_reporting.xls' % (
                    self.id,self.date_from , self.date_to , self.location_id.id),
                'target': 'new',
            }
        else:
            raise UserError("Fill Valid Data ")
class Binary(http.Controller):
    @http.route('/web/binary/download_xls_document', type='http', auth="public")
    @serialize_exception
    def download_xls_document(self, model, id, date_from,date_to,location_id,filename=None, **kw):
        Model = request.registry[model]
        cr, uid, context = request.cr, request.uid, request.context

        wb1 = xlwt.Workbook(encoding='utf-8')
        ws1 = wb1.add_sheet('KPI Reporting')
        fp = StringIO.StringIO()

        font_style = xlwt.XFStyle()
        # headers are bold
        font_style.font.bold = True

        row_num = 0

        genData=self.generateKpiData(date_from,date_to,location_id) #[["sno","id","name","status"],[1,1,"Sudish","Active"],[2,2,"Niraj","Active"],[3,3,"Test","Active"]]
        columns = genData[0]

        #write column headers in sheet
        for col_num in range(len(columns)):
            ws1.write(row_num, col_num, columns[col_num], font_style)

        # Here all excel data and calculations
        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        
        # row_num = row_num + 1
        # ws1.write(row_num, 0, date_from, font_style)
        # ws1.write(row_num, 1, date_to, font_style)
        # ws1.write(row_num, 2, location_id, font_style)
        for i in range(len(genData)-1):
            row_num = row_num + 1
            for j in range(len(genData[i+1])):
                ws1.write(row_num, j, genData[i+1][j], font_style)


        wb1.save(fp)
        filecontent = fp.getvalue()

        if not filecontent:

            return request.not_found()

        else:
            if not filename:
                filename = '%s_%s' % (model.replace('.', '_'), id)
            return request.make_response(filecontent,
                                        [('Content-Type', 'application/octet-stream'),
                                        ('Content-Disposition', content_disposition(filename))])
    
    def validateData(nvalue):
        if nvalue is None:
            return False
        else:
            return True

    def generateKpiData(self,dateFrom,dateTo,locationId):
        genData=[["Id","Product Name","Product Category","Supplier Category","Move date","Way","Supplier Name","PO Name","Supplier Unit Price","Purchase Unit Price With Tax","Quantity","Sales Price","From","To","Batch Number","MOHP Essesntial","Government Supply","Formulary","Medicine","Antibiotic","Lab item","Medical Item","Other Item","Physic Medicine","Insurance Medicine","Vertical Program","Dental Item","Min Quantity", "Max quantity"]]
        sql="""          
                select 
                row_number() OVER (order by sm.date) as id,
                pt.name as name,
                pp.id as product_id,
                sm.product_qty as quantity,
                sm.date as date_order,
                sm.location_dest_id, 
                sm.location_id,
                spol.lot_id,
                CASE WHEN sm.location_dest_id ="""+str(locationId)+ """ THEN '+'
                WHEN sm.location_id = """+str(locationId)+ """  THEN '-'
                ELSE '*'
                END as way,


                srcloc.name as fromloc,
                dstloc.name as toloc,
                pp.default_code as itemreference,
                swo.product_min_qty,
                swo.product_max_qty,
                pt.x_formulary,
                pt.x_govt,
                pt.x_low_cost_eq, 

                pt.antibiotic,
                pt.other_item,
                pt.medical_item,
                pt.lab_item,
                pt.medicine_item,
                pt.physic_medicine,
                pt.insurance_medicine,
                pt.vertical_program,
                pt.dental_item,


                xpsc.category_name,
                pt.list_price,
                po.name as poname,
                pc.name as product_category, 
                rp.name as supplier,
                pol.price_unit as purchase_price,
                pol.price_tax  as ptax,
                (pol.price_unit+(pol.price_tax)) as amtwithtax,
                spl.sale_price as lot_sp,
                spl.name as batch_number,
                rp.supplier_category

                from 
                stock_move sm inner join product_product pp on sm.product_id=pp.id and sm.state='done' AND (sm.location_dest_id="""+str(locationId)+ """ or sm.location_id="""+str(locationId)+ """)
                LEFT JOIN stock_warehouse_orderpoint swo on swo.product_id=sm.product_id and swo.location_id = """+str(locationId)+ """ 
                LEFT JOIN product_template pt on pt.id = pp.product_tmpl_id 
                LEFT JOIN stock_pack_operation_lot spol on spol.move_id = sm.id
                LEFT JOIN stock_production_lot spl on spl.id=spol.lot_id
                LEFT JOIN product_category pc on pt.categ_id= pc.id
                LEFT JOIN purchase_order_line pol on pol.id=sm.purchase_line_id
                LEFT JOIN res_partner rp on rp.id=pol.partner_id
                LEFT JOIN supplier_classification  xpsc on xpsc.id=rp.supplier_category
                LEFT JOIN purchase_order po on pol.order_id = po.id
                LEFT JOIN stock_location dstloc on dstloc.id = sm.location_dest_id
                LEFT JOIN stock_location srcloc on srcloc.id = sm.location_id

                where sm.date > '"""+str(dateFrom)+ """' and sm.date  < '"""+str(dateTo)+ """'
        """
        # Where

        # sm.date >= """ +str(dateFrom)+"""
        # sm.date <= """ +str(dateTo)+"""
        
        http.request.cr.execute(sql)
        rData=http.request.env.cr.fetchall()
        counter=0
        # _logger.error(rData)
        for data in rData:
            counter = counter+1
            mData=[]
            mData.append(counter)
            mData.append(data[1]) #Product Name
            mData.append(data[29]) #Product Category
            mData.append(data[26]) #Supplier Category
            mData.append(data[4]) #Move date
            mData.append(data[8]) #Way
            mData.append(data[30]) #Supplier Name
            mData.append(data[28]) # PO Name
            mData.append(data[31]) #Supplier Unit Price
            mData.append(data[33]) #Purchase Unit Price With Tax
            mData.append(data[3]) #Quantity
            mData.append(data[34]) #Sales Price
            mData.append(data[9]) #From
            mData.append(data[10]) #To
            mData.append(data[35]) #Batch Number
            # mData.append(data[11]) #Product reference
            mData.append(False if data[16] is None else True) #Essential
            mData.append(False if data[15] is None else True) #Government
            mData.append(False if data[14] is None else True) #Formulary
            mData.append(False if data[21] is None else True) #Medicine
            mData.append(False if data[17] is None else True) #Antibiotic
            mData.append(False if data[20] is None else True) #Lab item
            mData.append(False if data[19] is None else True) #Medical Item
            mData.append(False if data[18] is None else True) #Other Item
            mData.append(False if data[22] is None else True) #Physic Medicine
            mData.append(False if data[23] is None else True) #Insurance Medicine
            mData.append(False if data[24] is None else True) #Vertical Program
            mData.append(False if data[25] is None else True) #Dental Item
            mData.append(data[12]) #Minimum Quantity
            mData.append(data[13]) #Max Quantity

            genData.append(mData)

        return genData
