from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def paginate(request, queryset, *, url_param_name='page'):
	page_number = request.GET.get(url_param_name, 1)
	paginator = Paginator(queryset, 20)

	try:
		return paginator.get_page(page_number)
	except (PageNotAnInteger, EmptyPage):
		return paginator.get_page(1)
