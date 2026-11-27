import csv
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import TelemetryRecord


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("dashboard")
    return render(request, "telemetry/signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        messages.error(request, "Invalid username or password. Please try again.")
    return render(request, "telemetry/login.html")


def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    search_query = request.GET.get("q", "").strip()
    selected_status = request.GET.get("status", "all")
    per_page = request.GET.get("per_page", "5")
    if per_page not in {"5", "10", "15"}:
        per_page = "5"
    records = TelemetryRecord.objects.all()
    if search_query:
        records = records.filter(satellite_id__icontains=search_query)
    if selected_status in {"Active", "Warning", "Critical"}:
        records = records.filter(status=selected_status)
    paginator = Paginator(records, int(per_page))
    page_obj = paginator.get_page(request.GET.get("page"))
    summary = TelemetryRecord.objects.aggregate(average_battery=Avg("battery"))
    context = {
        "page_obj": page_obj, "search_query": search_query,
        "selected_status": selected_status, "per_page": per_page,
        "total_records": TelemetryRecord.objects.count(),
        "active_count": TelemetryRecord.objects.filter(status="Active").count(),
        "warning_count": TelemetryRecord.objects.filter(status="Warning").count(),
        "critical_count": TelemetryRecord.objects.filter(status="Critical").count(),
        "average_battery": round(summary["average_battery"] or 0),
    }
    return render(request, "telemetry/dashboard.html", context)


@login_required
def export_csv(request):
    records = TelemetryRecord.objects.all()
    search_query = request.GET.get("q", "").strip()
    selected_status = request.GET.get("status", "all")
    if search_query:
        records = records.filter(satellite_id__icontains=search_query)
    if selected_status in {"Active", "Warning", "Critical"}:
        records = records.filter(status=selected_status)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="aerotrack-telemetry.csv"'
    writer = csv.writer(response)
    writer.writerow(["Satellite ID", "Altitude (km)", "Temperature (C)", "Battery (%)", "Signal Strength", "Status"])
    for record in records:
        writer.writerow([record.satellite_id, record.altitude, record.temperature, record.battery, record.signal_strength, record.status])
    return response
