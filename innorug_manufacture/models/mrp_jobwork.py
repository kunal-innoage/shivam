from odoo import fields, models, _,api
from datetime import datetime
from odoo.exceptions import UserError, ValidationError, MissingError
import logging
_logger = logging.getLogger(__name__)


class MrpJobWork(models.Model):
    _name = "mrp.job.work"
    _description = 'Job Work'
    _rec_name = "product_id"

    name = fields.Char("Job Work")

    
    product_id = fields.Many2one(related="mrp_production_id.product_id", string="Product")
    bom_id = fields.Many2one(related="mrp_work_order_id.production_bom_id", string="Bill Of Material")
    
    product_qty = fields.Float("Quantity")
    qty_production = fields.Float('Original Production Quantity', readonly=True, related='mrp_production_id.product_qty')
    remaining_qty = fields.Float(string="Remaining Quantity", default= 0.0)

    mrp_work_order_id = fields.Many2one("mrp.workorder", "Work Order")

    mrp_production_id = fields.Many2one(related="mrp_work_order_id.production_id", string="MRP Production")
    product_id = fields.Many2one(related="mrp_work_order_id.product_id", string="MRP Production")
    manager_id = fields.Many2one(related="mrp_work_order_id.manager_id", string="Manager")

    subcontractor_id = fields.Many2one('res.partner', string='Subcontractors')
    cost_center_id = fields.Many2one("mrp.cost.center", "Cost Center")
    subcontracter_alloted_product_id = fields.One2many("subcontractor.alloted.product", "job_work_id", "Alloted Material")

    # issue_date = fields.Datetime(related="mrp_work_order_id.date_planned_start", string="Issue Date", readonly=False)
    issue_date = fields.Date(string='Issued Date')
    expected_received_date = fields.Date(string='Expected Date')
    total_day = fields.Integer(string='Total')



    work_center_id = fields.Many2one(related='mrp_work_order_id.workcenter_id', string="Work Center")
    

    cost_center_ids = fields.One2many("mrp.cost.center", "job_work_id", "Cost Center")

    #Boolean fields
    activate_inr = fields.Boolean("Activate INR")
    activate_product = fields.Boolean("Activate Product")
    active_hide_allot = fields.Boolean("Hide Details")
    active_hide_cost = fields.Boolean("Hide Details")
    active_hide_gate = fields.Boolean("Hide Details")
    active_release = fields.Boolean("Release")
    active_qa = fields.Boolean("QA")

    #Gate Pass
    warehouse = fields.Char("Warehouse")
    reference = fields.Char(string="Reference No")
    remarks =fields.Text( string="Remarks")


    #Quality Control relation
    quality_check_ids = fields.One2many("quality.check","job_work_id", string="Quality Check")
    team_id =fields.Many2one("quality.alert.team", "Team")
    test_type_id = fields.Many2one("quality.point.test_type","Test Type")
    


    

    state = fields.Selection([
        ('draft','DRAFT'),
        ('allotment','WAITING COMPONENTS'),
        ('release','RELEASED'),
        ('qa','QUALITY ASSURANCE'),
        ('received','RECEIVED'),
        ('cancel','CANCEL')
        ], string='Status', default='draft')


    # allotment_product_ids = fields.One2many("stock.move", "job_work_id", string="Allotment Product")
    



    #Day Calculate
    @api.onchange('issue_date', 'expected_received_date','total_day')
    def calculate_date(self):
        if self.issue_date and self.expected_received_date:
            d1=datetime.strptime(str(self.issue_date),'%Y-%m-%d') 
            d2=datetime.strptime(str(self.expected_received_date),'%Y-%m-%d')
            d3=d2-d1
            self.total_day= str(d3.days)








    def button_in_progress(self):
        _logger.info("~~~~~~~1~~~~~%r~~~~~~~~")
        pass

    def button_action_for_cancel(self):
        pass



    def  button_action_for_validate(self):
        self.state = 'allotment'
        self.active_hide_allot = True
        # return self.action_view_allotment_job_work()
   


    def button_action_for_cost_center(self):
        self.state = 'allotment'
        self.activate_inr = True
        self.active_hide_cost = False
        self.active_hide_gate = True
        return self.cost_center_view_action_open()

    def button_action_for_release(self):
        self.state = 'qa'
        self.active_qa = True
        self.active_release  = False
        quality_alert_team_id = self.env['quality.alert.team'].search([])
        quality_point_id = self.env['quality.point.test_type'].search([], limit=1)
        for job_work in self:
            if not job_work.team_id or not job_work.test_type_id:
                 raise UserError(_("Please select Team and Test Type"))  
            if not job_work.quality_check_ids:
                self.env["quality.check"].create({
                    "subcontractor_id" : job_work.subcontractor_id.id,
                    "product_id" : self.product_id.id,
                    "production_id" : self.mrp_production_id.id,
                    "test_type_id"  : job_work.test_type_id.id,
                    "team_id" : job_work.team_id.id,
                    "job_work_id" : job_work.id
                })
        pass

    # @api.model_create_multi
    # def create(self,vals):
    #     result = super(MrpJobWork,self).create(vals)
    #     for job_work in result:
    #         _logger.info("~~~~~~2~~~job_work~~~%r~~~~rec~~~----------------------------~",job_work )
    #         if not job_work.quality_check_ids:
    #             self.env["quality.check"].create({
    #                 "product_id" : self.product_id,
    #                 "production_id" : self.mrp_production_id
    #             })
    #         _logger.info("~~~~~~2~~~shivam~~~%r~~~~rec~~~----------------------------~",job_work )
    #         pass
    #         # if res:
    #         #     res.line_id = res.id
    #         #     res.warehouse_id = self.env.context.get('warehouse_id')
    #         #     res.shop_id = self.env.context.get('shop_id')
    #         # if res.product_ref and res.product_ref.startswith('='):
    #         #     res.product_ref = res.product_ref[2:]
    #         #     res.product_ref = res.product_ref[:-1]
    #     return result







    def view_tree_form_open_action(self):
        pass
        # return self.action_view_allotment_job_work() 





    def action_view_allotment_job_work(self):
        self.ensure_one() 
        return {
            'type': 'ir.actions.act_window',
            'name': _("Job Work"),
            'view_mode': 'form',
            # 'view_ids': [(self.env.ref('innorug_manufacture.view__mrp_job_work_form')).id],
            'res_model': 'mrp.job.work',
            'res_id': self.id,
            # 'nodestroy' : True,
            "target" : "current",
        }
 


    
    def button_action_for_allot_product(self):
        _logger.info("~~~~~~~1~~~~~%r~~~~~~~~", self.bom_id.operation_ids.workcenter_id)
        _logger.info("~~~~~~2~~~~~~%r~~~~~~~~", self.work_center_id)
        self.state = 'allotment'
        self.activate_product = True
        self.active_hide_allot = False
        self.active_hide_cost = True
        sub_allotment_id =self.env['subcontractor.alloted.product']
        mrp_routing_obj = self.env['mrp.routing.workcenter']
        for job_work in self:
            for raw_move in job_work.bom_id.operation_ids:
                if raw_move.workcenter_id == job_work.work_center_id:
                    mrp_routing_id = mrp_routing_obj.search([('workcenter_id','=', raw_move.workcenter_id.id),('bom_id','=', raw_move.bom_id.id)])
                    _logger.info("~~~~~~3~~~~~~%r~~~~~~~~",  mrp_routing_id.operation_component_ids)
                    for rec in mrp_routing_id.operation_component_ids:
                        sub_allotment_id = sub_allotment_id.search([('alloted_product_id','=', rec.product_id.id),('job_work_id','in', [job_work.id])])
                        if not sub_allotment_id:
                            sub_allotment_id =sub_allotment_id.create({
                                "parent_product_id" : job_work.product_id.id,
                                "alloted_product_id" : rec.product_id.id,
                                "alloted_quantity" : rec.product_qty * job_work.product_qty,
                                "amended_quantity": 0,
                                "consumed_quantity": 0,
                                "returned_quantity": 0,
                                "job_work_id": job_work.id,
                            })
                        else:
                            sub_allotment_id.alloted_quantity = rec.product_qty * job_work.product_qty
                            sub_allotment_id.parent_product_id = job_work.product_id
                            sub_allotment_id.job_work_id = job_work.id
        # return self.action_view_allotment_job_work()



    

    #########################
    # Cost Center View Action
    ########################

    def view_cost_centre_action(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_id': self.cost_center_id.id,
            'name': _("Cost center"),
            'view_mode': 'form',
            'res_model': 'mrp.cost.center',
            "target" : "new",
        }


    ########################
    #Action Button Cost Center
    ########################

    def cost_center_view_action_open(self):
        if self.subcontractor_id:
            if not self.cost_center_id:
                self.cost_center_id = self.cost_center_id.create({
                    "job_work_id": self.id,
                    "subcontractor_id": self.subcontractor_id,
                    "work_center_id" : self.work_center_id,
                    "product_id" : self.product_id ,
                    "mrp_production_id" : self.mrp_production_id,
                    "product_qty" : self. product_qty,
                     "issue_date" : self.issue_date , 
                     "expected_received_date" : self.expected_received_date,
                     "total_day" : self.total_day
                })
            else:
                if self.cost_center_id.work_center_id and self.cost_center_id.product_id :
                    if self.cost_center_id.subcontractor_id != self.subcontractor_id:
                        self.cost_center_id.subcontractor_id = self.subcontractor_id
                        self.cost_center_id.mrp_production_id  = self.mrp_production_id
                        self.cost_center_id.product_id  = self.product_id 
                        self.cost_center_id.product_qty  = self.product_qty
                        self.cost_center_id.issue_date  = self.issue_date 
                        self.cost_center_id.expected_received_date  = self.expected_received_date  
                        self.cost_center_id.total_day  = self.total_day      
                else:
                    self.cost_center_id.work_center_id = self.id
            _logger.info("~~~~~Assigned Cost Center~~~~~~~%r~~~~~~~~", self.cost_center_id)
        # return self.view_cost_centre_action()
        return self.action_view_allotment_job_work()


    def button_action_for_gate_pass(self):
        self.state = 'release'
        self.active_hide_gate = False
        self.active_release  = True
        return self.env.ref("innorug_manufacture.action_report_gate_pass_id").report_action(self)






class MrpStockMove(models.Model):
    _inherit = 'stock.move'



    job_work_id = fields.Many2one("mrp.job.work", string="Raw Components")


class SubBomlines(models.Model):
    _name = "subcontractor.alloted.product"
    _description = "Subcontractor Alloted Products"

    parent_product_id = fields.Many2one("product.product", string="Parent Product", readonly="1")
    alloted_product_id = fields.Many2one("product.product", string="Product", readonly="1")
    alloted_quantity = fields.Float("Alloted Quantity(Kg)", readonly="1")
    consumed_quantity = fields.Float("Consumed Quantity(Kg)")
    amended_quantity = fields.Float("Amended Qty(kg)")
    returned_quantity = fields.Float("Returned Quantity(kg)")

    job_work_id = fields.Many2one("mrp.job.work", "Job Work", readonly="1", invisible="1")
    # work_order_id = fields.Many2one("mrp.workorder", "Work Order")



    @api.onchange('returned_quantity')
    def product_consume_qty_descrese(self):
        for rec in self.job_work_id.mrp_production_id.move_raw_ids:
            _logger.info("~~~~~product product uom qty~~~~~~~%r~~~~~~~~", rec.product_uom_qty)
            if self.alloted_product_id == rec.product_id:
                rec.product_uom_qty -= self.returned_quantity


    
    @api.onchange('amended_quantity')
    def product_consume_qty_increase(self):
        for rec in self.job_work_id.mrp_production_id.move_raw_ids:
            _logger.info("~~~~~product product uom qty~~~~~~~%r~~~~~~~~", rec.product_uom_qty)
            if self.alloted_product_id == rec.product_id:
                rec.product_uom_qty += self.amended_quantity




    






    