from odoo import fields, models, _, api
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class MrpWorkOrder(models.Model):
    _inherit = 'mrp.workorder'


    main_job_work_id = fields.Many2one("mrp.jobwork", "Main Job Work")
    total_duration = fields.Integer(string="Total Duration", default= 0.0)
    remaining_qty = fields.Float(string="Remaining", default= 0.0)
    # sale_order_id = fields.Many2one(related = "production_id.")

    #  M2o relation
    manager_id = fields.Many2one('res.partner', string='Manager')

    

    # O2m relation
    job_work_lines_ids = fields.One2many("mrp.job.work","mrp_work_order_id", "Job Work")
    
    jobwork_allotment_ids = fields.One2many("jobwork.allotment", "work_order_id", string="Branch Wise Allotment")
    # default_alloted_product_ids =fields.One2many("subcontractor.alloted.product", "work_order_id", string = "Alloted Product")
    
    
    # @api.onchange('job_work_lines_ids')
    # def calculate_qty(self):
    #     qty =0
    #     for work_order in self:
    #         qty_list =[]
    #         last_job_order = False
    #         for rec in work_order.job_work_lines_ids:
    #             qty_list.append(rec.product_qty)
    #             last_job_order = rec
    #             _logger.info("~~~~~~qty~~~~~~%r~~~~~~~~", rec.product_qty)
    #         _logger.info("~~~~~~qty~~~~~~%r~~~~~~~~", qty_list)
    #         for l in qty_list:
    #             qty += l
    #         work_order.remaining_qty = work_order.qty_production - qty
    #         if work_order.remaining_qty < 0:
    #             if last_job_order:
    #                 work_order.remaining_qty += last_job_order.product_qty
    #                 last_job_order.unlink()
                    
                    
                    
    @api.onchange('jobwork_allotment_ids')
    def calculate_qty(self):
        qty =0
        for work_order in self:
            qty_list =[]
            last_job_order = False
            for rec in work_order.jobwork_allotment_ids:
                qty_list.append(rec.product_qty)
                last_job_order = rec
                _logger.info("~~~~~~qty~~~~~~%r~~~~~~~~", rec.product_qty)
            _logger.info("~~~~~~qty~~~~~~%r~~~~~~~~", qty_list)
            for l in qty_list:
                qty += l
            work_order.remaining_qty = work_order.qty_production - qty
            if work_order.remaining_qty < 0:
                if last_job_order:
                    work_order.remaining_qty += last_job_order.product_qty
                    last_job_order.unlink()
                    
                     
    
            











 


        
