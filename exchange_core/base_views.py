from django.views.generic import TemplateView
from django.shortcuts import render


class MultiFormView(TemplateView):
    forms = {}

    def get_context_data(self):
        context = super().get_context_data()
        
        for form_name, form in self.forms.items():
            form_kwargs = self.get_form_kwargs(form_name)
            context['form_' + form_name] = form(**form_kwargs)
        
        return context

    def get_form_kwargs(self, form_name):
        form_instance_method = self.get_method('get_{}_instance'.format(form_name))
        return {'instance': form_instance_method()} if form_instance_method else {}

    def get_current_form(self):
        self.form_name = self.request.POST['form_name']
        return self.forms[self.form_name]

    def get_method(self, method_name):
        return getattr(self, method_name, None)

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request):
        current_form = self.get_current_form()
        form_kwargs = self.get_form_kwargs(self.form_name)
        form = current_form(request.POST, request.FILES, **form_kwargs)

        if form.is_valid():
            form_valid_method = self.get_method(self.form_name + '_form_valid')
            return form_valid_method(form)

        context = self.get_context_data()
        context['form_' + self.form_name] = form
        return render(request, self.template_name, context)