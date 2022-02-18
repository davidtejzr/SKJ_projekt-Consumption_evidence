function getVehicleModels()
{
    const brand = document.getElementById("brandInput").value;
    const select = document.getElementById("modelInput");
    const length = select.options.length;
    for (let i = length-1; i >= 0; i--)
    {
        select.options[i] = null;
    }

    $.ajax({
        type: "POST",
        url: "/vehicle/add/getModel",
        data: { param: brand }
    }).done(function(data)
    {
        const models = JSON.parse(data);
        for(let i = 0; i < models['results'].length; i++)
        {
            const option = document.createElement('option');
            option.value = models['results'][i]['Model'] + ' (' + models['results'][i]['Year'] + ')';
            option.innerHTML = models['results'][i]['Model'] + ' (' + models['results'][i]['Year'] + ')';
            document.getElementById("modelInput").appendChild(option);
        }
    });
}

function getTankStation()
{
    const region = document.getElementById("regionSelect").value;
    let fuel = document.getElementById("fuelTypeInput").value;
    fuel = fuel.replace(" ", "-");
    const select = document.getElementById("tankStationSelect");
    document.getElementById("pricePerLiterTankInput").value = null;
    const length = select.options.length;
    for (let i = length-1; i >= 0; i--)
    {
        select.options[i] = null;
    }

    $.ajax({
        type: "POST",
        url: "/vehicle/getTankStation",
        data: { region: region, fuel: fuel }
    }).done(function(data)
    {
        const tankStations = JSON.parse(data);

        tankStations.sort(function (a, b)
        {
            return a.name.localeCompare(b.name);
        });

        const defaultOption = document.createElement('option');
        defaultOption.innerHTML = "Vyberte kraj";
        defaultOption.selected = true;
        defaultOption.disabled = true;
        document.getElementById("tankStationSelect").appendChild(defaultOption);

        for(let i = 0; i < tankStations.length; i++)
        {
            const option = document.createElement('option');
            option.value = tankStations[i]['name'] + ' | ' + tankStations[i]['address'];
            option.innerHTML = tankStations[i]['name'] + ' |' + tankStations[i]['address'];
            document.getElementById("tankStationSelect").appendChild(option);
        }
    });
}

function getTankStationDetails()
{
    const region = document.getElementById("regionSelect").value;
    const tankStation = document.getElementById("tankStationSelect").value;
    let fuel = document.getElementById("fuelTypeInput").value;
    fuel = fuel.replace(" ", "-");

    $.ajax({
        type: "POST",
        url: "/vehicle/getTankStation",
        data: { region: region, fuel: fuel }
    }).done(function(data)
    {
        const tankStations = JSON.parse(data);
        for(let i = 0; i < tankStations.length; i++)
        {
            if(tankStations[i]['name'] + ' | ' + tankStations[i]['address'] === tankStation)
            {
                const price = tankStations[i]['price'].replace(",", ".");
                document.getElementById("pricePerLiterTankInput").value = new Number(price);
            }
        }
    });
    renderMap();
}

function priceUpdate()
{
    let liters;
    let pricePerLiter;

    if(document.getElementById("litersTankInput").value)
    {
        liters = document.getElementById("litersTankInput").value;
    }
    else
    {
        liters = 0;
    }

    if(document.getElementById("pricePerLiterTankInput").value)
    {
        pricePerLiter = document.getElementById("pricePerLiterTankInput").value;
    }
    else
    {
        pricePerLiter = 0;
    }

    const result =  liters * pricePerLiter;
    document.getElementById("priceTankInput").value = result.toFixed(2);
}

function renderMap()
{
    const apiKey = "AIzaSyCPRJVtczSvz5xKJKSl-Edi-iFj8yPYkv8";
    const inputStr = document.getElementById("tankStationSelect").value;

    $.ajax({
        type: "POST",
        url: "/vehicle/getTankStationMap",
        data: { inputStr: inputStr}
    }).done(function(data)
    {
        const dataJson = JSON.parse(data);
        lat = dataJson.candidates[0].geometry.location.lat;
        lng = dataJson.candidates[0].geometry.location.lng;

        const lastChildToRemove = document.getElementById("map");
        lastChildToRemove.removeChild(lastChildToRemove.lastChild);

        const mapIframe = document.createElement("iframe");
        mapIframe.src = "https://www.google.com/maps/embed/v1/view?key=" + apiKey + "&center=" + lat + "," + lng + "&zoom=15";
        mapIframe.width = "400px";
        mapIframe.height = "250px";
        document.getElementById("map").appendChild(mapIframe);
    });
}

function renderMapRecordDetail()
{
    const apiKey = "AIzaSyCPRJVtczSvz5xKJKSl-Edi-iFj8yPYkv8";
    const inputStr = document.getElementById("staticTankStation").value;

    $.ajax({
        type: "POST",
        url: "/vehicle/getTankStationMapRecordDetail",
        data: { inputStr: inputStr}
    }).done(function(data)
    {
        const dataJson = JSON.parse(data);
        lat = dataJson.candidates[0].geometry.location.lat;
        lng = dataJson.candidates[0].geometry.location.lng;

        const lastChildToRemove = document.getElementById("map");
        lastChildToRemove.removeChild(lastChildToRemove.lastChild);

        const mapIframe = document.createElement("iframe");
        mapIframe.src = "https://www.google.com/maps/embed/v1/view?key=" + apiKey + "&center=" + lat + "," + lng + "&zoom=15";
        mapIframe.width = "110%";
        mapIframe.height = "300px";
        document.getElementById("map").appendChild(mapIframe);
    });
}

function addEvent()
{
    renderMapRecordDetail();
}