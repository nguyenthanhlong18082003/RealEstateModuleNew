from odoo import http
import io
import logging
import zipfile

from werkzeug.exceptions import NotFound

from odoo import _, http
from odoo.exceptions import AccessError
from odoo.http import request, content_disposition

from odoo.tools import consteq
from odoo.addons.mail.models.discuss.mail_guest import add_guest_to_context

logger = logging.getLogger(__name__)

class RealEstateModuleNewNew(http.Controller):
    @http.route("/mail/attachment/upload", methods=["POST"], type="http", auth="public")
    @add_guest_to_context
    def mail_attachment_upload(self, ufile, thread_id, thread_model, is_pending=False, **kwargs):
        thread = request.env[thread_model].with_context(active_test=False).search([("id", "=", thread_id)])
        if not thread:
            raise NotFound()
        if thread_model == "discuss.channel" and not thread.allow_public_upload and not request.env.user._is_internal():
            raise AccessError(_("You are not allowed to upload attachments on this channel."))
        vals = {
            "name": ufile.filename,
            "raw": ufile.read(),
            "res_id": int(thread_id),
            "res_model": thread_model,
        }
        if is_pending and is_pending != "false":
            # Add this point, the message related to the uploaded file does
            # not exist yet, so we use those placeholder values instead.
            vals.update(
                {
                    "res_id": 0,
                    "res_model": "mail.compose.message",
                }
            )
        if request.env.user.share:
            # Only generate the access token if absolutely necessary (= not for internal user).
            vals["access_token"] = request.env["ir.attachment"]._generate_access_token()
        try:
            # sudo: ir.attachment - posting a new attachment on an accessible thread

            logger.info(kwargs)
            attachment = request.env["ir.attachment"].sudo().create(vals)
            attachment._post_add_create(**kwargs)
            attachmentData = attachment._attachment_format()[0]
            if attachment.access_token:
                attachmentData["accessToken"] = attachment.access_token
        except AccessError:
            attachmentData = {"error": _("You are not allowed to upload an attachment here.")}
        return request.make_json_response(attachmentData)


