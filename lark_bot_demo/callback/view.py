from flask import Blueprint, copy_current_request_context, current_app, request
from flask.helpers import make_response
from flaskthreads import AppContextThread
from larksuiteoapi.card import handle_card, set_card_callback
from larksuiteoapi.event import handle_event
from larksuiteoapi.model import OapiHeader, OapiRequest
from larksuiteoapi.service.im.v1 import MessageReceiveEventHandler

from lark_bot_demo.callback.handler import CardCallbackEntry, MessageCallbackEntry

bp = Blueprint('callback', __name__, url_prefix='/callback')


def init():
    # To meet the "message_impl should be handle in 1s" limit, we have to process the request async.
    # We should copy current app and request context to that thread manually, so that we can use
    # `current_app` and functions like `url_for` in the sub-threads.
    MessageReceiveEventHandler.set_callback(
        current_app.config.lark,
        lambda ctx, conf, event: AppContextThread(
            target=copy_current_request_context(MessageCallbackEntry(event).handle)).start())

    set_card_callback(
        current_app.config.lark,
        lambda ctx, conf, card: CardCallbackEntry(card).handle())


@bp.route('/event', methods=('POST',))
def event_callback():
    """
    Process event (async) callback.
    :return: empty 200 response
    """
    oapi_request = OapiRequest(uri=request.path, body=request.data, header=OapiHeader(request.headers))
    oapi_resp = handle_event(current_app.config.lark, oapi_request)
    resp = make_response()
    resp.headers['Content-Type'] = oapi_resp.content_type
    resp.data = oapi_resp.body
    resp.status_code = oapi_resp.status_code
    return resp


@bp.route('/card', methods=('POST',))
def card_callback():
    """
    Process card_impl (sync) callback.
    :return: updated card content
    """
    oapi_request = OapiRequest(uri=request.path, body=request.data, header=OapiHeader(request.headers))
    oapi_resp = handle_card(current_app.config.lark, oapi_request)
    resp = make_response()
    resp.headers['Content-Type'] = oapi_resp.content_type
    resp.data = oapi_resp.body
    resp.status_code = oapi_resp.status_code
    return resp
