from django import forms
from Employee import models


class BookForm(forms.ModelForm):
    year = forms.DateField(widget=forms.DateInput(),input_formats=['%d/%m/%Y'])
    category=forms.ModelMultipleChoiceField(queryset=models.BookCategory.objects.all(),widget=forms.CheckboxSelectMultiple)
    class Meta:
        model=models.Book
        fields=("title","isbn","author","publications","edition","price","no_of_copies","initial_copies","book_pic")

    def clean_isbn(self):
        if len(str(self.cleaned_data['isbn']))!=13:
            raise forms.ValidationError("Incorrect ISBN number")
        return self.cleaned_data['isbn']

    def save(self,commit=True):
        f=super(BookForm,self).save(commit=False)
        f.year=self.cleaned_data['year']
        if commit:
            f.save()
        categories=self.cleaned_data['category']
        f.category.set(categories)

        return f





