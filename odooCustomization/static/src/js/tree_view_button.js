odoo.define('bahmni_insurance_odoo.tree_view_button', function (require){
    "use strict";
    var Model = require('web.Model') 
    var core = require('web.core');
    var ListView = require('web.ListView');
    var QWeb = core.qweb;
    var custom_model = new Model('stock.production.lot') 
    ListView.include({       
    
            render_buttons: function($node) {
                    var self = this;
                    this._super($node);
                        this.$buttons.find('.o_list_button_bulk_scrap').click(this.proxy('action_bulk_scrap'));
                       
            },
    
            render_buttons: function($node) {
                var self = this;
                this._super($node);
                    this.$buttons.find('.o_list_button_bulk_archieve').click(this.proxy('action_bulk_archieve'));
                   
        },
            action_bulk_scrap: function () {  
                new Model("stock.production.lot").call("action_bulk_scrap",[this.get_selected_ids()]).then(function(result){
                     window.location.reload() ;
                    console.log(result);//show result in console
                    });
            }  
            ,
            action_bulk_archieve: function () {  
                new Model("stock.production.lot").call("action_bulk_archieve",[this.get_selected_ids()]).then(function(result){
                     window.location.reload() 
                    console.log(result);//show result in console
                    });
            }  
    
    });
    
    });