from odoo import fields, models, _,api
from datetime import datetime 
from odoo.exceptions import UserError, ValidationError, MissingError
import logging
_logger = logging.getLogger(__name__)


class MrpJobWork(models.Model):
    _name = "mrp.job.work"
    _description = 'Job Work'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = "name"

    
    name = fields.Char(string='Order Reference', required=True,
                          readonly=True, default=lambda self: _('New'))
    # reference_no = fields.Char(string='Order Reference', required=True,
    #                       readonly=True, default=lambda self: _('New'))
    
    original_product_qty = fields.Float("Original Product Qty")  # use for job work allotement
    
    product_id = fields.Many2one(related="mrp_production_id.product_id", string="Product")
    bom_id = fields.Many2one(related="mrp_work_order_id.production_bom_id", string="Bill Of Material")
    
    product_qty = fields.Float("Quantity(Units)")
    qty_production = fields.Float('Original Production Quantity', readonly=True, related='mrp_production_id.product_qty')
    alloted_qty_production = fields.Float('Alloted Production Quantity', readonly=True, related='mrp_production_id.product_qty')
    remaining_qty = fields.Float(string="Remaining Quantity", default= 0.0, tracking = True)

    mrp_work_order_id = fields.Many2one("mrp.workorder", "Work Order")

    mrp_production_id = fields.Many2one(related="mrp_work_order_id.production_id", string="MRP Production")
    product_id = fields.Many2one(related="mrp_work_order_id.product_id", string="MRP Production")
    manager_id = fields.Many2one(related="mrp_work_order_id.manager_id", string="Manager")

    subcontractor_id = fields.Many2one('res.partner', string='Subcontractors', tracking=True)
    cost_center_id = fields.Many2one("mrp.cost.center", "Cost Center")
    
    main_jobwork_id = fields.Many2one("main.jobwork", string= "Main Job Work")
    



    #o2msubcontracter_alloted_product_ids
    subcontracter_alloted_product_ids = fields.One2many("subcontractor.alloted.product", "job_work_id", "Alloted Material")


    division = fields.Selection([
        ('kelim','KELIM'),
        ('knotted','KNOTTED'),
        ('main','MAIN'),
        ('sample','SAMPLE'),
        ('shag','SHAG'),
        ('tufted','TUFTED')
        ], string='Division')



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
    active_qty_cnf = fields.Boolean("cnf")
    active_qty_add = fields.Boolean("cnf")
    active_qty_product = fields.Boolean("act")
    active_components_allote = fields.Boolean("line")
    active_org_qty_product = fields.Boolean("Org Qty")


    #Gate Pass
    warehouse = fields.Char("Warehouse")
    reference = fields.Char(string="Reference No")
    remarks =fields.Text( string="Remarks")


    jobwork_allotment_id = fields.Many2one("jobwork.allotment", "Job work allotement")
    
    
    #quality control relation
    quality_control_ids = fields.One2many("mrp.quality.control","job_work_id", string="Quality Check")
    qc_manager_id = fields.Many2one('res.partner', string="QC Manager")
    
    
    #Baazar Product Lines relation
    baazar_product_lines_ids = fields.One2many("mrp.baazar.product.lines","job_work_id", string="Baazar product Details")
    
    


    

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
    total_receive_product_qty = fields.Integer("Total Received Quantity", tracking = True)
    pending_product_qty = fields.Integer("Pending Quantity") 
    total_receive_weight = fields.Float("Expected Receive Weight") 


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
    
    
    def add_qty(self):
        self.active_qty_product = True
        self.active_qty_add = False
        self.active_qty_cnf = True
        self.main_jobwork_id.active_sub = True 
        # return self.get_action_main_branch()
    
    
    def confirm_qty(self):
        if self.product_qty > self.original_product_qty:
            raise UserError(_("Max Alloted Qty "))   
        self.active_qty_cnf = False
        self.active_org_qty_product = False
        
        return  self.calculate_remaining_qty()
    
    
    
    def calculate_remaining_qty(self):
        job_allote_obj =self.env["jobwork.allotment"]  
        if self.jobwork_allotment_id:
            job_allote_id = job_allote_obj.search([('id','=',self.jobwork_allotment_id.id)])
            if job_allote_id:
                    job_allote_id.remaining_product_qty = job_allote_id.remaining_product_qty - self.product_qty
                    job_allote_id.alloted_product_qty += self.product_qty
                    if job_allote_id.alloted_product_qty == job_allote_id.product_qty:
                        job_allote_id.allotment = "full"  
                    elif(job_allote_id.alloted_product_qty > 0 and job_allote_id.alloted_product_qty < job_allote_id.product_qty):
                         job_allote_id.allotment = "partial"
                    else:
                        job_allote_id.allotment = "to_do"  
                     
        # return self.get_action_main_branch()
    
    def button_action_for_open_job_work(self):
        return self.action_view_allotment_job_work()
                
                
                
                
                
    def get_action_main_branch(self):   # not use this action     
        return {
            'type': 'ir.actions.act_window',
            'name': _("Main Job Work"),
            'view_mode': 'form',
            'res_model': 'main.jobwork',
            'res_id': self.main_jobwork_id.id,
            "target" : "new",
        }   
        
        
    
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'mrp.job.work') or _('New')
        res = super(MrpJobWork, self).create(vals)
        return res



    #Day Calculate
    @api.onchange('issue_date', 'expected_received_date','total_day')
    def calculate_date(self):
        if self.issue_date and self.expected_received_date:
            d1=datetime.strptime(str(self.issue_date),'%Y-%m-%d') 
            d2=datetime.strptime(str(self.expected_received_date),'%Y-%m-%d')
            d3=d2-d1
            self.total_day= str(d3.days)
    
  



    # @api.onchange('total_receive_product_qty')
    def calculate_pending_qty(self):
        self.pending_product_qty = 0
        if self.total_receive_product_qty <= self.product_qty :
            self.pending_product_qty = self.product_qty - self.total_receive_product_qty 
            if self.product_qty >0:
                w = self.total_weight / self.product_qty
                self.total_receive_weight = w * self.total_receive_product_qty
            if self.pending_product_qty > 0 :
                self.active_report_back_order = True
            else:
                self.active_report_back_order = False
        else:
            raise UserError(_("Please enter valid receive qty "))  
        
        
                    
        
    @api.onchange('baazar_product_lines_ids')
    def get_recieve_details(self):
        for work_order in self:
            t = 0
            last_job_order = False
            for rec in work_order.baazar_product_lines_ids:
                t =  rec.receive_product_qty
                last_job_order = rec
            if t > self.pending_product_qty:
                if last_job_order:
                    last_job_order.unlink()
           
    
    
    
    
        
        
    # @api.onchange('baazar_product_lines_ids')   
    def calculate_total_receive_product_qty(self):
        self.total_receive_product_qty = 0
        for rec in self.baazar_product_lines_ids:
            self.total_receive_product_qty += rec.accepted_qty
        self.pending_product_qty = 0
        self.pending_product_qty = self.product_qty - self.total_receive_product_qty 
        self.total_receive_weight = 0
        if self.product_qty >0:
                w = self.total_weight / self.product_qty
                self.total_receive_weight = w * self.total_receive_product_qty
        




    def button_action_for_back_order_report(self):
        pass

    def button_action_for_done(self):
        self.message_post(body= "DONE - RECEIVED")
        self.state = 'done'
        self.subcontracter_alloted_product_ids.activate_return_qty = True
        self.active_done = False
        self.subcontracter_alloted_product_ids.activate_return =False
        self.active_cancel = False
        for rec in self.subcontracter_alloted_product_ids:
            if not rec.activate_confirm_return :
                pass
            else:
                raise UserError(_("Please confirm return Qty")) 
        pass
    
    
    def button_action_for_force_qa(self):
        self.active_force_qa = False
        for rec in self.quality_control_ids:
            rec.do_pass_qc()
        today = datetime.today()
        subject="QC FORCE : "
        self.message_post(body=subject + str(today))
        pass



   

    def button_action_for_no_amended_qty(self):
        self.message_post(body= "NO AMENDED QUANTITY")
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
        for rec in self.subcontracter_alloted_product_ids:
            if not rec.activate_confirm_return :
                pass
            else:
                raise UserError(_("Please confirm return Qty")) 
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
        self.pending_product_qty = self.product_qty
        self.message_post(body= "Baazar Process Activated")
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
        # for rec in self.mrp_work_order_id.job_work_lines_ids:
        #     if rec.subcontractor_id.id == self.subcontractor_id.id:
        #          _logger.info("~~~~~~2~~~job_work~~~%r~~~~rec~~~-----------------recccccccccccccccccccccccccccccc---ee--------~", rec.subcontracter_alloted_product_ids)
        #          for line in  rec.subcontracter_alloted_product_ids:
        #             product_line_id = self.env["subcontractor.alloted.product"].create({   #for cost line code
        #                 "alloted_product_id" : line.alloted_product_id.id,
        #                 "alloted_quantity" : line.alloted_quantity,
        #                 "amended_quantity" : line.amended_quantity,
        #                 "consumed_quantity": line.consumed_quantity,
        #                 "returned_quantity": line.returned_quantity,
        #                 'total_allot_qty' :  line.total_allot_qty,
        #                 'product_uom' : line.product_uom.id,
        #                 "job_work_id": self.id,
        #             })
                    # if product_line_id:
                    #     self.cost_center_id.product_allotement_ids +=  product_line_id  
                    
                
            
        
        
        




    def button_action_for_qa_process(self):
        self.message_post(body= "QC Process Activated")
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
            if not rec.activate_confirm_amended :
                if rec.returned_quantity == 0:
                    rec.consumed_quantity = rec.total_allot_qty
            else:
                raise UserError(_("Please confirm Amended Qty"))      
        for job_work in self:  
            if not job_work.qc_manager_id:
                 raise UserError(_("Please select QC Manager"))    
            qlty_control_id = self.env["mrp.quality.control"].create({
                "subcontractor_id" : job_work.subcontractor_id.id,
                "product_id" : self.product_id.id,
                "production_id" : self.mrp_production_id.id,
                "operation_id" : self.work_center_id.id,
                "qc_manager_id" : self.qc_manager_id.id,
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
        _logger.info("~~~~~~~ jobwork_allotment_id~~~%r~~~~~~~~",self.jobwork_allotment_id)
        
        if  self.active_qty_cnf ==  True:
            raise UserError(_("Please confirm Qty"))
        self.active_org_qty_product = False
        self.message_post(body= str(self.mrp_work_order_id.name) + " Material Issued")
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

    def action_view_cost_center_form(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_id': self.cost_center_id.id,
            'name': _("Cost center"),
            'view_mode': 'form',
            'res_model': 'mrp.cost.center',
            "target" : "current",
        }


    ########################
    #Action Button Cost Center
    ########################

    def cost_center_view_action_open(self):
        self.message_post(body= "Generated Cost Center")
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
        # return self.action_view_allotment_job_work()
        # return self.action_view_cost_center_form()


        


    # def button_action_for_gate_pass(self):
    #     self.state = 'release'
    #     self.active_hide_gate = False
    #     self.active_release  = True
    #     result = self.env.ref("innorug_manufacture.action_report_gate_pass_id").report_action(self)
    #     import pdb;pdb.set_trace()






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
    main_job_work_id = fields.Many2one("main.jobwork", "Main Job Work")
    state = fields.Selection(related="job_work_id.state")


    # work_order_id = fields.Many2one("mrp.workorder", "Work Order")
    
    cost_center_id = fields.Many2one("mrp.cost.center", string="Cost Center")

    #Boolean fields details 
    activate_return = fields.Boolean("return")
    activate_consume = fields.Boolean("consume")
    activate_amended = fields.Boolean("amended")
    activate_return_qty = fields.Boolean("rrqty")
    activate_consume_qty = fields.Boolean("cqty")
    activate_amended_qty = fields.Boolean("aqty")
    activate_confirm_amended = fields.Boolean('aca')
    activate_confirm_return = fields.Boolean("acr")



    #calculate total qty
    def button_calculate_total_qty(self):
        self.activate_confirm_amended = False
        self.job_work_id.active_hide_qa =True
        if self.amended_quantity > 0:
            # self.job_work_id.message_post(body= "PROCESS QC PASS")
            self.total_allot_qty = 0
            self.total_allot_qty = self.alloted_quantity + self.amended_quantity
            self.job_work_id.message_post(body = str(self.alloted_product_id.name) + " amended by "+ (str(self.amended_quantity) + str(self.product_uom.name)))
        
    

    def button_action_for_confim_return(self):
        self.activate_confirm_return = False
        self.job_work_id.active_done =  True
        if self.returned_quantity > 0 and self.returned_quantity <= self.total_allot_qty:
            self.consumed_quantity = 0
            self.consumed_quantity = self.total_allot_qty - self.returned_quantity
            self.job_work_id.message_post(body = str(self.alloted_product_id.name) + " returned by "+ (str(self.returned_quantity) + str(self.product_uom.name)))
        else:
            raise UserError(_("Please check return weight"))  




    def button_action_for_return(self):
        self.activate_confirm_return = True
        # self.job_work_id.active_no_return  = False 
        self.activate_return_qty = True
        self.activate_return = False
        if self.returned_quantity == 0 :
            self.consumed_quantity = self.total_allot_qty
      

    def button_action_for_consume(self):
        pass


    def button_action_for_amended(self):
        self.job_work_id.active_no_amended  = False 
        self.activate_amended_qty = True
        self.activate_amended  = False
        self.total_allot_qty = 0
        self.activate_confirm_amended = True
        self.total_allot_qty = self.alloted_quantity + self.amended_quantity
        # if self.returned_quantity == 0 :
        #     self.consumed_quantity = self.total_allot_qty
        # _logger.info("~~~~~~2~~~job_work~~~%r~~~~rec~~~----------------------------~", self.activate_consume_qty)
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




    






    