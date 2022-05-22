
import os
import stripe

class StripePayments():
    def getClientSecret(self):
        # stripe.api_key = 'pk_test_51KV0M6IVC1czDxQLHi2WnMagLPnOvVw0CEWVPZBTksSQsWpv5gQOlStW9xnEqISv2wJHAdWUWIPaOxvQN1Vzxlzx00sH2rsDVv'
        stripe.api_key = 'sk_test_51KV0M6IVC1czDxQLhLXpfR4jLeLl1G0qnL2A0JBrm4FeWRF7wfdRXsqXku9Q0j9PDIlPNgKeDcp3fRyhl71bSR2K0095pG3xCV'
        # stripe.api_key = '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'


        try:
            intent = stripe.PaymentIntent.create(
                 amount= 800,
                 currency= 'EGP')

            # Send PaymentIntent details to the front end.
            return ({'clientSecret': intent.client_secret})
        except stripe.error.StripeError as e:
            return ({'error': {'message': str(e)}}), 400
        except Exception as e:
            return ({'error': {'message': str(e)}}), 400
