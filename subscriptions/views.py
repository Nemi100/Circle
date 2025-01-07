from django.shortcuts import render, redirect, get_object_or_404
from .models import SubscriptionPlan, UserSubscription, SubscriptionBasket
from .forms import SubscriptionForm, AddToBasketForm
from django.contrib.auth.decorators import login_required

def subscription_plans(request):
    plans = SubscriptionPlan.objects.all()
    basket_count = SubscriptionBasket.objects.filter(user=request.user).first().plans.count() if request.user.is_authenticated else 0
    return render(request, 'subscriptions/subscription-plans.html', {'plans': plans, 'basket_count': basket_count})

def add_to_basket(request):
    if request.method == 'POST':
        form = AddToBasketForm(request.POST)
        if form.is_valid():
            plan = get_object_or_404(SubscriptionPlan, id=form.cleaned_data['plan_id'])
            if request.user.is_authenticated:
                basket, created = SubscriptionBasket.objects.get_or_create(user=request.user)
                basket.plans.add(plan)
            else:
                if 'subscription_basket' not in request.session:
                    request.session['subscription_basket'] = []
                request.session['subscription_basket'].append(plan.id)
                request.session.modified = True
            return redirect('view_basket')
    return redirect('subscription_plans')

def view_basket(request):
    if request.user.is_authenticated:
        basket, created = SubscriptionBasket.objects.get_or_create(user=request.user)
        plans = basket.plans.all()
        basket_count = plans.count()
    else:
        plans = SubscriptionPlan.objects.filter(id__in=request.session.get('subscription_basket', []))
        basket_count = plans.count()
    return render(request, 'subscriptions/subscription_basket.html', {'plans': plans, 'basket_count': basket_count})

@login_required
def subscribe(request):
    plan_id = request.GET.get('plan_id')
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.plan = plan
            subscription.save()
            return redirect('thank_you')
    else:
        form = SubscriptionForm(initial={'plan': plan})
    
    return render(request, 'subscriptions/subscribe.html', {'form': form, 'plan': plan, 'basket_count': basket_count})

def thank_you(request):
    return render(request, 'subscriptions/thank_you.html')
