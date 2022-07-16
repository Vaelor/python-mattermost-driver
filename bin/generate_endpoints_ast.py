import ast
import json
from collections import namedtuple
from subprocess import run

from inflection import underscore

# Notes about parsing openapi file
#
# Attributes with special significance.
# All these attributes are part of the "paths" key which contains:
# - url_key: first key in the "paths" dictionary is the endpoint URL (e.g. "/users/login")
# - http_type: first key in the "url_key" that identifies the type of HTTP request that can be handled by this endpoint
#   - more on HTTP requests below, including specific arguments for each type
# - tags: the name of the module/file where the function should be stored.
#   - May include one ore more names in which case the function should be duplicated in more than one module
#   - May contain spaces that should be replaced with underscores
# - operation_id: CamelCase identifier used to give name to the API function call (e.g. CreateBot -> create_bot)
#   - Should also be included in the docstring as a URL linking to the original api (e.g. api.mattermost.com/#operation/CreateBot)
# - summary: description of the function that should be included in the docstring
# - parameters
#   - name: the name of the parameter that should be used as-is as a key in GET or POST attributes
#   - description: to be extracted into the docstring
#   - in: the "in" attribute contains either "path" or "query" which:
#     - "query": parameters that should be included as request attributes
#     - "path": parameters that should be included in the URL and string formatted
#   - schema.type: type annotation of parameter (for docstring)
#
# Type of request: Get
#   - Includes only query and path attributes.
#     - Query attributes should be passed as a JSON formatted
#     - Path attributes should be included in the URL and should be arguments to the function and formatted to the URL
# Type of request: Post / Put / Delete
#   - Can include a "requestBody" of type "application/json", "multipart/form-data" or "application/x-www-form-urlencoded"
#     - if "application/json" the options= attribute should be used. It will be sent as JSON
#     - if "application/x-www-form-urlencoded" the data= attribute should be used and a dictionary passed. It will be sent as URL encoded arguments
#     - if "multipart/form-data" the files= attribute should be used but additional arguments may also be passed via options=
#     - "description" should be kept and added to the function docstring as description of the attribute
#     - When including "required: true"
#       - schema.required is sometimes present to indicate properties that should be present in the payload
#       - schema.properties should be extracted and formatted into the docstring
#         - property_name: key in properties dictionary
#         - description: possible description of the attribute
#         - type: type annotation
#         - format: "binary" for file uploads, "int64" for some numeric fields
#     - When attribute isn't required the argument should default to None in the function signature (e.g. params=None)
#
# required = for parameters, there's often a "required: true" value,
#            for properties the field would be present in the "required" array
# type = "string", "integer", "boolean" and in some payloads, "array" and "object"
# default = a default value, usually an integer
# format = "binary" for upload fields, "int64" for some numeric fields
Parameter = namedtuple(
    "Parameter",
    ["name", "description", "required", "type", "default", "format"],
)


ast_template = """
from .base import Base
"""


def load_json(filepath="mattermost-api-reference/openapi.json"):
    with open(filepath) as fh:
        return json.loads(fh.read())


def get_parameters(params, key):
    output = {
        "description": "",
        "parameters": [],
        "required": False,
        "required_fields": [],
    }

    for param in params:
        if param["in"] == key:
            output["parameters"].append(
                Parameter(
                    param["name"],
                    param.get("description", ""),
                    param.get("required", False),
                    param["schema"]["type"],
                    param["schema"].get("default", None),
                    param["schema"].get("format", None),
                )
            )

    return output


def get_properties(schema):
    props = schema.get("properties", {})
    required = schema.get("required", [])

    return (
        required,
        [
            Parameter(
                prop,
                values.get("description", ""),
                prop in required,
                props.get("type", None),
                props.get("default", None),
                props.get("format", None),
            )
            for prop, values in props.items()
        ],
    )


def get_descriptions(params):
    if not params:
        return ""

    # Padding to align with docstring
    doc_pad = "        "

    def fix_docstr(doc):
        return doc.replace("\n", "\n          ")

    return (
        "\n\n"
        + "\n".join(
            [f"{doc_pad}{par.name}: {fix_docstr(par.description)}" for par in params]
        )
        + f"\n{doc_pad}"
    )


def parse_req_body(req_body_type, schema):
    if req_body_type in ("application/json", "multipart/form-data"):
        return get_properties(schema)
    elif req_body_type == "application/x-www-form-urlencoded":
        return (False, [])
    else:
        raise NotImplementedError(f"request body type {req_body_type} is not supported")


def get_request_body_type(body):
    if not body:
        return None

    assert len(body["content"].keys()) == 1

    return next(iter(body["content"].keys()))


def get_requestbody_parameters(body, request_type):
    # requestBody can have 3 types "application/json", "multipart/form-data" or "application/x-www-form-urlencoded"
    # - if "application/json" the options= attribute should be used. It will be sent as JSON
    # - if "application/x-www-form-urlencoded" the data= attribute should be used and a dictionary passed. It will be sent as URL encoded arguments
    # - if "multipart/form-data" the files= attribute should be used but additional arguments may also be passed via options=
    # - "description" should be kept and added to the function docstring as description of the attribute
    # - When including "required: true"
    #   - schema.required is sometimes present to indicate properties that should be present in the payload
    #   - schema.properties should be extracted and formatted into the docstring
    #     - property_name: key in properties dictionary
    #     - description: possible description of the attribute
    #     - type: type annotation
    #     - format: "binary" for file uploads, "int64" for some numeric fields
    # - When attribute isn't required the argument should default to None in the function signature (e.g. params=None)

    if not body:
        return {}

    req_body_type = get_request_body_type(body)

    required_fields, parameters = parse_req_body(
        req_body_type, body["content"][req_body_type]["schema"]
    )

    return {
        "description": body.get("description", ""),
        "parameters": parameters,
        "required": body.get("required", False),
        "required_fields": required_fields,
    }


def get_locations(tags):
    # Locations = which module the function call should be added to
    # NOTE that some identical function calls are present in more than one module/tag
    return list(map(lambda x: x.replace(" ", "_"), tags))


def get_payload_params_or_properties(data, request_type):
    if request_type == "get":
        return get_parameters(data.get("parameters", []), "query")
    else:
        req_body = data.get("requestBody", {})
        return get_requestbody_parameters(req_body, request_type)


def json_to_ast(api):
    blocks = {}

    for endpoint in api["paths"]:
        for request_type, rdata in api["paths"][endpoint].items():
            locations = get_locations(rdata["tags"])

            try:
                operation_id = rdata["operationId"]
            except KeyError:
                # We can't add API entries that don't have a function name
                print(
                    f">>> Couldn't create method for {endpoint} due to missing 'operationId'"
                )
                continue

            # Function name = underscore conversion of operation_id CamelCase
            function_name = underscore(operation_id)

            # In GET requests we have *query* parameters stored in the parameters object
            # For other types of request we have *properties* in the requestBody
            payload_params = get_payload_params_or_properties(rdata, request_type)

            url_parameters = get_parameters(rdata.get("parameters", {}), "path")

            docstring = rdata["summary"] + get_descriptions(
                url_parameters.get("parameters", [])
                + payload_params.get("parameters", [])
            )

            req_body = rdata.get("requestBody", {})
            req_body_type = get_request_body_type(req_body)

            # For every HTTP action there's a corresponding variable that should be used
            operations = {
                "delete": "params",
                "get": "params",
                "patch": "options",
                "post": "options",
                "put": "options",
            }

            def_params = prepare_def_keywords(
                url_parameters, payload_params, operations[request_type], req_body_type
            )
            call_kwargs = prepare_call_keywords(
                url_parameters, payload_params, operations[request_type], req_body_type
            )

            for loc in locations:
                if loc not in blocks:
                    blocks[loc] = []

                blocks[loc].append(
                    {
                        "module": loc,
                        "endpoint": endpoint,
                        "request_type": request_type,
                        "function": function_name,
                        "docstring": docstring,
                        "call_kwargs": call_kwargs,
                        "def_params": def_params,
                    }
                )

    return blocks


def prepare_call_keywords(url_params, payload_params, operation_arg, req_body_type):
    """Convert url parameters to function call arguments

    e.g. func(arg1, arg2=...)
    """

    # Add self to argument list because the function will be part of a class
    kwargs = []
    for param in url_params["parameters"]:
        if not param.required:
            kwargs.append(ast.keyword(arg=param.name, value=ast.Name(param.name)))

    # Add attributes specific to the operation being performed
    if req_body_type == "application/json":
        kwargs.append(ast.keyword(arg=operation_arg, value=ast.Name(operation_arg)))

    elif req_body_type == "application/x-www-form-urlencoded":
        kwargs.append(ast.keyword(arg=operation_arg, value=ast.Name(operation_arg)))
        kwargs.append(ast.keyword(arg="files", value=ast.Name("files")))

    elif req_body_type == "multipart/form-data":
        kwargs.append(ast.keyword(arg="data", value=ast.Name("data")))

    elif req_body_type is None:
        if payload_params.get("parameters", False):
            # Only add the argument if there are optional payload arguments
            kwargs.append(ast.keyword(arg=operation_arg, value=ast.Name(operation_arg)))

    else:
        raise NotImplementedError(
            f"Request body of type '{req_body_type}' is not implemented."
        )

    return kwargs


def prepare_def_keywords(url_params, payload_params, operation_arg, req_body_type):
    """Convert url parameters to function arguments

    e.g. def func(arg1, arg2=...):
    """

    args = [ast.arg(arg="self")]
    kwargs = []

    payload_required = payload_params.get("required", False)

    for param in url_params["parameters"]:
        if param.required:
            args.append(ast.arg(arg=param.name))
            # Always need to add a position matching None to AST kwargs
            kwargs.append(None)
        else:
            kwargs.append(ast.Constant(param.default))

    # Add attributes specific to the operation being performed
    if req_body_type == "application/json":
        args.append(ast.arg(arg=operation_arg))

        if payload_required:
            # Always need to add a position matching None to AST kwargs
            kwargs.append(None)
        else:
            kwargs.append(ast.Constant(None))

    elif req_body_type == "application/x-www-form-urlencoded":
        args.append(ast.arg(arg=operation_arg))
        args.append(ast.arg(arg="files"))

        if payload_required:
            # Always need to add a position matching None to AST kwargs
            kwargs.append(None)
            kwargs.append(None)
        else:
            kwargs.append(ast.Constant(None))
            kwargs.append(ast.Constant(None))

    elif req_body_type == "multipart/form-data":
        args.append(ast.arg(arg="data"))

        if payload_required:
            kwargs.append(None)
        else:
            kwargs.append(ast.Constant(None))

    elif req_body_type is None:
        if payload_params.get("parameters", False):
            # Only add the argument if there are optional payload arguments
            args.append(ast.arg(arg=operation_arg))
            kwargs.append(ast.Constant(None))

    else:
        raise NotImplementedError(
            f"Request body of type '{req_body_type}' is not implemented."
        )

    return {"args": args, "defaults": kwargs}


def ast_request(request_type, endpoint, call_params):
    args = [ast.parse('f"' + endpoint + '"')]

    return ast.Return(
        ast.Call(
            func=ast.Attribute(
                value=ast.Attribute(
                    value=ast.Name(id="self"),
                    attr="client",
                ),
                attr=request_type,
            ),
            args=args,
            keywords=call_params,
        )
    )


def ast_function(method):
    name = method["function"]
    docstring = method["docstring"]
    def_params = method["def_params"]
    call_kwargs = method["call_kwargs"]

    body = [
        ast.Expr(value=ast.Constant(value=docstring)),
        ast_request(method["request_type"], method["endpoint"], call_kwargs),
    ]

    return ast.FunctionDef(
        name=name,
        args=ast.arguments(
            **def_params,
            posonlyargs=[],
            kwonlyargs=[],
        ),
        body=body,
        decorator_list=[],
        lineno=None,
    )


def make_ast(methods, module):
    base = ast.parse(ast_template)
    funcs = [ast_function(method) for method in methods[module]]
    base.body.append(
        ast.ClassDef(
            module.lower().capitalize(),
            bases=[ast.Name("Base")],
            body=funcs,
            decorator_list=[],
            keywords=[],
        )
    )

    return base


def main():
    api = load_json()
    methods = json_to_ast(api)

    for module in methods.keys():
        code = make_ast(methods, module)
        filename = f"src/mattermostdriver/endpoints/{module}.py"
        with open(filename, "w") as fh:
            fh.write(ast.unparse(code))

        run(["black", filename])


if __name__ == "__main__":
    main()
