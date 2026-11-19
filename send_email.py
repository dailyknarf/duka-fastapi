try:
    import mailtrap  # type: ignore[import-not-found]
except ImportError:
    mailtrap = None


token = "daa1efb818285d31b6560476dce55f92"


def email(to, subject, message):
    if mailtrap is None:
        raise RuntimeError(
            "The 'mailtrap' package is not installed. Install it with: pip install mailtrap"
        )

    mail = mailtrap.Mail(
        sender=mailtrap.Address(email="hello@demomailtrap.co"),
        name="FLASK-API",
        to=[mailtrap.Address(email=to)],
        subject=subject,
        text=message,
        category="mailtrap integration test",
    )
    client = mailtrap.MailtrapClient(token=token)
    response = client.send(mail)

    print("this is mailtrap----------------------------------------")
    print(response)


# email("frankmulandi5758@gmail.com", "Testing API", "This is a test message.")