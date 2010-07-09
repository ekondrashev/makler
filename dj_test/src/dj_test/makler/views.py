from django.template import Context, loader
from dj_test.makler.models import Advertisement
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from dj_test.makler.adv_to_json import getJson

def index(request):
    latest_adv_list = Advertisement.objects.all().order_by('-pub_date')[:5]
    t = loader.get_template('makler/index.html')
    c = Context({
        'latest_adv_list': latest_adv_list,
    })
    return HttpResponse(t.render(c))

def test(request):
    return HttpResponse("Hello, world.")

def json(request):
    #request.encoding = 'ISO-8859-8'
    #request.encoding = 'utf-8'
    #print request.GET['adv_text']
    adv_text = unicode(request.GET['adv_text'])
    return HttpResponse(getJson(adv_text))

def detail(request, adv_id):
    adv = get_object_or_404(Advertisement, pk=adv_id)
    return render_to_response('makler/advDetail.html', {'adv': adv})

def addAdv(request):
    adv_text = request.POST['adv_text']
    adv = Advertisement(text = adv_text)
    adv.save()
    return HttpResponseRedirect(reverse('dj_test.makler.views.index'))