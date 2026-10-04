REQUIRED = ("overtime_hours", "tenure_months", "commute_km",)
WEIGHTS = {"overtime_hours": 0.4, "tenure_months": -0.05, "commute_km": 0.02}
INTERCEPT = -1.0
THRESHOLD = 0.0


class InputError(ValueError):
    pass


def score(body):
    missing = [name for name in REQUIRED if name not in body]
    if missing:
        raise InputError("missing " + ", ".join(missing))
    total = INTERCEPT
    parts = []
    for name, weight in WEIGHTS.items():
        value = body[name]
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise InputError(f"{name} must be a number")
        contrib = weight * value
        total += contrib
        parts.append({"feature": name, "contribution": round(contrib, 4)})
    label = "high" if total >= THRESHOLD else "low"
    return {"score": round(total, 4), "label": label, "threshold": THRESHOLD, "parts": parts}
