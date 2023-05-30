from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from world.models import City, Country, Language

def search(request):
    if request.method == 'POST':
        search_term = request.POST.get('search_term')
        
        cities = City.objects.filter(name__icontains=search_term)
        countries = Country.objects.filter(name__icontains=search_term)
        languages = Language.objects.filter(name__icontains=search_term)
        
        context = {
            'cities': cities,
            'countries': countries,
            'languages': languages,
        }
        
        return render(request, 'search_results.html', context)

    return render(request, 'dashboard.html')
