import json


def format_envelope_item(envelope_item):
    try:
        event = json.loads(envelope_item)
        if event.get('type') == 'transaction':
            return format_transaction(event)
        else:
            return format_error(event)
    except json.JSONDecodeError:
        # If we can't parse as JSON, return as is
        return envelope_item


def get_span_tree(event, prefix=""):
    assert event["type"] == "transaction"

    by_parent = {}
    for span in event["spans"]:
        by_parent.setdefault(span["parent_span_id"], []).append(span)

    def render_span(span):
        yield "{}- op={}: description={}".format(
            prefix, json.dumps(span.get("op")), json.dumps(span.get("description"))
        )
        for subspan in by_parent.get(span["span_id"]) or ():
            for line in render_span(subspan):
                yield f"{prefix}  {line}"

    root_span = event["contexts"]["trace"]

    # Return a list instead of a multiline string because black will know better how to format that
    return "\n".join(render_span(root_span))


def format_transaction(event):
    out = (
        f'  ~~~~ Transaction: "{event.get('transaction')}" ~~~~\n' +
        f"  Environment: {event.get('environment')}\n" +
        f"  Release:     {event.get('release')}\n" +
        f"  Tags:        {event.get('tags')}\n" +
        f"  Spans:\n" +
        get_span_tree(event, prefix="  ") + "\n" +
        f"  Raw Payload:\n  {event}\n"
    )

    return out


def format_error(event):
    out = (
        f"  ~~~~ Error ~~~~" + "\n" +
        f"  Raw Payload:\n  {event}\n"
    )
    return out 