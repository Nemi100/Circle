from django.shortcuts import render, redirect, get_object_or_404
from .models import SubscriptionPlan, UserSubscription, SubscriptionBasket
from .forms import SubscriptionForm, AddToBasketForm
from django.contrib.auth.decorators import login_required

def subscription_plans(request):
    plans = SubscriptionPlan.objects.all()
    basket_count = SubscriptionBasket.objects.filter(user=request.user).first().plans.count() if request.user.is_authenticated else 0
    return render(request, 'subscriptions/subscription_plans.html', {'plans': plans, 'basket_count': basket_count})

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
            return redirect('subscriptions:subscription_basket')
    return redirect('subscriptions:subscription_plans')

def proceed_to_subscribe(request):
    if request.method == 'POST':
        subscription_data = []
        for key, value in request.POST.items():
            if key.startswith('subscription_type_'):
                plan_id = key.split('_')[2]
                newsletter = request.POST.get(f'newsletter_{plan_id}', 'no')
                subscription_data.append({
                    'plan_id': plan_id,
                    'subscription_type': value,
                    'newsletter': newsletter
                })
        request.session['subscription_data'] = subscription_data
        return redirect('subscriptions:subscribe')
    return redirect('subscriptions:subscription_plans')

def switch_plan(request):
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        if request.user.is_authenticated:
            basket = SubscriptionBasket.objects.get(user=request.user)
            basket.plans.remove(plan_id)
        else:
            subscription_basket = request.session.get('subscription_basket', [])
            if plan_id in subscription_basket:
                subscription_basket.remove(plan_id)
            request.session['subscription_basket'] = subscription_basket
        return redirect('subscriptions:subscription_plans')
    return redirect('subscriptions:subscription_plans')

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
    subscription_data = request.session.get('subscription_data', [])
    plans = [get_object_or_404(SubscriptionPlan, id=data['plan_id']) for data in subscription_data]
    # Here, to handle the payment process or integrate Stripe
    # For now,i am simulating the payment processing
    if request.method == 'POST':
        # After payment is successful
        return redirect('subscriptions:thank_you')
    return render(request, 'subscriptions/subscribe.html', {'plans': plans, 'subscription_data': subscription_data})

def thank_you(request):
    show_toast = True  
    return render(request, 'subscriptions/thank_you.html', {'show_toast': show_toast})
