from django.template import Context, loader
from dj_test.makler.models import Advertisement
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404

def index(request):
    latest_adv_list = Advertisement.objects.all().order_by('-pub_date')[:5]
    t = loader.get_template('makler/index.html')
    c = Context({
        'latest_adv_list': latest_adv_list,
    })
    return HttpResponse(t.render(c))

def detail(request, adv_id):
    adv = get_object_or_404(Advertisement, pk=adv_id)
    return render_to_response('makler/advDetail.html', {'adv': adv})

def addAdv(request):
    adv_text = request.POST['adv_text']
    adv = Advertisement(text = adv_text)
    adv.save()
    return HttpResponseRedirect(reverse('dj_test.makler.views.index'))