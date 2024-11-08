from odoo import models, fields

class ProductFollow(models.Model):
    _name = 'product.follow'
    

    #user_id = fields.Many2one('res.users', string='User', required=False)
    product_id = fields.Many2one('product.template', string='Product', required=False)
    product_id_2 = fields.Many2one('product.template', string='Product', required=False)
    is_approved = fields.Boolean(string='Approved', default=False)    
    
    #duyệt
    def action_approve(self):
        """Cho phép người dùng xem chi tiết sản phẩm."""
        for record in self:
            record.is_approved = True
            record.product_id.follower_ids = [(3, record.id)]
            record.product_id_2.follower_2_ids = [(4, record.id)]


    #xóa khỏi danh sách
    def action_reject(self):
        """Từ chối yêu cầu của người dùng và xóa nó."""
        for record in self:
            record.unlink()  # Xóa yêu cầu theo dõi
    # duyệt thì kết nối và hiển thị lên danh sách đã duyệt, từ chối thì ngắt kết nối và biến mất khỏi danh sách đã duyệt
    def action_disconnect(self):
        """Từ chối yêu cầu của người dùng và xóa nó."""
        for record in self:
            record.is_approved = False
            record.product_id_2.follower_2_ids = [(3, record.id)]
            record.product_id.follower_ids = [(4, record.id)]

   

    