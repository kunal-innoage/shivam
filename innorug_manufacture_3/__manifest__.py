{
    "name" : "InnoRug Manufacturing",
    "depends": ['mrp','sale', 'stock','product','account',"hr_contract"],
    "data": [
        "security/ir.model.access.csv",
        'views/work_order_view.xml',
        "views/mrp_production_views.xml",
        "views/cost_center_views.xml",
        # "views/gate_pass.xml",
        "reports/gate_pass_reports.xml",
        "reports/allotment_product_report.xml",
        "reports/cost_center_report.xml",
        "views/surya_sale_order_mrp.xml",
        'views/mrp_jobwork_views.xml',
        "views/mrp_routing_workcentre_views.xml",
        "views/bom_opration_operation.xml",
        "views/subcontractor_alloted_product_views.xml",
        "views/product_views.xml",
        "views/mrp_quality_control_views.xml",
        # "views/sale_order.xml",
    ],
    'application': True,
    "installable": True,
    'license': 'LGPL-3',
    

}

