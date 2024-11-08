from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import json
class Product(models.Model):
    
    _inherit = 'product.template'
    
    # Trường để liên kết với sản phẩm
    product_template_id = fields.Many2one('product.template', string="Sản phẩm", required=True)
    
    # Các trường cho thông tin bán
    nums_bedrooms = fields.Integer(string="Số phòng ngủ")
    nums_bath = fields.Integer(string="Số nhà vệ sinh")
    facade = fields.Float(string="Mặt tiền (m)")
    real_length = fields.Float(string="Chiều dài (m)")
    real_width = fields.Float(string="Chiều rộng (m)")
    way_in = fields.Integer(string="Ngõ vào (m)")
    floors = fields.Integer(string="Số Tầng")
    interior = fields.Char(string="Nội thất")
    direction_id = fields.Many2one("product.direction.new", string="Hướng nhà")
    balcony = fields.Integer(string="Số ban công")

    acreage = fields.Float(string="Diện tích")
    real_acreage = fields.Float(string="Diện tích thực tế")
    alley = fields.Char(string="Ngõ, số nhà")
    street = fields.Char(string="Đường phố")
    ward = fields.Char(string="Phường xã")
    district = fields.Char(string="Quận huyện")
    city = fields.Char(string="Thành phố")
    state_id = fields.Many2one(comodel_name="res.country.state")
    country_id = fields.Many2one(
        comodel_name="res.country", default=lambda self: self.env.ref("base.vn")
    )

    sell_name = fields.Char(string="Tên chủ nhà", )
    sell_phone = fields.Char(string="Điện thoại chủ nhà", )

    offer_price = fields.Float(string="Giá chào hợp đồng (Triệu VND)")
    close_price = fields.Float(string="Giá chốt (Triệu VND)")
    bonus_money_percent = fields.Float(string="Hoa hồng %")
    bonus_money = fields.Float(string="Hoa hồng (Triệu VND)")

    district_id = fields.Many2one("res.country.district_new", string="District")
    ward_id = fields.Many2one("res.country.ward_new", string="Ward")
    @api.onchange("state_id")
    def _onchange_state_id(self):
        self.district_id = False
        self.ward_id = False

    @api.onchange("district_id")
    def _onchange_district_id(self):
        self.ward_id = False

    # Tài khoản liên kết
    supp_ggmap = fields.Char(string="Google Map")

    # product_type_id = fields.Many2one("product.type.new", string="Loại bất động sản")

    product_type_id = fields.Many2one("category.bds", string="Loại bất động sản")
    

  
    
    multiple_images = fields.Many2many('ir.attachment', 
        'product_template_ir_attachment_rel_multiple',  # Bảng trung gian tùy chỉnh
        'product_id', 'attachment_id',string="Ảnh sổ đỏ",help="Chọn nhiều hình ảnh cho sản phẩm này",
        domain=[('mimetype', 'ilike', 'image')],)
    
    
    additional_images_2 = fields.Many2many(
        'ir.attachment', 
        'product_template_ir_attachment_rel_additional_2',  # Bảng trung gian khác nữa
        'product_id', 'attachment_id', 
        string="Hình ảnh chi tiết",
        help="Chọn thêm hình ảnh chi tiết",
        # groups='RealEstateModuleNew.group_people_dauchu,RealEstateModuleNew.group_people_chunha,RealEstateModuleNew.group_people_daukhach',
        domain=[('mimetype', 'ilike', 'image')],
    )

    image_hopdong = fields.Binary(string="Hình ảnh hợp đồng trích thưởng")
    
    # image_hopdong = fields.Many2many('ir.attachment', 
    #     'product_template_ir_attachment_rel_image_hopdong',  # Bảng trung gian khác nữa
    #     'product_id', 'attachment_id', 
    #     string="Ảnh hợp đồng",
    #     help="Có thể chọn thêm hình ảnh",
    #     groups='RealEstateModuleNew.group_people_dauchu,RealEstateModuleNew.group_people_chunha,RealEstateModuleNew.group_people_daukhach',
    #     required=True,
    #     domain=[('mimetype', 'ilike', 'image')],
    # )

    
    
    # def write(self, vals):
    #     _logger.info(vals)  
    #     new_record = super(Product, self).write(vals)
    #     return new_record


    # multi_images = fields.Many2many(
    #     'ir.attachment', 
    #     string="Images",
    #     help="Upload multiple images for the product", groups='RealEstateModuleNew.group_people_dauchu')
    

    #người chờ duyệt
    follower_ids = fields.Many2many('product.follow', 'product_id', string="Followers")
    isFollow = fields.Boolean(compute='_compute_is_follow', string="Is Follow")
    isApprove = fields.Boolean(compute='_compute_is_approve', string="Is Follow")
    isReadonly = fields.Boolean(string="Is Readonly")

    #Nguoi duoc duyệt
    follower_2_ids = fields.Many2many('product.follow', 'product_id_2', string="Followers")
    #follower_2_ids = fields.Many2many('product.follow', 'product_id', string="Followers")

   
    isDuplicate = fields.Boolean( string="Is Duplicate")
    product_parent = fields.Many2one('product.template', string="Gốc", readonly=True)
    saler_id = fields.Many2one('res.partner', string="Người bán", domain="[('is_company','=',True)]")
    
    def _compute_is_approve(self):
        for record in self:
            if record.env.user.has_group('RealEstateModuleNew.group_people_dauchu'):
                record.isReadonly = False
            else:
                record.isReadonly = True

            if record.env.user in record.follower_2_ids.create_uid or record.env.user.has_group('RealEstateModuleNew.group_people_dauchu') or record.env.user.has_group('RealEstateModuleNew.group_people_chunha'):
                record.isApprove = True
            else:
                record.isApprove = False    
    def _compute_is_follow(self):
        for record in self:
            record.isFollow = record.env.user in record.follower_ids.create_uid
            
    def action_follow_product(self):
        # Phương thức này sẽ được gọi từ UI, có thể nhận thêm đối số
        self.ensure_one()  # Đảm bảo chỉ có một bản ghi

        # Kiểm tra xem người dùng đã theo dõi sản phẩm chưa
        existing_follow = self.env['product.follow'].search([
            ('create_uid', '=', self.env.user.id),
            ('product_id', '=', self.id)
        ], limit=1)
        _logger.info(existing_follow)


        if not existing_follow:
            existing_follow = self.env['product.follow'].create({
                'create_uid': self.env.user.id,
                'product_id': self.id,
                'product_id_2': self.id
            })
            _logger.info("fff")
        
        self.follower_ids = [(4, existing_follow.id)]    


        
        
        #Gửi thông báo đến tài khoản đầu khách
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            # 'params': {
            #  'title': 'Thông báo',
            # 'message': 'Hãy đợi Đầu chủ duyệt yêu cầu của bạn!',
            #  'sticky': False,
            # },
        }
        
    def write(self, vals):
        _logger.info(vals)  
        new_record = super(Product, self).write(vals)
        return new_record
    


    def domain(self):
            # Tạo mảng để lưu trữ các ID của các đối tác liên quan (partner_ids).
        _logger.info([self.env.user.id])
        if self.env.user.has_group('RealEstateModuleNew.group_people_dauchu') or self.env.user.has_group('RealEstateModuleNew.group_people_chunha'):
            return []
        return [('create_uid', '=', self.env.user.id)]
    #tạo sản phẩm bán
    sale_product_ids = fields.One2many('product.template', 'product_template_id', string="Sản phẩm bán",domain=domain)

    
    def action_create_sale_product(self):
        res = super().copy(default={'product_properties': {}})
        # Since we don't copy the product template attribute values, we need to match the extra prices.
        for ptal, copied_ptal in zip(self.attribute_line_ids, res.attribute_line_ids):
            for ptav, copied_ptav in zip(ptal.product_template_value_ids, copied_ptal.product_template_value_ids):
                if not ptav.price_extra:
                    continue
                # security check
                if ptav.attribute_id == copied_ptav.attribute_id and ptav.product_attribute_value_id == copied_ptav.product_attribute_value_id:
                    copied_ptav.price_extra = ptav.price_extra
        
        res.write({'name': self.name,'isDuplicate':True,'product_parent':self.id, "saler_id": self.create_uid.partner_id.id})
        res.create_uid.write({'product_for_sale_ids': [(4, res.id)]})
        self.sale_product_ids = [(4, res.id)]
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'Thông tin bán',
        #     'res_model': 'product.template',
        #     'res_id': res.id,
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'target': 'current',
        # }
    
    

   



    #go to website
    def action_go_to_website(self):
        self.ensure_one()
        # Lấy URL của sản phẩm trên website
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        product_url = f'/shop/product/{self.id}'
        # Điều hướng đến URL của sản phẩm
        return {
            'type': 'ir.actions.act_url',
            'url': f'{base_url}{product_url}',
            'target': 'new',  # Mở trong tab mới
        }

    
    # product_template_image_ids = fields.One2many(
    #         string="Extra Product Media",
    #         comodel_name='product.image',
    #         inverse_name='product_tmpl_id',
    #         copy=True,
    #     )