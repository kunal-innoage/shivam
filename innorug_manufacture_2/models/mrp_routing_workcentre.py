from odoo import fields, models, _
import logging
_logger = logging.getLogger(__name__)


class MrpBomData(models.Model):
    _inherit = 'mrp.routing.workcenter'


    def get_bom_components(self):
        products = self.env['product.product']
        for operation in self:
            if operation.bom_id:
                for line in operation.bom_id.bom_line_ids:
                    products += line.product_id
            self.bom_component_ids = products
        return products


    operation_component_ids = fields.One2many("bom.operation.component", "operation_routing_id", string="Alloted Components")
    bom_component_ids = fields.One2many("product.product", string="BOM Components", compute="get_bom_components")


    def view_action_bom_materials_allotments(self):
        self.ensure_one()  
        return {
            'type': 'ir.actions.act_window',
            'name': _("Operation Components"),
            'view_mode': 'list',
            'res_model': 'bom.operation.component',
            'context': {'create': False},
            'domain': [('workcenter_id','=',self.id)]
        }


  