import json
import os
import shutil


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


def write_envelope_item_to_file(version_from_envelope_header, item_header, payload):
    """
    Creates a directory for the SDK version used and then saves the envelope item
    as formatted JSON into the directory.
    """
    print(f"Payload: {payload}")
    sdk_version = version_from_envelope_header

    if sdk_version is None:
        try:
            sdk_version = json.loads(payload)["sdk"]["version"]
        except (KeyError, json.JSONDecodeError):
            try:
                for attr in json.loads(payload)["attributes"]:
                    if attr["key"] == "sentry.sdk.version":
                        sdk_version = attr["value"]["stringValue"]
                        break
            except Exception as e:
                try:
                    sdk_version = json.loads(payload)["release"]
                except Exception as e:
                    try:
                        sdk_version = json.loads(payload)["attrs"]["release"]
                    except Exception as e:
                        print(f"XXX Error parsing payload: {e}")

    suffix = 0
    filename = f"envelope-{item_header['type']}-{suffix}.json"
    filepath = os.path.join(sdk_version, filename)
    print(f"Writing envelope item to {filepath}")

    os.makedirs(sdk_version, exist_ok=True)

    try:
        # Try to parse the payload as JSON first
        json_payload = json.loads(payload)
        formatted_payload = json.dumps(json_payload, indent=2, sort_keys=True)
    except json.JSONDecodeError:
        # If it's not valid JSON, write it as is
        formatted_payload = payload

    while os.path.exists(filepath):
        suffix += 1
        filename = f"envelope-{item_header['type']}-{suffix}.json"
        filepath = os.path.join(sdk_version, filename)

    with open(filepath, "w") as f:
        f.write(formatted_payload)
