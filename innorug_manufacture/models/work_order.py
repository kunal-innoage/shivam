from odoo import fields, models, _, api
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class MrpWorkOrder(models.Model):
    _inherit = 'mrp.workorder'

    # Day Calculate
    # @api.onchange('date_planned_start', 'date_planned_finished')
    # def calculate_date(self):
    #     if self.date_planned_start and self.date_planned_finished:
    #         d1=datetime.strptime(str(self.date_planned_start),'%Y-%m-%d  %H:%M:%S') 
    #         d2=datetime.strptime(str(self.date_planned_finished),'%Y-%m-%d  %H:%M:%S')
    #         d3=d2-d1
    #         self.total_duration=str(d3.days)



   
    total_duration = fields.Integer(string="Total Duration", default= 0.0)
    remaining_qty = fields.Float(string="Remaining", default= 0.0)
    

    #  M2o relation
    manager_id = fields.Many2one('res.partner', string='Manager')

    

    # O2m relation
    job_work_lines_ids = fields.One2many("mrp.job.work","mrp_work_order_id", "Job Work")
    # default_alloted_product_ids =fields.One2many("subcontractor.alloted.product", "work_order_id", string = "Alloted Product")
    
    
    
    # def do_finish(self):
    #     return super(MrpWorkOrder, self).do_finish()
    
    
    # def record_production(self):
    #     return super(MrpWorkOrder, self).record_production()
    

    # @api.onchange('manager_id')
    # def default_alloted_product(self):
    #     sub_allotment_id =self.env['subcontractor.alloted.product']
    #     mrp_routing_obj = self.env['mrp.routing.workcenter']
    #     for job_work in self:
    #         for raw_move in job_work.production_bom_id.operation_ids:
    #             if raw_move.workcenter_id == job_work.workcenter_id:
    #                 mrp_routing_id = mrp_routing_obj.search([('workcenter_id','=', raw_move.workcenter_id.id),('bom_id','=', raw_move.bom_id.id)], limit=1)
    #                 _logger.info("~~~~~~3~~~~sssssssssssss~~%r~~~~~~~~",  mrp_routing_id.operation_component_ids)
    #                 for rec in mrp_routing_id.operation_component_ids:
    #                     sub_allotment_id = sub_allotment_id.search([('alloted_product_id','=', rec.product_id.id),('work_order_id','in', [job_work.id])])
    #                     if not sub_allotment_id:
    #                         sub_allotment_id =sub_allotment_id.create({
    #                             "parent_product_id" : job_work.production_bom_id.id,
    #                             "alloted_product_id" : rec.product_id.id,
    #                             "alloted_quantity" : rec.product_qty * job_work.qty_production,
    #                             "consumed_quantity": 0,
    #                             "returned_quantity": 0,
    #                             "work_order_id": job_work.id,
    #                         })
    #                     else:
    #                         sub_allotment_id.alloted_quantity = rec.product_qty * job_work.qty_production
    #                         sub_allotment_id.parent_product_id = job_work.production_bom_id
    #                         sub_allotment_id.work_order_id = job_work.id




    @api.onchange('job_work_lines_ids')
    def calculate_qty(self):
        qty =0
        for work_order in self:
            qty_list =[]
            last_job_order = False
            for rec in work_order.job_work_lines_ids:
                qty_list.append(rec.product_qty)
                last_job_order = rec
                _logger.info("~~~~~~qty~~~~~~%r~~~~~~~~", rec.product_qty)
            _logger.info("~~~~~~qty~~~~~~%r~~~~~~~~", qty_list)
            for l in qty_list:
                qty += l
            work_order.remaining_qty = work_order.qty_production - qty
            # _ logger.info("~~~~~~qty~~~~~~%r~~~~kkkk~~~~", self.remaining_qty)
            if work_order.remaining_qty < 0:
                if last_job_order:
                    work_order.remaining_qty += last_job_order.product_qty
                    last_job_order.unlink()
            











 


        
