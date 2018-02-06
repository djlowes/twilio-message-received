from twilio.rest import Client

# put your own credentials here
account_sid = "AC05c492100ba229f40bd463f0c99da9b2"
auth_token = "your_auth_token"

client = Client(account_sid, auth_token)

client.messages.create(
    to="+5555555555",
    from_="+5555555555",
    body="McAvoy or Stewart? These timelines can get so confusing.",
    status_callback="https://requestb.in/1i4srh11"
)