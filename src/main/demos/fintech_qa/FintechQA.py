from .qa_data import template, data


class FintechQA:


    def __init__(self, data=None, **kwargs):

        self.tokens = None




    def get_test(self, token):
        test = {
            "accounts_generated": self.random_number(token, 500),          # number of ledger accounts created
            "transactions_executed": self.random_number(token, 10000),        # transfers, refunds, reversals
            "starting_total": 0,                # e.g. 18250000.00
            "transactions_list": self.transactions_list(token),
            # set in front end
            "ending_total": 0,                  # e.g. 18250000.00
            "net_drift": 0,                     # e.g. 0.00
            "expected_drift": 0,          # invariant
            "assertion_result": "",
        }

        start = float((test["accounts_generated"] * self.random_number(token, 50000, 10)) + self.random_decimal(token))
        test["starting_total"] = f"{start:.2f}"

        return test

    
    def random_decimal(self, token):
        return (token % 100) / 100


    def random_number(self, token, ceiling, multiplier=1):
        return (token % ceiling) * multiplier


    def get_currency(self, token):
        currencies = ["USD","EUR","JPY","GBP","AUD","CAD","CHF","CNY","SEK","NZD","MXN","SGD","HKD","NOK","KRW","TRY","INR","RUB","ZAR","BRL","TWD","DKK","PLN","THB","MYR","IDR","HUF","CZK","AED","SAR","QAR","KWD","OMR","ILS","PHP","VND","EGP","NGN","PKR","COP","ARS","CLP","PEN","JOD","BHD","LKR","KES","RON","MAD","TND"]
        return currencies[token % len(currencies)]
    

    def transactions_list(self, token):
        types = ["deposit", "withdraw", "transfer", "stock", "bill"]
        return self.derive_index(token, types)


    def derive_index(self, token, types):
        included = {}
        count = token % len(types) + 1
        print(count)
        print(token)
        for i in range(count):
            test = types[round(token / (i + 2)) % len(types)-1] 
            if test not in list(included.keys()):
                included[test] = self.get_amount(token, i+2) 
        return included
    

    def get_amount(self, token, multiplier=5):
        return (token * multiplier * ((token % 5)+1)) + (token * multiplier % 100) / 100


    def payment_idempotency(self):
        test = template[self.current_test]
        print()
        print(test)


    def double_spend_prevention(self):
        test = template[self.current_test]
        print()
        print(test)


    def fraud_threshold_boundary(self):
        test = template[self.current_test]
        print()
        print(test)


    def kyc_state_machine(self):
        test = template[self.current_test]
        print()
        print(test)


    def regulatory_limits(self):
        test = template[self.current_test]
        print()
        print(test)


    def fx_conversion(self):
        test = template[self.current_test]
        print()
        print(test)


    def end_of_day_reconciliation(self):
        test = template[self.current_test]
        print()
        print(test)


    def refunds_and_chargebacks(self):
        test = template[self.current_test]
        print()
        print(test)


    def cross_version_determinism(self):
        test = template[self.current_test]
        print()
        print(test)


FintechQA()