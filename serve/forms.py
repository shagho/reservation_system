from django import forms



class ProfileForm(forms.Form):
    name = forms.CharField(max_length=128, required=True, error_messages={'required': 'این فیلد الزامی است.'})
    email = forms.EmailField(max_length=128, required=False)

    def save(self, user, data):
        user.email = data['email']
        user.name = data['name']
        user.save()
