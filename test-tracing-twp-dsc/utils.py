
def format_baggage(baggage):
    """Given a baggage string format all the "sentry" prefixed keys and values in an easy to read format"""
    baggage_dict = {}
    for item in baggage.split(","):
        if item.startswith("sentry-"):
            key, value = item.split("=")
            baggage_dict[key] = value

    formatted_baggage = ""
    for key, value in sorted(baggage_dict.items()):
        formatted_baggage += f"  - {key:<20}: {value}\n"

    return formatted_baggage
