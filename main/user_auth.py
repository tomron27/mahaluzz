from django.contrib.auth.models import User

def check_user(username, password):
    user_queryset = User.objects.filter(username=username)
    if not user_queryset.exists():
        return True, "משתמש לא קיים",None

    if not user_queryset[0].check_password(password):
        return True, "סיסמה שגויה",user_queryset

    return False, "הצלחה",user_queryset

def get_user_data(username):
    # TODO - query custom users database and retrieve relevant user data (children, etc)
    pass

