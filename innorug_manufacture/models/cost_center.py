from odoo import fields, models, _, api
from datetime import date
import logging
_logger = logging.getLogger(__name__)



class CostCenter(models.Model):
    _name = "mrp.cost.center"
    _description = 'Cost Center'
    _rec_name = "name"

    # @api.model
    # def default_get(self, fields):
    #     res = super(CostCenter, self).default_get(fields)
    #     order = self.env['mrp.workorder'].search([('subcontractor_ids','=',self._context.get('subcontractor_ids'))])     
    #     res.update({'subcontractor_ids': order.subcontractor_ids.name})
    #     _logger.info("~~~~~~~~~~~~%r~~~~~~res~~", res)
    #     return res
    
    
    


    name = fields.Char(string='Order Reference', required=True,
                          readonly=True, default=lambda self: _('New'))
    job_work_id = fields.Many2one("mrp.job.work", string="Job Work")
    job_id = fields.Many2many("mrp.job.work", string="Job Work")

    subcontractor_id = fields.Many2one(related="job_work_id.subcontractor_id",string="Subcontractor")
    mrp_production_id = fields.Many2many("mrp.production", string="Manufacturing Order")
    
    
    work_center_id = fields.Many2one(related="job_work_id.work_center_id",string="Work Center")
    product_id =fields.Many2one(related="job_work_id.product_id", string="Product")
    product_qty = fields.Float(related="job_work_id.product_qty", string="Allotment Qty(Units)")
    design = fields.Char(related = "job_work_id.design", string="Design", readonly="1")
    area = fields.Float(related="job_work_id.area", string="Area", readonly="1")
    size = fields.Char(related="job_work_id.size", string="Product Size Name", readonly="1")
    shape = fields.Char(related="job_work_id.shape", string="Shape", readonly="1")
    size_type = fields.Selection(related="job_work_id.size_type", string='Product Size Type', readonly="1")
    
    
    cost_center_line_ids = fields.One2many("mrp.cost.center.line","cost_center_id", string="Cost Center")



    issue_date = fields.Date(related="job_work_id.issue_date", string='Issued Date')
    expected_received_date = fields.Date(related="job_work_id.expected_received_date", string='Expected Received Date')
    total_day = fields.Integer(related="job_work_id.total_day", string='Total Days')

    time_incentive = fields.Float("Time Incentive")
    time_penalities = fields.Float("Time Penality")
    fragments = fields.Float("Fragments")
    fragments_penality = fields.Float("Fragments Penalities")
    
    cost_per_yard = fields.Float("Cost Per Yard")
    
    
    
    #O2m relation
    product_allotement_ids = fields.One2many(related="job_work_id.subcontracter_alloted_product_ids")
    
    
    
    # main job work
    main_job_work_id = fields.Many2one("main.jobwork", string="Main Job")
    
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'mrp.cost.center') or _('New')
        res = super(CostCenter, self).create(vals)
        return res
    
    
    
    
    
    
    
    
class CostCenterLine(models.Model):
    _name = "mrp.cost.center.line"
    _description = 'Cost Center Line'
    
    name = fields.Char(string="Cost Center")
    cost_center_id = fields.Many2one("mrp.cost.center",string="Cost Center")
    job_work_id = fields.Many2one("mrp.job.work", string="Job Work")
    mrp_production_id = fields.Many2many(related="cost_center_id.mrp_production_id", string="MRP Production")
    product_id =fields.Many2one(related="cost_center_id.product_id", string="Product")
    check_no = fields.Char("Chq. No.")
    total_square_yard = fields.Float("Total Sqr. Yard")
    cost_per_yard = fields.Float("Cost Per Yard")
    time_incentive = fields.Float("Time Incentive")
    time_penalities = fields.Float("Time Penality")
    last_baazar_date = fields.Date("Last Baazar Date")
    
    
    

  




    