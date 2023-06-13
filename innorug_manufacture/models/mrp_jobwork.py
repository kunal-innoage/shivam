from odoo import fields, models, _,api
from datetime import datetime
from odoo.exceptions import UserError, ValidationError, MissingError
import logging
_logger = logging.getLogger(__name__)


class MrpJobWork(models.Model):
    _name = "mrp.job.work"
    _description = 'Job Work'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = "product_id"

    name = fields.Char("Job Work")

    
    product_id = fields.Many2one(related="mrp_production_id.product_id", string="Product")
    bom_id = fields.Many2one(related="mrp_work_order_id.production_bom_id", string="Bill Of Material")
    
    product_qty = fields.Float("Quantity(Units)")
    qty_production = fields.Float('Original Production Quantity', readonly=True, related='mrp_production_id.product_qty')
    remaining_qty = fields.Float(string="Remaining Quantity", default= 0.0, tracking = True)

    mrp_work_order_id = fields.Many2one("mrp.workorder", "Work Order")

    mrp_production_id = fields.Many2one(related="mrp_work_order_id.production_id", string="MRP Production")
    product_id = fields.Many2one(related="mrp_work_order_id.product_id", string="MRP Production")
    manager_id = fields.Many2one(related="mrp_work_order_id.manager_id", string="Manager")

    subcontractor_id = fields.Many2one('res.partner', string='Subcontractors', tracking=True)
    cost_center_id = fields.Many2one("mrp.cost.center", "Cost Center")




    #o2msubcontracter_alloted_product_ids
    subcontracter_alloted_product_ids = fields.One2many("subcontractor.alloted.product", "job_work_id", "Alloted Material")




    # issue_date = fields.Datetime(related="mrp_work_order_id.date_planned_start", string="Issue Date", readonly=False)
    issue_date = fields.Date(string='Issued Date', tracking = True)
    expected_received_date = fields.Date(string='Expected Date' , tracking = True)
    total_day = fields.Integer(string='Total')



    work_center_id = fields.Many2one(related='mrp_work_order_id.workcenter_id', string="Work Center")
    

    cost_center_ids = fields.One2many("mrp.cost.center", "job_work_id", "Cost Center")

    #Boolean fields
    activate_inr = fields.Boolean("Activate INR")
    activate_product = fields.Boolean("Activate Product")
    active_hide_allot = fields.Boolean("Hide Details product")
    active_hide_cost = fields.Boolean("Hide Details Cost")
    active_hide_qa = fields.Boolean("Hide Details QA Button")
    active_release = fields.Boolean("QA")
    active_qa = fields.Boolean("QA")
    active_baazar = fields.Boolean("BAAZAR")
    active_baazar_page = fields.Boolean("active_baazar_page")
    active_report_back_order = fields.Boolean("Active Report Back Order")
    active_no_amended = fields.Boolean("amended")
    active_no_return = fields.Boolean("return")
    active_done = fields.Boolean("done")
    active_done_state = fields.Boolean("Active Done")
    active_cancel = fields.Boolean("cancel")
    active_force_qa = fields.Boolean("force")


    #Gate Pass
    warehouse = fields.Char("Warehouse")
    reference = fields.Char(string="Reference No")
    remarks =fields.Text( string="Remarks")


    #Quality Control relation
    quality_check_ids = fields.One2many("quality.check","job_work_id", string="Quality Check")
    team_id =fields.Many2one("quality.alert.team", "Team")
    test_type_id = fields.Many2one("quality.point.test_type","Test Type")
    
    
    #quality control relation
    quality_control_ids = fields.One2many("mrp.quality.control","job_work_id", string="Quality Check")
    
    


    

    state = fields.Selection([
        ('draft','DRAFT'),
        ('allotment','WAITING COMPONENTS'),
        ('release','RELEASE'),
        ('qa','PROCESS QC'),
        ('waiting_baazar','WAITING BAAZAR'),
        ('baazar','BAAZAR'),
        ('fqa','FINAL QC'),
        ('done','RECEIVED'),
        ('cancel','CANCEL')
        ], string='Status', default='draft')


    # allotment_product_ids = fields.One2many("stock.move", "job_work_id", string="Allotment Product")
    


    #Baazar Details for receive product
    baazar_details = fields.Char("Bazar Details")
    total_weight = fields.Float("Total Weight")
    total_receive_product_qty = fields.Integer("Total Receive Quantity", tracking = True)
    pending__product_qty = fields.Integer("Pending Quantity") 
    total__receive_weight = fields.Float("Receive Weight") 


    #original details of product
    design = fields.Char("Design", readonly="1")
    area = fields.Float("Area", readonly="1")
    size = fields.Char("Product Size Name", readonly="1")
    perimeter = fields.Float("Perimeter", readonly="1")
    shape = fields.Char("Shape", readonly="1")
    lenght_fraction = fields.Float("Length Fraction", readonly="1")
    size_type = fields.Selection([
        ('standard','Standard'),
        ('manufaturing_size','Manufaturing Size'),
        ('finishing_size','Finishing Size'),
        ('stencil','Stencil'),
        ('map','Map')
        ], string='Product Size Type', readonly="1")



    #Actual details of product
    actual_weight = fields.Float("Actual Weight")
    actual_design = fields.Char("Actual Design")
    actual_area = fields.Float("Actual Area")
    actual_size = fields.Char("Actual Product Size Name")
    actual_perimeter = fields.Float( "Actual Perimeter")
    actual_shape = fields.Char("Actual Shape")
    # size_type = fields.Char("Size Type")
    actual_lenght_fraction = fields.Float("Actual Length Fraction")

    actual_size_type = fields.Selection([
        ('standard','Standard'),
        ('manufaturing_size','Manufaturing Size'),
        ('finishing_size','Finishing Size'),
        ('stencil','Stencil'),
        ('map','Map')
        ], string=' Actual Product Size Type')



    #Day Calculate
    @api.onchange('issue_date', 'expected_received_date','total_day')
    def calculate_date(self):
        if self.issue_date and self.expected_received_date:
            d1=datetime.strptime(str(self.issue_date),'%Y-%m-%d') 
            d2=datetime.strptime(str(self.expected_received_date),'%Y-%m-%d')
            d3=d2-d1
            self.total_day= str(d3.days)
    
  



    @api.onchange('total_receive_product_qty')
    def calculate_pending_qty(self):
        if self.total_receive_product_qty <= self.product_qty :
            self.pending__product_qty = self.product_qty - self.total_receive_product_qty 
            # w =0
            if self.product_qty >0:
                w = self.total_weight / self.product_qty
                self.total__receive_weight = w * self.total_receive_product_qty
            if self.pending__product_qty > 0 :
                self.active_report_back_order = True
            else:
                self.active_report_back_order = False
        else:
            raise UserError(_("Please enter valid receive qty "))  




    def button_action_for_back_order_report(self):
        pass

    def button_action_for_done(self):
        self.state = 'done'
        self.subcontracter_alloted_product_ids.activate_return_qty = True
        self.active_done = False
        self.subcontracter_alloted_product_ids.activate_return =False
        self.active_cancel = False
        pass
    
    
    def button_action_for_force_qa(self):
        self.active_force_qa = False
        for rec in self.quality_check_ids:
            rec.do_pass()
        pass



   

    def button_action_for_no_amended_qty(self):
        self.subcontracter_alloted_product_ids.activate_amended_qty = True
        self.subcontracter_alloted_product_ids.activate_amended = False
        self.active_no_amended =False
        self.active_hide_qa =True
        pass



    def button_action_for_no_return_qty(self):
        self.subcontracter_alloted_product_ids.activate_return_qty = True
        self.subcontracter_alloted_product_ids.activate_return  = False
        self.active_no_return = False
        self.active_done =  True
        pass 






    def button_in_progress(self):
        _logger.info("~~~~~~~1~~~~~%r~~~~~~~~")
        pass






    def button_action_for_cancel(self):
        pass





    def  button_action_for_validate(self):
        self.state = 'allotment'
        self.active_hide_allot = True
        # return self.action_view_allotment_job_work()




    def button_action_for_baazar(self):
        self.state = 'baazar'
        self.subcontracter_alloted_product_ids.activate_return  = True
        self.active_no_return  = True
        self.active_baazar =  False
        self.active_hide_qa = False
        for rec in self.subcontracter_alloted_product_ids:
                self.total_weight += rec.total_allot_qty
        self.active_baazar_page =  True
        pass
   


    def button_action_for_cost_center(self):
        self.state = 'allotment'
        self.activate_inr = True
        self.active_hide_cost = False
        self.active_release  = True
        return self.cost_center_view_action_open()
    

    def button_action_for_release(self):
        self.state = 'release'
        self.subcontracter_alloted_product_ids.activate_amended = True
        self.active_no_amended = True
        self.active_release  = False
        
        




    def button_action_for_qa_process(self):
        self.state = 'qa'
        self.active_qa = True
        self.active_hide_qa = False
        self.active_no_amended = False
        self.active_force_qa = True
        self.active_baazar = False
        self.subcontracter_alloted_product_ids.activate_amended_qty = True
        self.subcontracter_alloted_product_ids.activate_amended = False
        self.subcontracter_alloted_product_ids.activate_consume_qty = True
        for rec in self.subcontracter_alloted_product_ids:
            if rec.returned_quantity == 0:
                rec.consumed_quantity = rec.total_allot_qty
        for job_work in self:
            if not job_work.team_id or not job_work.test_type_id:
                 raise UserError(_("Please select Team and Test Type"))  
            qlty_check_id = self.env["quality.check"].create({
                "subcontractor_id" : job_work.subcontractor_id.id,
                "product_id" : self.product_id.id,
                "production_id" : self.mrp_production_id.id,
                "test_type_id"  : job_work.test_type_id.id,
                "team_id" : job_work.team_id.id,
                "job_work_id" : job_work.id
            })
            if qlty_check_id:
                job_work.quality_check_ids += qlty_check_id
                
            qlty_control_id = self.env["mrp.quality.control"].create({
                "subcontractor_id" : job_work.subcontractor_id.id,
                "product_id" : self.product_id.id,
                "production_id" : self.mrp_production_id.id,
                "operation_id" : self.work_center_id.id,
                "job_work_id" : job_work.id
            })
            if qlty_control_id:
                job_work.quality_control_ids += qlty_control_id            
        pass





    def view_tree_form_open_action(self):
        pass





    def action_view_allotment_job_work(self):
        self.ensure_one() 
        return {
            'type': 'ir.actions.act_window',
            'name': _("Job Work"),
            'view_mode': 'form',
            # 'view_ids': [(self.env.ref('innorug_manufacture.view__mrp_job_work_form')).id],
            'res_model': 'mrp.job.work',
            'res_id': self.id,
            "target" : "current",
        }
 


    
    def button_action_for_allot_product(self):
        self.state = 'allotment'
        self.activate_product = True
        self.active_hide_allot = False
        self.active_hide_cost = True
        sub_allotment_id =self.env['subcontractor.alloted.product']
        mrp_routing_obj = self.env['mrp.routing.workcenter']
        mrp_product_obj =self.env["product.template"]
        for job_work in self:
            for raw_move in job_work.bom_id.operation_ids:
                if raw_move.workcenter_id == job_work.work_center_id:
                    mrp_routing_id = mrp_routing_obj.search([('workcenter_id','=', raw_move.workcenter_id.id),('bom_id','=', raw_move.bom_id.id)])
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
                                'total_allot_qty' :  rec.product_qty * job_work.product_qty,
                                'product_uom' : rec.product_uom_id.id,
                                "job_work_id": job_work.id,
                            })
                        else:
                            sub_allotment_id.alloted_quantity = rec.product_qty * job_work.product_qty
                            sub_allotment_id.parent_product_id = job_work.product_id
                            sub_allotment_id.job_work_id = job_work.id
            product_id = mrp_product_obj.search([('id','=', job_work.product_id.id)])
            if product_id :
                job_work.design = product_id.design
                job_work.area = product_id.area
                job_work.size = product_id.size
                job_work.perimeter = product_id.perimeter
                job_work.shape = product_id.shape
                job_work.lenght_fraction =  product_id.lenght_fraction
                job_work.size_type =  product_id.size_type
                




    

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
        return self.action_view_allotment_job_work()


        


    # def button_action_for_gate_pass(self):
    #     self.state = 'release'
    #     self.active_hide_gate = False
    #     self.active_release  = True
    #     return self.env.ref("innorug_manufacture.action_report_gate_pass_id").report_action(self)






class MrpStockMove(models.Model):
    _inherit = 'stock.move'



    job_work_id = fields.Many2one("mrp.job.work", string="Raw Components")






class SubBomlines(models.Model):
    _name = "subcontractor.alloted.product"
    _description = "Subcontractor Alloted Products"

    parent_product_id = fields.Many2one("product.product", string="Parent Product", readonly="1")
    alloted_product_id = fields.Many2one("product.product", string="Product", readonly="1")
    alloted_quantity = fields.Float("Alloted Quantity", readonly="1")
    consumed_quantity = fields.Float("Consumed Quantity")
    amended_quantity = fields.Float("Amended Qty")
    total_allot_qty = fields.Float("Total Allote Qty")
    returned_quantity = fields.Float("Returned Quantity")
    product_uom =  fields.Many2one("uom.uom",string="UOM")

    job_work_id = fields.Many2one("mrp.job.work", "Job Work", readonly="1", invisible="1")
    state = fields.Selection(related="job_work_id.state")


    # work_order_id = fields.Many2one("mrp.workorder", "Work Order")

    #Boolean fields details 
    activate_return = fields.Boolean("return")
    activate_consume = fields.Boolean("consume")
    activate_amended = fields.Boolean("amended")
    activate_return_qty = fields.Boolean("rrqty")
    activate_consume_qty = fields.Boolean("cqty")
    activate_amended_qty = fields.Boolean("aqty")



    #calculate total qty
    @api.onchange('amended_quantity')
    def calculate_total_qty(self):
        if self.amended_quantity > 0:
            self.total_allot_qty = 0
            self.total_allot_qty = self.alloted_quantity + self.amended_quantity
        
    
    #calculate consume qty
    @api.onchange('returned_quantity')
    def calculate_consume_qty(self):
        if self.returned_quantity > 0 and self.returned_quantity <= self.total_allot_qty:
            self.consumed_quantity = 0
            self.consumed_quantity = self.total_allot_qty - self.returned_quantity
        else:
            raise UserError(_("Please check return weight"))  




    def button_action_for_return(self):
        self.job_work_id.active_no_return  = False 
        self.job_work_id.active_done =  True
        self.activate_return_qty = True
        self.activate_return = False
        if self.returned_quantity == 0 :
            self.consumed_quantity = self.total_allot_qty
      

    def button_action_for_consume(self):
        pass


    def button_action_for_amended(self):
        self.job_work_id.active_no_amended  = False 
        self.job_work_id.active_hide_qa =True
        self.activate_amended_qty = True
        self.activate_amended  = False
        self.total_allot_qty = 0
        self.total_allot_qty = self.alloted_quantity + self.amended_quantity
        if self.returned_quantity == 0 :
            self.consumed_quantity = self.total_allot_qty
        _logger.info("~~~~~~2~~~job_work~~~%r~~~~rec~~~----------------------------~", self.activate_consume_qty)
        pass
    



    # @api.onchange('returned_quantity')
    # def product_consume_qty_descrese(self):
    #     for rec in self.job_work_id.mrp_production_id.move_raw_ids:
    #         _logger.info("~~~~~product product uom qty~~~~~~~%r~~~~~~~~", rec.product_uom_qty)
    #         if self.alloted_product_id == rec.product_id:
    #             rec.product_uom_qty -= self.returned_quantity


    
    # @api.onchange('amended_quantity')
    # def product_consume_qty_increase(self):
    #     for rec in self.job_work_id.mrp_production_id.move_raw_ids:
    #         _logger.info("~~~~~product product uom qty~~~~~~~%r~~~~~~~~", rec.product_uom_qty)
    #         if self.alloted_product_id == rec.product_id:
    #             rec.product_uom_qty += self.amended_quantity




    






    