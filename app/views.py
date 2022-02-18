from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from app.models import Vehicle, Record
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
import app.apiDef


def index(request):
    if request.user.is_authenticated:
        return home(request)
    return render(request, 'app/index.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def home(request):
    vehicles = Vehicle.objects.filter(user=request.user)
    return render(request, 'app/home.html', {'vehicles': vehicles})


@login_required
def vehicleDetailRecords(request, v_id):
    vehicle = Vehicle.objects.filter(id=v_id).first()
    records = Record.objects.filter(vehicle=vehicle)
    if vehicle is None or vehicle.user != request.user:
        raise PermissionDenied
    return render(request, 'app/vehicle_records.html', {'vehicle': vehicle, 'records': records})


@login_required
def vehicleDetailConsumption(request, v_id):
    vehicle = Vehicle.objects.filter(id=v_id).first()
    if vehicle is None or vehicle.user != request.user:
        raise PermissionDenied
    return render(request, 'app/vehicle_consumption.html', {'vehicle': vehicle})


@login_required
def vehicleDetailRefuel(request, v_id):
    vehicle = Vehicle.objects.filter(id=v_id).first()
    if vehicle is None or vehicle.user != request.user:
        raise PermissionDenied
    return render(request, 'app/vehicle_refuel.html', {'vehicle': vehicle})


@login_required
def vehicleDetailEdit(request, v_id):
    vehicle = Vehicle.objects.filter(id=v_id).first()
    records = Record.objects.filter(vehicle=vehicle)
    if vehicle is None or vehicle.user != request.user:
        raise PermissionDenied
    return render(request, 'app/vehicle_edit.html', {'vehicle': vehicle, 'brands': app.apiDef.getBrands(), 'records': records})


@login_required
def vehicleAdd(request):
    return render(request, 'app/vehicle_add.html', {'brands': app.apiDef.getBrands()})


@csrf_exempt
def vehicleAddGetModel(request):
    if request.method == 'POST':
        brand = str(request.POST.get('param'))
        return HttpResponse(app.apiDef.getModels(brand))


def vehicleAddPost(request):
    if request.method == 'POST':
        vehicle = Vehicle(brand=request.POST.get('brand'), model=request.POST.get('model'),
                          motor=request.POST.get('motor'), fuel=request.POST.get('fuel'),
                          fuelTank=request.POST.get('fuelTank'), kilometresCount=request.POST.get('km'),
                          user=request.user)
        vehicle.save()
        messages.success(request, "Vozidlo úspěšně přidáno.")
        return redirect('home')


def vehicleEditPost(request, v_id):
    if request.method == 'POST':
        vehicle = Vehicle.objects.get(id=v_id)
        vehicle.brand = request.POST.get('brand')
        vehicle.model = request.POST.get('model')
        vehicle.motor = request.POST.get('motor')
        vehicle.fuel = request.POST.get('fuel')
        vehicle.fuelTank = request.POST.get('fuelTank')
        vehicle.km = request.POST.get('km')

        vehicle.save()
        messages.success(request, "Změny úspěšně uloženy.")
        return redirect('/vehicle/' + v_id + '/edit')


def vehicleAddTankPost(request, v_id):
    if request.method == 'POST':
        consumed = 0
        vehicle = Vehicle.objects.get(id=v_id)
        thisVehicleRecords = Record.objects.filter(vehicle=vehicle)
        record = Record(kilometresCount=request.POST.get('km'), fuelType=request.POST.get('fuelType'),
                        liters=request.POST.get('liters'), pricePerLiter=request.POST.get('pricePerLiter'),
                        price=request.POST.get('price'), fullTank=request.POST.get('radioTank'),
                        missingRecord=request.POST.get('missingRecord'), refuelDate=request.POST.get('refuelDate'),
                        tankStation=request.POST.get('tankStationSelect'), vehicle=vehicle)
        vehicle.kilometresCount = request.POST.get('km')
        if record.missingRecord is None:
            record.missingRecord = False

        if record.fullTank == 'True':
            record.fuelTankActualState = vehicle.fuelTank
            consumed = float(record.liters)
        else:
            record.fuelTankActualState = float(request.POST.get('customTankValue')) + float(record.liters)
            consumed = thisVehicleRecords[len(thisVehicleRecords) - 1].fuelTankActualState - float(request.POST.get('customTankValue'))
            if record.fuelTankActualState > vehicle.fuelTank:
                record.fuelTankActualState = vehicle.fuelTank

        if len(thisVehicleRecords) > 0 and record.missingRecord is False:
            lastRecord = thisVehicleRecords[len(thisVehicleRecords) - 1]
            record.shortTermConsumption = round((consumed / (float(record.kilometresCount) - lastRecord.kilometresCount)) * 100, 2)

        vehicle.refuelCount += 1
        record.save()

        if len(thisVehicleRecords) > 0:
            consumptionAvg = Record.objects.filter(vehicle=vehicle, shortTermConsumption__gt=0).aggregate(Avg('shortTermConsumption'))
            roundedAvg = round(consumptionAvg['shortTermConsumption__avg'], 2)
            vehicle.longTermConsumption = roundedAvg
        vehicle.save()

        messages.success(request, "Tankování úspěšně evidováno.")
        return redirect('/vehicle/' + v_id + '/records')


def vehicleConsumptionCalc(request, v_id):
    if request.method == 'POST':
        vehicle = Vehicle.objects.get(id=v_id)
        resultDict = dict()
        resultDict['result'] = round((float(request.POST.get('calcKmInput')) / 100) * (
                vehicle.longTermConsumption * float(request.POST.get('calcPriceInput'))), 2)
        return render(request, 'app/vehicle_consumption.html', {'vehicle': vehicle, 'resultDict': resultDict})


def vehicleRecordDetail(request, v_id, r_id):
    record = Record.objects.get(id=r_id)
    vehicle = Vehicle.objects.get(id=v_id)
    records = Record.objects.filter(vehicle=vehicle)
    stateDict = dict()
    stateDict['state'] = int(round(((record.fuelTankActualState / vehicle.fuelTank) * 100), 0))
    return render(request, 'app/vehicle_records.html', {'records': records, 'record': record, 'vehicle': vehicle, 'stateDict': stateDict})


def vehicleEditRemove(request, v_id):
    Vehicle.objects.get(id=v_id).delete()
    messages.warning(request, "Vozidlo bylo úspěšně smazáno.")
    return redirect('home')


def vehicleRecordRemove(request, v_id, r_id):
    Record.objects.get(id=r_id).delete()
    messages.warning(request, "Záznam o tankování úspěšně smazán.")
    return redirect('/vehicle/' + v_id + '/records')


def vehicleDetailEditUploadImg(request, v_id):
    if request.method == 'POST' and request.FILES['vehicleImg']:
        vehicle = Vehicle.objects.get(id=v_id)
        carImage = request.FILES['vehicleImg']
        fs = FileSystemStorage()
        filename = fs.save(carImage.name, carImage)
        vehicle.image = fs.url(filename)
        vehicle.save()
        return redirect('/vehicle/' + v_id + '/edit')


@csrf_exempt
def getTankStation(request):
    if request.method == 'POST':
        return HttpResponse(app.apiDef.getTankStation(request))


@csrf_exempt
def getTankStationMap(request):
    if request.method == 'POST':
        return HttpResponse(app.apiDef.getMapGeometry(request))
