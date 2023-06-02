from odoo import fields, models, _, api
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class MrpWorkOrder(models.Model):
    _inherit = 'sale.order'



