# -*- coding: utf-8 -*-
from odoo import models, fields, _, api

import logging
_logger = logging.getLogger(__name__)



class SuryaSaleOrder(models.Model):
    _name = 'surya.excel.sale.order'
    _description = 'Surya Sale Order'


    name =fields.Char("Name")
    address= fields.Char("Address")
    country = fields.Char("Country")
    mobile = fields.Char("Mobile")
    email = fields.Char("Email")
    quantity = fields.Char("Quantity")
    product = fields.Char("Product")
    order_date = fields.Char("OrderDate")
    due_date = fields.Char("DueDate")
    rate = fields.Float("Rate")
    buyer_up_code = fields.Char("BuyerUpcCode")
    order_no = fields.Char("Order No")


    partner_id =  fields.Many2one("res.partner", "Customer")
    sale_order_id = fields.Many2one("sale.order", "Sale Order", readonly=True)
    product_id = fields.Many2one("product.product", "Product", readonly=True)
    



    @api.model_create_multi
    def create(self, vals):
        res = super(SuryaSaleOrder, self).create(vals)
        if res._context['import_file']:
            for order in res:
                customer_id = self.env['res.partner']
                customer_id = customer_id.search([('name', '=', order.name)],  limit=1)
                if customer_id:
                    order.partner_id = customer_id
                if order.product:
                    order.product_id = self.env['product.product'].search([('name', 'in', [order.product])])
        return res
    


    def map_with_bulk_order_record(self):
        sale_order_obj = self.env["sale.order"]
        for order in self:
            if int(order.quantity) != 0 and order.product_id:
                order_id = sale_order_obj.search([('partner_id', '=', order.name)])
                if not order_id:
                    customer_id, billing_id, shipping_id = self._get_customer_details(order)
                    so_line =[]
                    so_line += [(0, 0, {
                            'product_id': order.product_id.id,
                            'product_uom_qty': order.quantity,
                        })]
                    _logger.info("~~~~~~~~~so_line~~~~%r~~~~~~", so_line)
                    sale_order_id = sale_order_obj.create({
                        'partner_id': customer_id.id,
                        'partner_invoice_id': billing_id.id,
                        'partner_shipping_id': shipping_id.id,
                        'order_line': so_line,
                    })
                    _logger.info("~~~~~~~~~order_id~~~~%r~~~~~~", order_id)
                    order.sale_order_id = sale_order_id
                else:
                    if order.product_id:
                        self.env["sale.order.line"].create({
                            'product_id': order.product_id.id,
                            'product_uom_qty': order.quantity,
                            'order_id': order_id.id,
                        })
                    order.sale_order_id = order_id


        



    
    

    # def map_with_bulk_order_record(self):
    #     sale_order_obj = self.env["sale.order"]
    #     list_order_no = self.order_list_details()
    #     dict_details =self.dict_details(list_order_no)
    #     print("________________",  dict_details )
    #     for order in self:
    #         if order.order_no in list_order_no:
    #             if int(order.quantity) != 0 and order.product_id:
    #                 order_id = sale_order_obj.search([('partner_id', '=', order.name)])
    #                 if not order_id :
    #                     customer_id, billing_id, shipping_id = self._get_customer_details(order)
    #                     so_line =[]
    #                     product_d = self.env['product.product'].search([('name', 'in', [order.product])])
    #                     so_line += [(0, 0, {
    #                             'product_id': order.product_id.id,
    #                             'product_uom_qty': order.quantity,
    #                         })]
    #                     _logger.info("~~~~~~~~~so_line~~~~%r~~~~~~", so_line)
    #                     sale_order_id = sale_order_obj.create({
    #                         'partner_id': customer_id.id,
    #                         'partner_invoice_id': billing_id.id,
    #                         'partner_shipping_id': shipping_id.id,
    #                         'order_line': so_line,
    #                     })
    #                     _logger.info("~~~~~~~~~order_id~~~~%r~~~~~~", order_id)
    #                     order.sale_order_id = sale_order_id
    #                 elif order_id: 
    #                         customer_id, billing_id, shipping_id = self._get_customer_details(order)
    #                         so_line =[]
    #                         product_d = self.env['product.product'].search([('name', 'in', [order.product])])
    #                         so_line += [(0, 0, {
    #                                 'product_id': order.product_id.id,
    #                                 'product_uom_qty': order.quantity,
    #                             })]
    #                         _logger.info("~~~~~~~~~so_line~~~~%r~~~~~~", so_line)
    #                         sale_order_id = sale_order_obj.create({
    #                             'partner_id': customer_id.id,
    #                             'partner_invoice_id': billing_id.id,
    #                             'partner_shipping_id': shipping_id.id,
    #                             'order_line': so_line,
    #                         })
    #                         _logger.info("~~~~~~~~~order_id~~~~%r~~~~~~", order_id)
    #                         order.sale_order_id = sale_order_id

                    
    #                 else:
    #                     if order.product_id:
    #                         self.env["sale.order.line"].create({
    #                             'product_id': order.product_id.id,
    #                             'product_uom_qty': order.quantity,
    #                             'order_id': order_id.id,
    #                         })
    #                     order.sale_order_id = order_id
    #                     print("------------------",order.sale_order_id)


  
    # def dict_details(self, order_list):
    #     group= {}
    #     list_or = []
    #     for order_no in order_list:
    #         product_list =[]
    #         for order in self:
    #             if order.order_no == order_no:
    #                 product_list.append(order.product)
    #         group = {order_no : product_list}
    #         list_or.append(group)
    #     return list_or

    

    # def order_list_details(self):
    #     order_list = []
    #     for val in self:
    #         order_list.append(val.order_no)
    #         mySet = set(order_list)
    #     order_list = list(mySet)
    #     return  order_list


    

    def _get_customer_details(self, order):
        customer_env = self.env['res.partner']
        customer = customer_env.search([('name','=',order.name)],limit=1)

        if not customer:
            customer = customer_env.create({
                'company_type': 'person',
                'name': order.name,
                'country_id': self.env['res.country'].search([('code','=', order.country)],limit=1).id,
            })
          
            billing_customer = customer_env.create({
                'company_type': 'person',
                'type': 'invoice',
                'parent_id': customer.id,
                'name': order.name,
                'country_id': self.env['res.country'].search([('code','=', order.country )],limit=1).id,
            })
           
            shipping_customer = customer_env.create({
                'company_type': 'person',
                'type': 'delivery',
                'parent_id': customer.id,
                'name': order.name,
                'country_id': self.env['res.country'].search([('code','=', order.country )],limit=1).id,
            })
        else:
            billing_customer = customer_env.search([('type','=','invoice'),('parent_id', '=', customer.id)])
            shipping_customer = customer_env.search([('type','=','delivery'),('parent_id', '=', customer.id)])

        return [customer, billing_customer, shipping_customer]


    
    
   

   