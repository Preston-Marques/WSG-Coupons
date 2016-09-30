from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .forms import CouponCreationForm
from .models import Coupon, Claim
from accounts.models import Person

class IndexView(generic.ListView):
    template_name = 'coupons/index.html'
    context_object_name = 'latest_coupon_list'
    def get_queryset(self):
        # Return the last twenty published coupons, newest first
        return Coupon.objects.filter(
            publish_date__lte=timezone.now(),
            expire_date__gt=timezone.now()
        ).order_by('-publish_date')[:20]

class DetailView(generic.DetailView):
    model = Coupon
    template_name = 'coupons/detail.html'
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['claim_list'] = Claim.objects.filter(coupon=context['coupon'])
        return context

class ResultView(generic.DetailView):
    model = Coupon
    template_name = 'coupons/result.html'
    def get_queryset(self):
        return Coupon.objects.filter(publish_date__lte=timezone.now())

def claim(request, coupon_id):
    coupon = get_object_or_404(Coupon, pk=coupon_id)
    if request.user.is_authenticated():
        if coupon.expire_date >= timezone.now() >= coupon.publish_date :
            user = Person.objects.get(pk=request.user.id)
            if Claim.objects.filter(user=user, coupon=coupon).exists():
                # Redisplay the coupon detail form.
                return render(request, 'coupons/detail.html', {
                    'coupon': coupon,
                    'error_message': "You have already claimed this coupon.",
                })
            else:
                claim = Claim.objects.create(coupon=coupon, user=user)
                # Always return an HttpResponseRedirect after successfully dealing
                # with POST data. This prevents data from being posted twice if a
                # user hits the Back button.
                return HttpResponseRedirect(reverse('coupons:index'))
        else:
            return render(request, 'coupons/detail.html', {
                'coupon': coupon,
                'error_message': "Sorry, this coupon cannot be claimed at this time.",
            })
    else:
        return render(request, 'coupons/detail.html', {
            'coupon': coupon,
            'error_message': "You need to be logged in to claim.",
        })
#view for creating coupons
def createcoupon(request):
    if request.method == 'POST':
        form = CouponCreationForm(request.POST)
        if form.is_valid():
            coupon = form.save(commit=False)
            coupon.owner = request.user
            coupon = form.save()
            return redirect('coupons:index')
    else:
        form = CouponCreationForm()
    return render(request, 'coupons/create.html', {'form':form})
