from django.utils import timezone


def reset_password_expire_otp(user, password):
    """
    Reset user's password and expire OTP.

    This function resets the user's password to the provided one
    and marks the OTP (One Time Password) as expired.
    """
    expiration_time = user.password_reset_otp_created_at + \
        timezone.timedelta(minutes=15)

    if timezone.now() > expiration_time:
        return False, 'OTP has expired. Please request a new one.'

    # reset password
    user.set_password(password)
    user.save()

    # mark OTP as expired
    user.password_reset_otp = None
    user.password_reset_otp_created_at = None
    user.save()

    return True, 'Password reset successful.'
