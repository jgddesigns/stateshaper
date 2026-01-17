template =  {
    "money_conservation": {
        "accounts_generated": 0,          # number of ledger accounts created
        "transactions_executed": 0,        # transfers, refunds, reversals
        "currency": "",
        "starting_total": 0,                # e.g. 18250000.00
        "ending_total": 0,                  # e.g. 18250000.00
        "net_drift": 0,                     # e.g. 0.00
        "net_drift_must_equal": 0,       # invariant
        "assertion_result": "",
        "first_failure_index": None,        # e.g. 8421 if failed
    },

    "payment_idempotency": {
        "requests_sent": 0,              # Total API requests issued
        "duplicate_groups": 0,           # Groups of intentionally duplicated requests
        "unique_charges": 0,             # Charges actually created
        "duplicate_charges": 0,          # Extra charges detected (should be 0)
        "expected_duplicate_charges": 0, # Invariant: must be 0
        "assertion_result": "",          # PASS / FAIL
        "first_failure_index": None,     # Index of first duplicate charge
    },

    "double_spend_prevention": {
        "concurrent_withdrawals": 0,      # Number of simultaneous withdrawals
        "min_balance": 0,                 # Lowest observed account balance
        "negative_balance_events": 0,     # Count of balances < 0
        "expected_negative_events": 0,    # Invariant: must be 0
        "assertion_result": "",           # PASS / FAIL
        "first_failure_index": None,      # Index of first negative balance event
    },

    "fraud_threshold_boundary": {
        "transactions_evaluated": 0,     # Total transactions checked
        "boundary_cases_generated": 0,   # Transactions near fraud thresholds
        "rule_mismatches": 0,            # Expected vs actual fraud decisions
        "expected_mismatches": 0,        # Invariant: must be 0
        "assertion_result": "",          # PASS / FAIL
        "first_failure_index": None,     # Index of first mismatch
    },

    "kyc_state_machine": {
        "users_generated": 0,             # Users created in onboarding flow
        "verified_count": 0,              # Users fully verified
        "pending_count": 0,               # Users awaiting documents
        "rejected_count": 0,              # Users rejected
        "invalid_transitions": 0,         # Illegal state transitions
        "expected_invalid_transitions": 0,# Invariant: must be 0
        "assertion_result": "",           # PASS / FAIL
        "first_failure_index": None,      # User index of first invalid transition
    },

    "regulatory_limits": {
        "daily_cap": 0,                   # Daily transaction limit
        "monthly_cap": 0,                 # Monthly transaction limit
        "blocked_attempts": 0,            # Transactions blocked by limits
        "limit_breaches": 0,              # Actual limit violations (should be 0)
        "expected_limit_breaches": 0,     # Invariant: must be 0
        "assertion_result": "",           # PASS / FAIL
        "first_failure_index": None,      # Index of first breach
    },

    "fx_conversion": {
        "conversions_executed": 0,        # Number of currency conversions
        "max_rounding_delta": 0,          # Max per-transaction rounding error
        "cumulative_drift": 0,            # Total FX drift across test
        "expected_cumulative_drift": 0,   # Invariant: must be 0
        "assertion_result": "",           # PASS / FAIL
        "first_failure_index": None,      # Index where drift first appears
    },

    "end_of_day_reconciliation": {
        "reconciliation_date": "",        # Date of reconciliation run
        "ledger_total": 0,                # Internal ledger total
        "processor_total": 0,             # Payment processor total
        "bank_total": 0,                  # Bank settlement total
        "unmatched_entries": 0,           # Entries not reconciled
        "expected_unmatched_entries": 0,  # Invariant: must be 0
        "assertion_result": "",           # PASS / FAIL
        "first_failure_index": None,      # Index of first mismatch
    },

    "refunds_and_chargebacks": {
        "refunds_issued": 0,              # Refund transactions
        "chargebacks_issued": 0,          # Chargebacks processed
        "duplicate_reversals": 0,         # Duplicate reversals detected
        "over_refunds": 0,                # Refunds exceeding original amount
        "expected_errors": 0,             # Invariant: must be 0
        "assertion_result": "",           # PASS / FAIL
        "first_failure_index": None,      # Index of first reversal error
    },

    "cross_version_determinism": {
        "baseline_version": "",           # Approved system version
        "tested_version": "",             # Version under test
        "output_deltas": 0,               # Count of behavioral differences
        "expected_output_deltas": 0,      # Invariant: must be 0
        "assertion_result": "",           # PASS / FAIL
        "first_failure_index": None,      # Index of first delta
    }
}


data = {
    "input": [
        {"data": "money_conservation", "groups": []},
        {"data": "payment_idempotency", "groups": []},
        {"data": "double_spend_prevention", "groups": []},
        {"data": "fraud_threshold_boundary", "groups": []},
        {"data": "kyc_state_machine", "groups": []},
        {"data": "regulatory_limits", "groups": []},
        {"data": "fx_conversion", "groups": []},
        {"data": "end_of_day_reconciliation", "groups": []},
        {"data": "refunds_and_chargebacks", "groups": []},
        {"data": "cross_version_determinism", "groups": []}
    ],
    "rules": "compound",
    "length": 10,
    "compound_length": 3,
    "compound_groups": [["breakfast", 1], ["meat", 0]],
    "compound_terms": ["and", "with"]
}
