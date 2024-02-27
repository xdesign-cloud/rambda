import functools
import inspect

from aws_xray_sdk.core import xray_recorder

from .request import Request
from .response import Response


def lambda_rest_endpoint(_func=None, *, include_raw_event=False):
    def outer_wrap(func):
        @functools.wraps(func)
        def inner_wrap(event, context):
            xray_recorder.begin_segment("Process Request")
            xray_recorder.begin_subsegment("Parse Request")
            request = Request.from_apigw_event(
                event, include_raw_event=include_raw_event
            )
            xray_recorder.end_subsegment()

            xray_recorder.begin_subsegment("Call Inner Function")
            sig = inspect.signature(func, follow_wrapped=True)
            kwargs = {}
            if "request" in sig.parameters:
                kwargs["request"] = request
            response = func(**kwargs)
            xray_recorder.end_subsegment()

            xray_recorder.begin_subsegment("Process Response")
            if isinstance(response, dict):
                response = Response(body=response)
            elif (
                isinstance(response, tuple)  # ie `return 200, {"hello": "world"}`
                and isinstance(response[0], int)  # Status code
                and isinstance(response[1], dict)  # Response body
            ):
                response = Response(body=response[1], status_code=response[0])
            xray_recorder.end_subsegment()

            return response.api_gateway_response()

        return inner_wrap

    # This allows us to use the decorator as @lambda_rest_endpoint when we don't have
    # arguments
    if _func is None:
        return outer_wrap
    else:
        return outer_wrap(_func)
