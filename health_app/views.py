import requests
from django.shortcuts import render, redirect
from .models import RealEstate
from django.conf import settings
import os
import ssl
import json  # Debugging
from django.contrib.auth.decorators import login_required

AZURE_API_URL = "http://b088d51b-1dcb-445e-bfbb-01cb2b42bf40.germanywestcentral.azurecontainer.io/score"

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)

def home(request):
    return render(request, 'health_app/home.html')


@login_required
def real_estate_input(request):
    if request.method == "POST":
        
        api_payload = {
            "Inputs": {
                "input1": [
                    {
                        "area": int(request.POST.get("area")),
                        "bedrooms": int(request.POST.get("bedrooms")),
                        "bathrooms": int(request.POST.get("bathrooms")),
                        "stories": int(request.POST.get("stories")),
                        "mainroad": int(request.POST.get("mainroad")),
                        "guestroom": int(request.POST.get("guestroom")),
                        "basement": int(request.POST.get("basement")),
                        "hotwaterheating": int(request.POST.get("hotwaterheating")),
                        "airconditioning": int(request.POST.get("airconditioning")),
                        "parking": int(request.POST.get("parking")),
                        "prefarea": int(request.POST.get("prefarea")),
                        "furnishingstatus": int(request.POST.get("furnishing"))
                    }
                ]
            },
            "GlobalParameters": {}
        }

        

        headers = {
            "Authorization": f"Bearer {settings.AZURE_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            #  DEBUG: Print API request payload
            print("🔵 Sent to Azure API:", json.dumps(api_payload, indent=4))

            response = requests.post(AZURE_API_URL, json=api_payload, headers=headers)

            response.raise_for_status()
            data = response.json()
            print("🟢 Received from Azure API:", json.dumps(data, indent=4))  # Debugging
            predicted_price = data["Results"]["WebServiceOutput0"][0]["Scored Labels"]

        except requests.RequestException as e:
            predicted_price = f"Error: {e}"

        request.session["Scored Labels"] = round(float(predicted_price), 2)

        real_estate = RealEstate.objects.create(
            user=request.user,
            price=float(predicted_price),
            area=int(request.POST.get("area")),
            bedrooms=int(request.POST.get("bedrooms")),
            bathrooms=int(request.POST.get("bathrooms")),
            stories=int(request.POST.get("stories")),
            mainroad=request.POST.get("mainroad") == "1",
            guestroom=request.POST.get("guestroom") == "1",
            basement=request.POST.get("basement") == "1",
            hotwaterheating=request.POST.get("hotwaterheating") == "1",
            airconditioning=request.POST.get("airconditioning") == "1",
            parking=int(request.POST.get("parking")),
            prefarea=request.POST.get("prefarea") == "1",
            furnishingstatus=int(request.POST.get("furnishing")),
        )
        real_estate.save()


        return redirect("profile")

    return render(request, "health_app/real_estate_input.html")


@login_required
def profile(request):
    if request.user.is_superuser:
        real_estates = RealEstate.objects.all().order_by('-id')  # Admin sees all entries, ordered by newest
    else:
        real_estates = RealEstate.objects.filter(user=request.user).order_by('-id')  # Normal users see their entries, ordered by newest

    predicted_price = request.session.get("predicted_price", "No prediction available")
    return render(request, "health_app/profile.html", {"predicted_price": predicted_price, "real_estates": real_estates})




