from odoo import models, fields, api

class SaleProduct(models.Model):
    _name = 'sale.product'
    _description = 'Sale Product'
    
    # Trường để liên kết với sản phẩm
    product_template_id = fields.Many2one('product.template', string="Sản phẩm", required=True)
    
    # Các trường cho thông tin bán
    product_type_id = fields.Many2one("category.bds", string="Loại bất động sản")
    nums_bedrooms = fields.Integer(string="Số phòng ngủ")
    nums_bath = fields.Integer(string="Số nhà vệ sinh")
    facade = fields.Float(string="Mặt tiền (m)")
    real_length = fields.Float(string="Chiều dài (m)")
    way_in = fields.Integer(string="Ngõ vào (m)")
    floors = fields.Integer(string="Số Tầng")
    interior = fields.Char(string="Nội thất")
    direction_id = fields.Many2one("product.direction.new", string="Hướng nhà")

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

    user_id_ban = fields.Many2one('res.users', string='User', required=False)


    isApprove_ban = fields.Boolean(compute='_compute_is_approve_ban', string="Is Follow")
    isReadonly_ban = fields.Boolean(string="Is Readonly")
    
    def _compute_is_approve_ban(self):
        for record in self:
            if record.env.user.has_group('RealEstateModuleNew.group_people_dauchu'):
                record.isReadonly_ban = False
            else:
                record.isReadonly_ban = True

            if record.env.user in record.user_id_ban or record.env.user.has_group('RealEstateModuleNew.group_people_dauchu'):
                record.isApprove_ban = True
            else:
                record.isApprove_ban = False


    @api.onchange("state_id")
    def _onchange_state_id(self):
        self.district_id = False
        self.ward_id = False

    @api.onchange("district_id")
    def _onchange_district_id(self):
        self.ward_id = False

    # Tài khoản liên kết
    supp_ggmap = fields.Char(string="Google Map")
     
    
    def create(self, vals):
        # Tạo một bản ghi mới

        vals["user_id_ban"] = self.env.user.id
        record = super(SaleProduct, self).create(vals)
        return record

    # def action_reject(self):
    #     """Từ chối yêu cầu của người dùng và xóa nó."""
    #     for record in self:
    #         record.unlink()  # Xóa yêu cầu theo dõi