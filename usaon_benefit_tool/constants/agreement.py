"""Constants for the Contributor User Agreement & Informed Consent.

Bump CURRENT_AGREEMENT_VERSION whenever a *material* change (per Section 10)
is published. All users who accepted an older version will be re-prompted on
their next request. Non-material changes (typos, formatting) should NOT bump
this constant.
"""

CURRENT_AGREEMENT_VERSION = "1.0"
CURRENT_AGREEMENT_EFFECTIVE_DATE = "June 24, 2026"

# The confirmations from the Statement of Informed Consent. Each is rendered
# as a required checkbox and validated server-side by name.
CONSENT_STATEMENTS: dict[str, str] = {
    "read_understood": (
        "I have read and understood this Contributor User Agreement."
    ),
    "age_18": "I am 18 years of age or older.",
    "voluntary": (
        "I voluntarily agree to contribute and understand I may withdraw"
        " at any time."
    ),
    "public_attribution": (
        "I understand that my assessments will be publicly attributed to me"
        " by name and institution."
    ),
    "withdrawal_limits": (
        "I understand the current limitations on data withdrawal described"
        " in Section 4.2."
    ),
    "updates": (
        "I understand that this agreement may be updated, and I will be"
        " notified of material changes."
    ),
}
