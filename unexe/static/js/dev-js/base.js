//----------------------------------------iwidget global settings class --------------------------------------//
function IwidgetUtil()
{
	// Error message codes - code number should match the one on the 
    this.INACTIVE        = -1;
    this.NOT_FOUND       = -2;
    this.ALREADY_EXIST   = -3;
    
	//variables to hold important URL locations
	this.baseURL   	    = 'http://iwidget.up-ltd.co.uk/';
	this.mediaURL  		= this.baseURL+'media/';
	this.staticURL 		= this.baseURL+'static/';
	this.usericon  		= this.staticURL+'images/usericon.png'; //icon to show user position on map
	
	//variables of django URL string
	this.index	   	   = "index";
	this.dashboard 	   = "dashboard";
	this.household 	   = "household";
	this.getuser   	   = "getuser";
	this.gethousehold  = "gethouseho";
	this.getforecast   = "getforecast";
	this.getcompare    = "getcompare";
	this.ukcsconfirm   = "ukcsregistrationconfirm";
	
	//this.gethousehold  = "superuser";
	//variables of form id (DOM)
	this.loginform 	   = "#login-form";
	this.passwordform  = "#password-form";
	this.profileform   = "#profile-form";
	this.householdform = "#household-form";
	this.forecastform  = "#forecast-form";
	this.compareuc32form = "#compareuc32-form";
	this.c_uc32form    = "#c_uc32-form";
	this.c_uc52form    = "#c_uc52-form";
	this.c_uc53form    = "#c_uc53-form";
	this.c_uc41form    = "#c_uc41-form";
	this.c_uc33form    = "#c_uc33-form";
	this.c_uc34form    = "#c_uc34-form";	
	this.ukcsregform   = "#ukcsreg-form";
	this.mapcontainer  = "map"; //map container id (DOM) without # sign.
	//variables to hold id (DOM) of forms alert box
	this.loginmsg     = "#login-msg";
	this.passwordmsg  = "#password-msg";
	this.profilemsg   = "#profile-msg";
	this.householdmsg = "#household-msg";
	this.householdmsg2 = "#household-msg-bottom";
	this.forecastmsg  = "#forecast-msg";
	this.compareuc32msg  = "#compareuc32-msg";
	this.c_uc52msg    = "#c_uc52-msg";
	this.c_uc53msg    = "#c_uc53-msg";
	this.c_uc33msg    = "#c_uc33-msg";
	this.c_uc34msg    = "#c_uc34-msg";	
	this.c_uc32msg    = "#c_uc32-msg";
	this.c_uc41msg    = "#c_uc41-msg";
	this.ukcsregmsg   = "#ukcsreg-msg";
	
	
	//global unexpected error message
	this.unexpectederror = "Unexpected error: Please try again later.";
	this.currency     = "£"; //currency to be used to show cost
	
}//--end class
//---------------------------------------------------End class-------------------------------------------------//
iwidgetutil = new IwidgetUtil();

//------------------------------------------------HashTable Class----------------------------------------------//
function HashtableUtil()
{
    this.length = 0;
    this.items = {};
    /*
    for (var p in obj) {
        if (obj.hasOwnProperty(p)) {
            this.items[p] = obj[p];
            this.length++;
        }
    }*/

    this.setItem = function(key, value)
    {
        var previous = undefined;
        if (this.hasItem(key)) {
            previous = this.items[key];
        }
        else {
            this.length++;
        }
        this.items[key] = value;
        return previous;
    }

    this.getItem = function(key) {
        return this.hasItem(key) ? this.items[key] : undefined;
    }

    this.hasItem = function(key)
    {
        return this.items.hasOwnProperty(key);
    }
   
    this.removeItem = function(key)
    {
        if (this.hasItem(key)) {
            previous = this.items[key];
            this.length--;
            delete this.items[key];
            return previous;
        }
        else {
            return undefined;
        }
    }

    this.keys = function()
    {
        var keys = [];
        for (var k in this.items) {
            if (this.hasItem(k)) {
                keys.push(k);
            }
        }
        return keys;
    }

    this.values = function()
    {
        var values = [];
        for (var k in this.items) {
            if (this.hasItem(k)) {
                values.push(this.items[k]);
            }
        }
        return values;
    }

    this.each = function(fn) {
        for (var k in this.items) {
            if (this.hasItem(k)) {
                fn(k, this.items[k]);
            }
        }
    }

    this.clear = function()
    {
        this.items = {}
        this.length = 0;
    }
    
    this.empty = function()
    {
    	if(this.length==0)
    		return true;
    	else
    		return false;
    }
}
//---------------------------------------------------------End class-------------------------------------------------//
hashtableutil    = new HashtableUtil();

//---------------------------------------------------Math utility class ---------------------------------------------//
function MathUtil()
{
	/* This function converts string to float
	 * num: number to convert
	 * return: float equivalent of num
	 */
	this.stringTofloat = function(num)
	{
		return parseFloat(num);
	}
	
	/* Formats any number for "num" number of trailing decimals
	 * fvalue: float value for formatting
	 * num: number of desired number of digits
	 */
	this.floatFixed = function(fvalue,num)
	{
		return fvalue.toFixed(num);
	}
}
//---------------------------------------------------------End class-------------------------------------------------//
mathutil  = new MathUtil();

//------------------------------------------String utility class ---------------------------------------------//
function StringUtil()
{
	this.matchRegex = function(searchInto,regexExpr)
	{
           if(searchInto.match(regexExpr)==null)
	     return false;
	   else
	     return true;
	}

	this.matchregex = function(pattern, keyword)
	{
	    var patt1=new RegExp(pattern);
	    return patt1.test(keyword); //return true if match
	}//end function

	//simple keyword search method
	this.matchstring = function(searchstring, keyword)
	{
	    if(searchstring.search(keyword)==-1)
		return false;
	    else
		return true;
	}
	
	//method to get substring at specified position and character
	this.getSubscharfrom = function(str,ch)
	{		
	    var index = str.indexOf(ch);
	    if(index==-1)
	       return -1;
	    else
	       return str.substring(index+1,str.length);
	}
	
	/* method to get substring at specified position and character
	 * str: string to search for character (ch)
	 * ch: character to search in string (str)
	 * return: -1 indicate not found
	 */	
	this.getSubscharbefore = function(str,ch)
	{
	  var index = str.indexOf(ch);
	  if(index==-1)
	    return -1;
	  else	
	    return str.substring(0,index);
	}	
	
	/* This method count word excluding of spaces
	 * value: It is a text string
	 */
	this.countWord = function(value)	
	{
      //var value = $(id).val();
      var regex = /\s+/gi;
      return  value.trim().replace(regex, ' ').split(' ').length;
	}

	this.countChar = function(value,trails)
	{
    	  //var value = $(id).val();
      var regex = /\s+/gi;
	  if (typeof trails==='undefined')
    	     return value.length;
	  else
	  {
	     if(trails)
	        return value.trim().length;
	     else
		return value.length;
	  }//--end else
    	  //var charCountNoSpace = value.replace(regex, '').length;
	}//--end function

    this.stripHTML = function(html)
	{
	   var tmp = document.createElement("DIV");
	   tmp.innerHTML = html;
	   return tmp.textContent || tmp.innerText;
	}//--end function
        
    /*This method find the . and return only the file name
     * filename: it is a full filename+extension
    */
    this.getFilename = function(filename)
    {
       return filename.substr(0, filename.lastIndexOf('.'));
    }//--end function

    /*This method find the . and return only the extension
     * filename: it is a full filename+extension
     */
    this.getFileext = function(filename)
    {
       return filename.split('.').pop();
    }//--end function

   this.stringTojson = function(json)
   {
      if(typeof json === 'string') // if string variable
    	  return jQuery.parseJSON(json); // convert to array
      else
    	  return null;
   }//--end function
}
//---------------------------------------------------End class-------------------------------------------------//
stringutil = new StringUtil();

//------------------------------------------DOM utility class -------------------------------------------------//
function DomUtil()
{
	
	/*
	 * This method sets the css class to DOM element
	 * id: Element id
	 * cls: css class to add
	 */
    this.setCssclass = function(id,cls)
    {
	    $(id).addClass(cls);
    }

	/*
	 * This method removes the css class from DOM element
	 * id: Element id
	 * cls: css class to add
	 */	
    this.removeCssclass = function(id,cls)
    {
	    $(id).removeClass(cls);
    }	
    
    /* 
     * This method check existence of class in div
     * id: Element id
     * cls: css class to check for existence
     * return: true if file exists otheriwise false
     */
    this.hasCssclass = function(id,cls)
    {
    	return $(id).hasClass(cls);
    }
    
    /* This method search for attribute value in giving DOM element
     * id: DOM element id
     * attr: DOM element attribute
     * return: DOM element attribute value
     */
    this.getattrvalue = function(id,attr)
    {
    	return $(id).prop(attr);
    }
    /*
     * This method sets the style of dom object, it might fail
     * if the css property is not supported by the the object
     * id: DOM object
     * attr: css attribute
     * val: css attribute value
     */
    this.setstyle = function(id,attr,val)
    {
    	$(id).css(attr,val);
    }//--end function
    
    //delays execution of the provided function, please enclose your function inside braces: function(){}
    this.setdelay = function(func,delay)
    {
    	window.setTimeout(func, delay);
    }//--end
    
    this.delay = function(ms) 
    {
    	ms += new Date().getTime();
    	while (new Date() < ms){}
    }//--end
    
    /* This method generates CSRF token and 
     * is copied from the django website. Where there is no
     * form then this function can be used to obtain CSRF token
     * for ajax request
     */
    this.getcsrftoken = function(name) 
    {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }//--end function   
    
    //list: it is an array with item options to be displayed in dropdown list
    this.getoption = function(list)
    {
        var option = "<option value=''>Please Select</option>";
        for (i=1;i<=list.length;i++)
           option += '<option value="'+ i + '">' + list[i-1] + '</option>';
        return option
    }//--end function
    
	/* This method remembers the currently selected bootstrap3 tab and on page reload make it focus
	 * id: tab DOM id
	 */
	this.tabfocus = function(id)
	{		
	    // on load of the page: switch to the currently selected tab
	    var hash = window.location.hash;
	    $(id+' a[href="' + hash + '"]').tab('show');		
	}//--end    
	
	/*
	 * This method returns the width of the HTML div
	 * id: is the div DOM id or class without # or preceeding # or .  
	 */
	this.getdivwidth = function(id)
	{
		return document.getElementById(id).offsetWidth;
	}//--end

	/*
	 * This method returns the height of the HTML div
	 * id: is the div DOM id or class without # or preceeding # or .  
	 */	
	this.getdivheight = function(id)
	{
		return document.getElementById(id).offsetHeight;
	}//--end

	/*
	 * This method returns the height of the HTML div
	 * id: is the div DOM id or class without # or preceeding # or .  
	 */	
	this.setdivheight = function(id,height)
	{
		return $(id).height(height);
	}//--end function	
	
	/* This method check the status of the checkbox and return value if it is checked
	 * id: DOM id of the checkbox
	 * return: checkbox value of the provided DOM id or empty string if not checked
	 */
	this.getchkboxvalue = function(id)
	{
		if($(id).is(':checked'))
			return $(id).val();
		else
			return ""; //make sure to return no value or empty string
	}//--end function

	/* This method check the status of the radiobutton and return value if it is selected
	 * id: id of he radio button (without #)
	 * return: radio button value of the provided DOM id or empty string if not checked
	 * 	  ...var id= "domid";
	 *    ...domutil.getradiovalue(name);
	 */
	this.getradiovalue = function(id)
	{
		return $('input[id='+id+']:checked').val();
		/*
		if($(id).is(':checked'))
			return $(id).val();
		else
			return ""; //make sure to return no value or empty string
		*/
	}//--end function
	
	/* This method add comma seprated value to HTML form select list 
	 * id: select DOM id
	 * list: list of values (options and text)
	 */
	this.setselect = function(id,list)
	{
		var arraylist = list.split(",");
		for(i=0;i<arraylist.length;i++)
			 $(id).append("<option value='"+arraylist[i]+"'>"+arraylist[i]+"</option>");
	}//--end function
}//--end class

//---------------------------------------------------End class-------------------------------------------------//
domutil = new DomUtil();

//------------------------------------------------DateUtil Class-------------------------------------------------//
function DateUtil()
{
	
	/* This function test if two dates are equals
	 * date1: JavaScript Date object
	 * date1: JavaScript Date object
	 * return: true or false (true if both dates are equal otherwise false)
	 * ... dateutil.isequal(new Date(2012,0,10),new Date(2012,0,10));
	 * ... return true
	 */
	this.isequal = function(date1,date2)
	{
		return (date1.valueOf() == date2.valueOf());
	}//--end function
	
	/* This method convert date string into JavaScript date object
	 * strdate: Date string in the format: yyyy-mm-dd
	 * ... strtodate("2014-12-01");
	 * 
	 */
	this.strtodate = function(strdate)
	{
		var dateParts = strdate.split("-");
		return new Date(dateParts[0], (dateParts[1] - 1), dateParts[2]);
	}//--end function
	
	/* This gets the year from the date string
	 * strdate: Date string in the format: yyyy-mm-dd
	 * ... getdateyear("01-12-2014")
	 * ... 2014
	 */	
	this.getdateyear = function(strdate)
	{
		var dateParts = strdate.split("-");
		return dateParts[2];
	}//--end function

	/* This function return the list from start to end
	 * start: start year (int)
	 * end  : end year (int)
	 * return: comma seprated list of years (string) if end<start then returns empty string
	 * ... getyearlyst(2008,2011)
	 * ... 2008,2009,2010,2011
	 */	
	this.getyearlist = function(start,end)
	{
		if(end<start)
			return "";

		var dates="";
		var count=0;
		
		for(i=start;i<=end;i++)
		{	
			if(start==end)
				dates = dates + (start++);
			else
				dates = dates + (start++)+",";
		}
		return dates;
	}//--end function	
}//--end class
//---------------------------------------------------End class-------------------------------------------------//
dateutil = new DateUtil();
	
//------------------------------------------------FormUtil Class-------------------------------------------------//
function FormUtil()
{
	this.post     = "POST";
	this.get      = "GET";
	this.async    = false;
	this.json     = "json";
	
	/* This method get the form "action" attribute value
	 * id: it is a form id (DOM)
	 * return: action attribute value - URL
	 */
	this.getAction = function(id)
	{
		return $(id).prop('action');
	}//-end

	/* This method validate the form. This relies on jquery plugin
	 * id: it is a form id (DOM)
	 * return: return false if error otherwise true
	 */	
	this.getValidation = function(id)
	{
     	var validator = $(id).validate();
	    if(validator.form())
	    	return true;
    	else
	       return false;
	}//-end
	
	/* This method submit form
	 * id: it is a form id (DOM)
	 */
	this.submitForm = function(id)
	{
	    $(id).submit();
	}//-end
	
	/* This method reset form to original state
	 * id: it is a form id (DOM)
	 */
	this.resetForm = function(id)
	{
	    $(id).trigger("reset");
	}//--end
}
//------------------------------------------------End class-------------------------------------------------//
formutil = new FormUtil();
//----------------------------------------------------Ajax class ---------------------------------------------//
function AjaxUtil()
{
	/* This is ajax post method 
	 * dataObj: This is JavaScript object contain form values (key,value)
	 * url: it is the url to sent ajax post request
	 * return: This can be anything from status code to full json reply
	 */
    this.postAjax = function(dataObj,url)
    {
    	var data = {};
		$.ajax({
		url: url,
		async: false,     //must be syncronous request! or not return ajax results
		type: 'POST',
		data: dataObj,
		dataType: 'json',	
		success: function(json)
		{
			data = json;
			
		},
		error: function(json)
		{
			data = json;
		}
	});	  
		
	return data;
	}//--end postAjax
    
	/* This is ajax get method 
	 * dataObj: This is JavaScript object contain form values (key,value)
	 * url: it is the url to sent ajax post request
	 * return: This can be anything from status code to full json reply
	 */
    this.getAjax = function(dataObj,url)
    {
    	var data = {};
		$.ajax({
		url: url,
		async: false,     //must be syncronous request! or not return ajax results
		type: 'GET',
		data: dataObj,
		dataType: 'json',	
		success: function(json)
		{
			data = json;
			
		},
		error: function(json)
		{
			data = json;
		}
	});	  
		
		return data;
	}//--end postAjax    
    
    this.ajaxEffect = function()
    {
	  $(document).ajaxStart(function(){
		  $("#overlay").height($("body").height());
		  domutil.removeCssclass("#overlay","hide");
	  });

	  $(document).ajaxComplete(function(){
		  domutil.setCssclass("#overlay","hide");
	  });
    }
}//--end class
//---------------------------------------------------End class-------------------------------------------------//
ajaxutil = new AjaxUtil();
//-------------------------------------------------------LeafletMap Class---------------------------------------------//
function LeafletUtil()
{
    var self = this;
    var map;
    this.marker=null;
    var zoom = 5;
    this.layercontrol;
    var basemap,tonermap,minimal,nightview; //variable for map layers
    var shape   = null; //variable to hold shape
	
    this.loadMap = function(id,zoomcontrol,mapbase)
    {	
       var con = {};

	   if (typeof zoomcontrol==='undefined')
	     con = {zoomControl:false};
	   else if (zoomcontrol==true)
	     con = {zoomControl:true, position:'topleft'};
	   else
	     con = {zoomControl:false};
		
	   var attribution = '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>';

           basemap = L.tileLayer(
              //'http://{s}.tile.cloudmade.com/d2d204fa6e094ad09838d20c4c021aee/997/256/{z}/{x}/{y}.png'
        	  'http://{s}.tile.osm.org/{z}/{x}/{y}.png'
              , {attribution: attribution}
           )

           tonermap = new L.StamenTileLayer("toner");

       	   var mapnik = L.tileLayer(
              'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
              , {attribution: attribution}
           )

           var blackAndWhite = L.tileLayer(
              'http://{s}.www.toolserver.org/tiles/bw-mapnik/{z}/{x}/{y}.png'
              , {attribution: attribution}
           )

           minimal = L.tileLayer(
              'http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/22677/256/{z}/{x}/{y}.png'
              , {attribution: attribution}
           )

           nightview = L.tileLayer(
              'http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/999/256/{z}/{x}/{y}.png'
              , {attribution: attribution}
           )

           var clouds = L.tileLayer('http://{s}.tile.openweathermap.org/map/clouds/{z}/{x}/{y}.png', {
              attribution: 'Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>'
              , opacity: 0.5
           })

           var wind = L.tileLayer('http://{s}.tile.openweathermap.org/map/wind/{z}/{x}/{y}.png', {
              attribution: 'Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>'
            , opacity: 0.5
           })

           var temperature = L.tileLayer('http://{s}.tile.openweathermap.org/map/temp/{z}/{x}/{y}.png', {
              attribution: 'Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>'
            , opacity: 0.5
           })

           // set up the map
           if (typeof mapbase==='undefined')
               map = new L.Map(id,{zooncontrol:true,layers:[basemap]});
	   else if(mapbase=='toner')
	       map = new L.Map(id,{zooncontrol:true,layers:[tonermap]});
	   else
	       map = new L.Map(id,{zooncontrol:true,layers:[basemap]});

	   // start the map in Exeter University
	   //imap.setView(new L.LatLng(50.737137, -3.535148),zoom);
	   
	   return map;
	}//--end load function
	
	//create map marker
	this.createMarker = function(lat,lng)
	{
		return L.marker([lat,lng]);
	}//--end

	//create marker icon from image file
	this.getIcon = function(iconfile)
    	{
       		var customIcon = L.Icon.extend({
            	options: {
            		shadowUrl: null,
            		//iconAnchor: new L.Point(32, 32),
            		iconSize:  [32, 32],
            		iconUrl: iconfile
           	}
          	});
         return new customIcon();
	}//--end icon

	//add marker to map (point format string var "lat,lng" formar
	this.addPoint = function(point,marker,layer)
	{
	  var comma = ",";
	  y = point.split(comma);
	  lng = y[1];
	  lat = y[0];

	  if (typeof layer==='undefined')                 //if default layer or direct to map
	    marker = L.marker([lat, lng]).addTo(map);
	  else
	    marker = L.marker([lat, lng]).addTo(layer);
	 return marker;
	}//--end addPoint

	//set marker icon
	this.setIcon = function(marker,iconObj) 
	{
		return marker.setIcon(iconObj);
	}
	
	//--add popup to marker
	this.addPopup = function(marker,content,open)
	{
		if(typeof open==='undefined')
			marker.bindPopup(content);
		else
			marker.bindPopup(content).openPopup();
	}//--end
    
	//focus to specific zoom and location (lat, lng)
//	this.setFocus = function(lat, lng,Zoom)
//	{
//		if(typeof zoom==='undefined')
//			map.setView(new L.LatLng(lat, lng),zoom);
//		else
//			map.setView(new L.LatLng(lat, lng),Zoom);
//	}

	this.addLayer = function(layerToadd,addTo)
	{
	    if(typeof addTo=='undefined')
	    	map.addLayer(layerToadd);
	    else
	    	addTo.addLayer(layerToadd);
	}
}//--end class

//--------------------------------------------------------End class-------------------------------------------------//
leafletutil = new LeafletUtil();
//----------------------------------------------------Chart class ---------------------------------------------//
function ChartUtil()
{
	
	/* This method create line chart for the consumer use case 3.3
	 * id: DOM id to add chart to. e.g: #id
	 * dim: Chart dimenions object. e.g: var dim = {width: 30, height: 80} 
	 * data1: This is the first line series data. e.g: 
	 * data2: This is the first line series data. e.g:
	 * 
	 */

	this.c_uc52linechart = function(id,dim,data1,data2)
	{
		var margin = {top: 30, right: 80, bottom: 110, left: 60};
	    var keys = Object.keys(data1[0]);
	    var xcord = keys[0];
	    var ycord = keys[1];

	    var svg = dimple.newSvg(id, dim.width, dim.height);
	    var parser = d3.time.format("%Y-%m-%d")
	    
	    var dateReader = function (d) { return parser.parse(d[xcord]); }
	    var start = d3.time.day.offset(d3.min(data1, dateReader), -5);
	    var end = d3.time.day.offset(d3.max(data1, dateReader), 15);

	    var myChart = new dimple.chart(svg,data1);
	    myChart.setBounds(margin.left,margin.top,dim.width-margin.right,dim.height-margin.bottom);     	
	    
    	var x = myChart.addTimeAxis("x", xcord, "%Y-%m-%d","%b %Y");
	    
	    x.overrideMin = start;
	    x.overrideMax = end;
	    x.addOrderRule(xcord);
	    x.showGridlines = true;
	    x.timePeriod = d3.time.months;
	    x.floatingBarWidth = dim.width/data1.length/2;
	    
	    var y = myChart.addMeasureAxis("y", ycord);
	    y.showGridlines = true;
	    y.tickFormat = ',.2f';  
	    y.title = "Cost (£)";
	    
	    var s1 = myChart.addSeries("Tariff1", dimple.plot.line);
	    var s2 = myChart.addSeries("Tariff2", dimple.plot.line);
	    
	    s1.lineMarkers = true;
	    s1.lineWeight = 3;
	    s1.lineMarkers = true;

	    s2.data = data2;

	    s2.lineMarkers = true;
	    s2.lineWeight = 3;
	    s2.lineMarkers = true;	    
	    

		myChart.addLegend(margin.left,0,dim.width-margin.right,20,"left");
		
	    myChart.assignColor("Tariff1", "#C0C0C0");
	    //myChart.assignColor("Area", "#8E35EF");
	    
	    myChart.draw(1500);
	    
	    /*Change tooltip data*/
	    s1.getTooltipText = function (e) {
	    	var parser   = d3.time.format("%b-%Y");
            return [
                "Date: "+ parser(new Date(e.x)),
                "Cost: £" + e.y,
                "Data: "+ e.aggField[0]
            ];
        };

	    s2.getTooltipText = function (e) {
	    	var parser   = d3.time.format("%b-%Y");
            return [
                "Date: "+ parser(new Date(e.x)),
                "Cost: £" + e.y,
                "Data: "+ e.aggField[0]                
            ];
        };	            
	}
	
	this.c_uc52comparechart = function(id,dim,data)
	{
		var margin = {top: 30, right: 80, bottom: 115, left: 60};
		var svg    = dimple.newSvg(id, dim.width, dim.height);
		// Draw a standard chart using the aggregated data
		var chart = new dimple.chart(svg, data);
		//chart.setBounds(70, 30, 505, 305);  
		chart.setBounds(margin.left,margin.top,dim.width-margin.right,dim.height-margin.bottom);
		var x = chart.addCategoryAxis("x", ["Data"]);
		x.showGridlines = true;
		x.addOrderRule(["Tariff1","Tariff2"]);
		x.title = "Tariffs";
		
		var y = chart.addMeasureAxis("y", "Cost");
		y.showGridlines = true;
		y.tickFormat = ',.2f';
		y.title = "Cost (£)";
		
		chart.addLegend(margin.left,0,dim.width-margin.right,20,"left");
		
		var s1  = chart.addSeries(["Cost", "Data"], dimple.plot.bar);
		//var s2 = chart.addSeries("Price Break", dimple.plot.line);
		//s2.data = price_break;
		chart.assignColor("Tariff1", "#C0C0C0")
		chart.draw(1500);
		
	    /*Change tooltip data*/
	    s1.getTooltipText = function (e) {
	    	var parser   = d3.time.format("%b-%Y");
            return [
                "Cost: £" + e.y,
                "Data: "+ e.x
            ];
        };		
		
		 // After drawing we can access the shapes and their associated data
	    s1.shapes.each(function(d) {

	        // Get the shape as a d3 selection
	        var shape = d3.select(this);
	        
	        //alert(d.width);
	        // Add a text label for the value
	        svg.append("text")
	
	        // Position in the centre of the shape (vertical position is
	        // manually set due to cross-browser problems with baseline)
	        .attr("x", parseFloat(shape.attr("x")) + parseFloat(shape.attr("width"))/2)
	        .attr("y", y._scale(d.height))
	        .attr("dy", "-0.5em")
	
	        // Centre align
	        .style("text-anchor", "middle")
	        .style("font-size", "10px")
	        .style("font-family", "sans-serif")
	
	        // Make it a little transparent to tone down the black
	        .style("opacity", 0.7)
	
	        // Format the number
	        .text("£"+d3.format(",.2f")(d.yValue));
        });	 		
	}
	
	this.c_uc33comparechart = function(id,dim,server_data)
	{
		var data = server_data["comparechart"];
		var start = 0;
		var end   = 10;
		var h 	  = data[0]["Units"];
	    var price_break = [      
			               { "Price Break" : "Highest", "units" :30 , "start" : start }, 
			               { "Price Break" : "Highest", "units" :30, "start" : end },
			           ];
		
		var margin = {top: 30, right: 80, bottom: 110, left: 60};
		var svg    = dimple.newSvg(id, dim.width, dim.height);
		// Draw a standard chart using the aggregated data
		var chart = new dimple.chart(svg, data);
		//chart.setBounds(70, 30, 505, 305);  
		chart.setBounds(margin.left,margin.top,dim.width-margin.right,dim.height-margin.bottom);
		var x = chart.addCategoryAxis("x", ["Data"]);
		x.showGridlines = true;
		x.addOrderRule(["Area","You"]);
		var y = chart.addMeasureAxis("y", "Units");
		y.showGridlines = true;
	    y.tickFormat = ',.2f';  
	    y.title = "Units (m3)";
		//x.overrideMin = 0;
		//x.overrideMax = 5;
		//y.tickFormat = '%';
		//y.overrideMin = 0;
		//y.overrideMax = 1.0;
		//y.showPercent = true
		chart.addLegend(65, 10, dim.width-margin.right, 20, "right");
		
		var s1  = chart.addSeries(["Units", "Data"], dimple.plot.bar);
		//var s2 = chart.addSeries("Price Break", dimple.plot.line);
		//s2.data = price_break;
		chart.assignColor(server_data["area_label"], "#C0C0C0");
		chart.draw(1500);
		x.titleShape.text(server_data["data_label"]);
		y.titleShape.text(server_data["units_label"]);

	    /*Change tooltip data*/
	    s1.getTooltipText = function (e) {
	    	var parser   = d3.time.format("%b-%Y");
            return [
                server_data["units_label"] + ": " + e.y +" m3",
                server_data["data_label"] + ": "+ e.x
            ];
        };
        
		 // After drawing we can access the shapes and their associated data
	    s1.shapes.each(function(d) {

	        // Get the shape as a d3 selection
	        var shape = d3.select(this);
	        
	        //alert(d.width);
	        // Add a text label for the value
	        svg.append("text")
	
	        // Position in the centre of the shape (vertical position is
	        // manually set due to cross-browser problems with baseline)
	        .attr("x", parseFloat(shape.attr("x")) + parseFloat(shape.attr("width"))/2)
	        .attr("y", y._scale(d.height))
	        .attr("dy", "-1em")
	
	        // Centre align
	        .style("text-anchor", "middle")
	        .style("font-size", "10px")
	        .style("font-family", "sans-serif")
	
	        // Make it a little transparent to tone down the black
	        .style("opacity", 0.7)
	
	        // Format the number
	        .text(d3.format(",.2f")(d.yValue)+ " m3");
        });	 		
	}

	this.c_uc34comparechart = function(id,dim,data)
	{
		var start = 0;
		var end   = 10;
		var h 	  = data[0]["Units"];
	    var price_break = [      
			               { "Price Break" : "Highest", "units" :30 , "start" : start }, 
			               { "Price Break" : "Highest", "units" :30, "start" : end },
			           ];
		
		var margin = {top: 30, right: 80, bottom: 110, left: 60};
		var svg    = dimple.newSvg(id, dim.width, dim.height);
		// Draw a standard chart using the aggregated data
		var chart = new dimple.chart(svg, data);
		//chart.setBounds(70, 30, 505, 305);  
		chart.setBounds(margin.left,margin.top,dim.width-margin.right,dim.height-margin.bottom);
		var x = chart.addCategoryAxis("x", ["Data"]);
		x.showGridlines = true;
		x.addOrderRule(["Efficient User","You"]);
		var y = chart.addMeasureAxis("y", "Units");
		y.showGridlines = true;
	    y.tickFormat = ',.2f';  
	    y.title = "Units (m3)";
		
		//x.overrideMin = 0;
		//x.overrideMax = 5;
		//y.tickFormat = '%';
		//y.overrideMin = 0;
		//y.overrideMax = 1.0;
		//y.showPercent = true
		chart.addLegend(65, 10, dim.width-margin.right, 20, "right");
		
		var s1  = chart.addSeries(["Units", "Data"], dimple.plot.bar);
		//var s2 = chart.addSeries("Price Break", dimple.plot.line);
		//s2.data = price_break;
		chart.assignColor("Efficient User", "#C0C0C0")
		chart.draw(1500);
		
	    /*Change tooltip data*/
	    s1.getTooltipText = function (e) {
	    	var parser   = d3.time.format("%b-%Y");
            return [
                "Units: " + e.y +" m3",
                "Data: "+ e.x
            ];
        };
        
		 // After drawing we can access the shapes and their associated data
	    s1.shapes.each(function(d) {

	        // Get the shape as a d3 selection
	        var shape = d3.select(this);
	        
	        //alert(d.width);
	        // Add a text label for the value
	        svg.append("text")
	
	        // Position in the centre of the shape (vertical position is
	        // manually set due to cross-browser problems with baseline)
	        .attr("x", parseFloat(shape.attr("x")) + parseFloat(shape.attr("width"))/2)
	        .attr("y", y._scale(d.height))
	        .attr("dy", "-1em")
	
	        // Centre align
	        .style("text-anchor", "middle")
	        .style("font-size", "10px")
	        .style("font-family", "sans-serif")
	
	        // Make it a little transparent to tone down the black
	        .style("opacity", 0.7)
	
	        // Format the number
	        .text(d3.format(",.2f")(d.yValue)+ " m3");
        });	 		
	}	
	
	this.c_uc52donutchart = function(id,dim,data)
	{
		//var margin = {top: 5, right: 80, bottom: 30, left: 50};
		var svg = d3.select(id).append("svg")
				  .attr("width",  dim.width)
				  .attr("height", dim.height);	
		
		svg.append("g").attr("id","units");
		Donut3D.draw("units", data, 150, 150, 130, 100, 30, 0.4);
	}
	
	/*
	this.c_uc52linechart1 = function(id,dim,data1,data2)
	{
		var margin = {top: 30, right: 80, bottom: 110, left: 60};
	    var keys = Object.keys(data1[0]);
	    var xcord = keys[0];
	    var ycord = keys[1];
	    var svg = dimple.newSvg(id, dim.width, dim.height);
	    var myChart = new dimple.chart(svg,data1);
	    myChart.setBounds(margin.left,margin.top,dim.width-margin.right,dim.height-margin.bottom);
	    var x = myChart.addTimeAxis("x", xcord, "%Y-%m-%dT%H:%M:%S.%L000000+0000","%b %Y");
    	//var x = myChart.addTimeAxis("x", xcord, "%Y-%m-%dT%H:%M:%S.%LZ","%b %Y");

    	//alert(JSON.stringify(data1));
	    //x.overrideMin = "2008-07-16T07:00:00.000000000+0000";
	    //x.overrideMax = "2008-07-16T16:00:00.000000000+0000";    	
	    x.addOrderRule(xcord);
	    x.showGridlines = true;
	    x.timePeriod = d3.time.months;
	    x.floatingBarWidth = dim.width/data1.length/2;
	    
	    var y = myChart.addMeasureAxis("y", ycord);
	    y.showGridlines = true;
	    y.tickFormat = ',.2f';  
	    
	    var s1 = myChart.addSeries("Day Units", dimple.plot.line);
	    var s2 = myChart.addSeries("Night Units", dimple.plot.line);
	    s2.data = data2;

	    //s1.lineMarkers = true;
	    //s1.lineWeight = 3;
	    //s1.lineMarkers = true;
	    /*
	    s2.data = data2;
	    s2.lineMarkers = true;
	    s2.lineWeight = 3;
	    s2.lineMarkers = true;	    
	    */
		//myChart.addLegend(65,10,dim.width-margin.right,20,"right");
	    //myChart.draw(1500);    	
	//}
	
	/* This method create line chart for the consumer use case 3.3
	 * id: DOM id to add chart to. e.g: #id
	 * dim: Chart dimenions object. e.g: var dim = {width: 30, height: 80} 
	 * data1: This is the first line series data. e.g: 
	 * data2: This is the first line series data. e.g:
	 * 
	 */

	this.c_uc33linechart = function(id,dim,server_data)
	{
		var data1 = server_data["you"]["data"];
		var data2 = server_data["area"]["data"];
		var margin = {top: 30, right: 80, bottom: 110, left: 60};
	    var keys = Object.keys(data1[0]);
	    var xcord = keys[0];
	    var ycord = keys[1];
	    var svg = dimple.newSvg(id, dim.width, dim.height);
	    var parser = d3.time.format("%Y-%m-%d");

	    var dateReader = function (d) { return parser.parse(d[xcord]); }
	    var start = d3.time.day.offset(d3.min(data1, dateReader), -5);
	    var end = d3.time.day.offset(d3.max(data1, dateReader), 15);

	    var myChart = new dimple.chart(svg,data1);
	    myChart.setBounds(margin.left,margin.top,dim.width-margin.right,dim.height-margin.bottom);

    	var x = myChart.addTimeAxis("x", xcord, "%Y-%m-%d","%m/%Y");

	    x.overrideMin = start;
	    x.overrideMax = end;
	    x.addOrderRule(xcord);
	    x.showGridlines = true;
	    x.timePeriod = d3.time.months;
	    x.floatingBarWidth = dim.width/data1.length/2;
	    x.title = server_data["date_label"]

	    var y = myChart.addMeasureAxis("y", ycord);
	    y.showGridlines = true;
	    y.tickFormat = ',.2f';
	    y.title = server_data['units_label'] + " (m3)";

	    var s1 = myChart.addSeries(server_data["you_label"], dimple.plot.line);
	    var s2 = myChart.addSeries(server_data["area_label"], dimple.plot.line);

	    s1.lineMarkers = true;
	    s1.lineWeight = 3;
	    s1.lineMarkers = true;

	    s2.data = data2;

	    s2.lineMarkers = true;
	    s2.lineWeight = 3;
	    s2.lineMarkers = true;

		myChart.addLegend(65,10,dim.width-margin.right,20,"right");

	    myChart.assignColor(server_data["area_label"], "#C0C0C0");
	    //myChart.assignColor("Area", "#8E35EF");

	    myChart.draw(1500);
		x.titleShape.text(server_data["data_label"]);
		y.titleShape.text(server_data["units_label"]);

	    /*Change tooltip data*/
	    s1.getTooltipText = function (e) {
	    	var parser   = d3.time.format("%b-%Y");
            return [
                server_data["date_label"] + ": "+ parser(new Date(e.x)),
                server_data["units_label"] + ": " + e.y+ " m3",
                server_data["data_label"] + ":" + e.aggField[0]
            ];
        };

	    s2.getTooltipText = function (e) {
	    	var parser   = d3.time.format("%b-%Y");
            return [
				server_data["date_label"] + ": "+ parser(new Date(e.x)),
				server_data["units_label"] + ": " + e.y+ " m3",
				server_data["data_label"] + ":" + e.aggField[0]
            ];
        };
	}
	
	/* This method create line chart for the consumer use case 3.4
	 * id: DOM id to add chart to. e.g: #id
	 * dim: Chart dimenions object. e.g: var dim = {width: 30, height: 80} 
	 * data1: This is the first line series data. e.g: 
	 * data2: This is the first line series data. e.g:
	 * 
	 */

	this.c_uc34linechart = function(id,dim,data1,data2)
	{
		var margin = {top: 30, right: 80, bottom: 110, left: 60};
	    var keys = Object.keys(data1[0]);
	    var xcord = keys[0];
	    var ycord = keys[1];
	    var svg = dimple.newSvg(id, dim.width, dim.height);
	    var parser = d3.time.format("%Y-%m-%d")
	    
	    var dateReader = function (d) { return parser.parse(d[xcord]); }
	    var start = d3.time.day.offset(d3.min(data1, dateReader), -5);
	    var end = d3.time.day.offset(d3.max(data1, dateReader), 15);

	    var myChart = new dimple.chart(svg,data1);
	    myChart.setBounds(margin.left,margin.top,dim.width-margin.right,dim.height-margin.bottom);     	
	    
    	var x = myChart.addTimeAxis("x", xcord, "%Y-%m-%d","%b %Y");
	    
	    x.overrideMin = start;
	    x.overrideMax = end;
	    x.addOrderRule(xcord);
	    x.showGridlines = true;
	    x.timePeriod = d3.time.months;
	    x.floatingBarWidth = dim.width/data1.length/2;
	    x.title = "Date";
	    
	    var y = myChart.addMeasureAxis("y", ycord);
	    y.showGridlines = true;
	    y.tickFormat = ',.2f';  
	    y.title = "Units (m3)";
	    
	    var s1 = myChart.addSeries("You", dimple.plot.line);
	    var s2 = myChart.addSeries("Efficient User", dimple.plot.line);
	    
	    s1.lineMarkers = true;
	    s1.lineWeight = 3;
	    s1.lineMarkers = true;

	    s2.data = data2;

	    s2.lineMarkers = true;
	    s2.lineWeight = 3;
	    s2.lineMarkers = true;	    
	    
		myChart.addLegend(65,10,dim.width-margin.right,20,"right");
		
	    myChart.assignColor("Efficient User", "#C0C0C0");
	    //myChart.assignColor("Area", "#8E35EF");
	    
	    myChart.draw(1500);    
	    
	    /*Change tooltip data*/
	    s1.getTooltipText = function (e) {
	    	var parser   = d3.time.format("%b-%Y");
            return [
                "Date: "+ parser(new Date(e.x)),
                "Units: " + e.y+ " m3",
                "Data: "+ e.aggField[0]
            ];
        };

	    s2.getTooltipText = function (e) {
	    	var parser   = d3.time.format("%b-%Y");
            return [
                "Date: "+ parser(new Date(e.x)),
                "Units: " + e.y+ " m3",
                "Data: "+ e.aggField[0]                
            ];
        };		    
	}
	
	/* This method create line chart for the consumer use case 5.2
	 * id: DOM id to add chart to. e.g: #id
	 * dim: Chart dimenions object. e.g: var dim = {width: 30, height: 80} 
	 * data1: This is the first line series data. e.g: 
	 * data2: This is the first line series data. e.g:
	 * type: This is the optional parameter and default axis is format is:"%Y-%m-%d". If specify then chart axis needs to be adjusted. e.g: chartutil.c_uc52linechart(id,dim,data1,data2,"days");
	 * 
	 */
	/*
	this.c_uc52linechart = function(id,dim,data1,data2,type)
	{
		var margin = {top: 30, right: 80, bottom: 110, left: 60};
	    var keys = Object.keys(data1[0]);
	    var xcord = keys[0];
	    var ycord = keys[1];
	    var svg = dimple.newSvg(id, dim.width, dim.height);
	    if (typeof type==='undefined')
	    	var parser = d3.time.format("%Y-%m-%d")
	    else
	    	var parser = d3.time.format.utc("%Y-%m-%dT%H:%M:%S.%LZ");
	    
	    var dateReader = function (d) { return parser.parse(d[xcord]); }
	    var start = d3.time.day.offset(d3.min(data1, dateReader), -5);
	    var end = d3.time.day.offset(d3.max(data1, dateReader), 15);
	    //alert(JSON.stringify(data1));
	    var myChart = new dimple.chart(svg,data1);
	    myChart.setBounds(margin.left,margin.top,dim.width-margin.right,dim.height-margin.bottom);     	
	    
	    if (typeof type==='undefined')
	    	var x = myChart.addTimeAxis("x", xcord, "%Y-%m-%d","%b %Y");
	    else
	    	var x = myChart.addTimeAxis("x", xcord, "%Y-%m-%dT%H:%M:%S.%LZ","%b %Y");
	    
	    x.overrideMin = start;
	    x.overrideMax = end;
	    x.addOrderRule(xcord);
	    x.showGridlines = true;
	    x.timePeriod = d3.time.months;
	    x.floatingBarWidth = dim.width/data1.length/2;
	    
	    var y = myChart.addMeasureAxis("y", ycord);
	    y.showGridlines = true;
	    y.tickFormat = ',.2f';  
	    
	    var s1 = myChart.addSeries("Day Units", dimple.plot.line);
	    var s2 = myChart.addSeries("Night Units", dimple.plot.line);
	    
	    s1.lineMarkers = true;
	    s1.lineWeight = 3;
	    s1.lineMarkers = true;

	    s2.data = data2;

	    s2.lineMarkers = true;
	    s2.lineWeight = 3;
	    s2.lineMarkers = true;	    
	    
		myChart.addLegend(65,10,dim.width-margin.right,20,"right");
		
	    myChart.assignColor("Night Units", "#C0C0C0");
	    myChart.assignColor("Day Units", "#8E35EF");
	    
	    myChart.draw(1500);
	    
	}
	*/
	this.uc32barplot1 = function(id,dim,data)
	{
		//var data = '[{"Units": "273.881880739", "Cost": "273.881880739", "Data": "DMA", "Period": "12"}, {"Units": "9.47616916667", "Cost": "9.47616916667", "Data": "You", "Period": "12"}, {"Units": "115.149275501", "Cost": "115.149275501", "Data": "DMA", "Period": "6"}, {"Units": "10.793005", "Cost": "10.793005", "Data": "You", "Period": "6"}, {"Units": "74.2850266667", "Cost": "74.2850266667", "Data": "DMA", "Period": "4"}, {"Units": "11.161", "Cost": "11.161", "Data": "You", "Period": "4"}]';
		var margin = {top: 30, right: 80, bottom: 110, left: 60};
		var svg = dimple.newSvg(id, dim.width, dim.height);
	    //chart = null,
	    //s = null,
	    //x = null;
		// Draw a standard chart using the aggregated data
		var chart = new dimple.chart(svg, data);
		//chart.setBounds(70, 30, 505, 305);  
		chart.setBounds(margin.left,margin.top,dim.width-margin.right,dim.height-margin.bottom);
		var x = chart.addCategoryAxis("x", ["Period", "Data"]);
		x.showGridlines = true;
		//x.addGroupOrderRule([2012, 2013]);
		x.addGroupOrderRule("Period");
		
		var y = chart.addMeasureAxis("y", "Cost");
		y.showGridlines = true;
		y.tickFormat = ',.2f';
		y.title = "Cost(£)";
		chart.addLegend(65, 10, 510, 20, "right");
		var s = chart.addSeries(["Cost", "Data"], dimple.plot.bar);
		chart.assignColor("DMA", "#C0C0C0");
		chart.assignColor("Area", "#C0C0C0")
		chart.assignColor("Consumer", "#C0C0C0");
		chart.assignColor("Most Efficient", "#C0C0C0");
		chart.assignColor("Electricity", "#800080");
		/*s.addEventHandler("click", function (e) { 
		    d3.select("#infoLabel").text("In " + e.seriesValue[1] + " we sold " + e.seriesValue[0] + " " + e.xValue + "s!");
		});*/
		chart.draw(1500);		

	    /*Change tooltip data*/
	    s.getTooltipText = function (e) {
            return [
                "Cost: £" + e.y,
                "Period: "+ e.x,
                "Data: "+ e.aggField[1] 
            ];
        };
        
		 // After drawing we can access the shapes and their associated data
	    s.shapes.each(function(d) {

	        // Get the shape as a d3 selection
	        var shape = d3.select(this);
	        
	        //alert(d.width);
	        // Add a text label for the value
	        svg.append("text")
	
	        // Position in the centre of the shape (vertical position is
	        // manually set due to cross-browser problems with baseline)
	        .attr("x", parseFloat(shape.attr("x")) + parseFloat(shape.attr("width"))/2)
	        .attr("y", y._scale(d.height))
	        .attr("dy", "-1em")
	
	        // Centre align
	        .style("text-anchor", "middle")
	        .style("font-size", "10px")
	        .style("font-family", "sans-serif")
	
	        // Make it a little transparent to tone down the black
	        .style("opacity", 0.7)
	
	        // Format the number
	        .text("£"+d3.format(",.2f")(d.yValue));
        });			
	}//--end function
	
	this.barplot = function(id,dim,data,price_break)
	{
		var margin = {top: 30, right: 80, bottom: 110, left: 60};
	    var keys = Object.keys(data[0]);
	    var xcord = keys[0];
	    var ycord = keys[1];

	    var svg = dimple.newSvg(id, dim.width, dim.height);
	    var parser = d3.time.format("%Y-%m-%d")
	    var dateReader = function (d) { return parser.parse(d[xcord]); }
	    var start = d3.time.month.offset(d3.min(data, dateReader), -1);
	    var end = d3.time.month.offset(d3.max(data, dateReader), 1);

	    var myChart = new dimple.chart(svg,data);
	    //myChart.setBounds(60, 30, 505, 305);        
	    myChart.setBounds(margin.left,margin.top,dim.width-margin.right,dim.height-margin.bottom);
	    //var x = myChart.addCategoryAxis("x", xcord);
	    var x = myChart.addTimeAxis("x", xcord, "%Y-%m-%d","%b %Y");
	    x.overrideMin = start;
	    x.overrideMax = end;
	    x.addOrderRule(xcord);
	    x.showGridlines = true;
	    x.timePeriod = d3.time.months;
	    x.floatingBarWidth = dim.width/data.length/2;
	    
	    var y = myChart.addMeasureAxis("y", ycord);
	    y.showGridlines = true;
	    y.tickFormat = ',.2f';    
	    y.title = "Cost (£)";
	    
	    var s1 = myChart.addSeries(null, dimple.plot.bar);
	    var s2 = myChart.addSeries(null, dimple.plot.line);
	    var s3 = myChart.addSeries("Price Break", dimple.plot.line);

	    s1.getTooltipText = function (e) {
	    	var parser   = d3.time.format("%b-%Y");
            return [
                    "Date: "+ parser(new Date(e.x)),
                    "Cost: £" + e.y
            ];
        };
        
	    s3.getTooltipText = function (e) {
            return [
                "Price: "+ e.aggField[0],
                "Cost: £" + e.y
            ];
        };        
	    
	    s2.lineMarkers = true;
	    s2.lineWeight = 3;
	    s2.lineMarkers = true;
	    
	    s3.data = price_break;
	    myChart.draw(1500);
	    
		 // After drawing we can access the shapes and their associated data
	    s1.shapes.each(function(d) {

	        // Get the shape as a d3 selection
	        var shape = d3.select(this);
	        
	        //alert(d.width);
	        // Add a text label for the value
	        svg.append("text")
	
	        // Position in the centre of the shape (vertical position is
	        // manually set due to cross-browser problems with baseline)
	        .attr("x", parseFloat(shape.attr("x")) + parseFloat(shape.attr("width"))/2)
	        .attr("y", y._scale(d.height))
	        .attr("dy", "-1em")
	
	        // Centre align
	        .style("text-anchor", "middle")
	        .style("font-size", "10px")
	        .style("font-family", "sans-serif")
	
	        // Make it a little transparent to tone down the black
	        .style("opacity", 0.7)
	
	        // Format the number
	        .text("£"+d3.format(",.2f")(d.yValue));
        });	 	    
	}

/*
	this.barplot = function(id,dim,data)
	{
	    keys = Object.keys(data[0]);
	    var xcord = keys[0];
	    var ycord = keys[1];
	    var svg = dimple.newSvg(id, dim.width, dim.height);
	                
	    var myChart = new dimple.chart(svg,data);
	    //myChart.setStoryboard("date");
	    myChart.setBounds(60, 30, 505, 305);	    
	    //var x = myChart.addTimeAxis("x", xcord, "%Y-%m-%d","%b %Y");
	    
	    var x = myChart.addCategoryAxis("x", xcord);
	    //x.dateParseFormat = "%d-%m-%Y";
	    //x.addOrderRule(xcord);
	    //x.addGroupOrderRule("Date");
	    x.showGridlines = true;
	    
	    var y = myChart.addMeasureAxis("y", ycord);
	    y.tickFormat = ',.2f'; 
	    y.showGridlines = true;	
	    
	    var s = myChart.addSeries(null, dimple.plot.bar);
	    var s1 = myChart.addSeries(null, dimple.plot.line);
		s1.lineWeight = 3;
		s1.lineMarkers = true;
	    //s.barGap = 0;
		//s.addEventHandler("mouseover", onHover);
	    myChart.draw(1500);

	 // After drawing we can access the shapes and their associated data
	    s.shapes.each(function(d) {

            // Get the shape as a d3 selection
            var shape = d3.select(this);
            
            //alert(d.width);
            // Add a text label for the value
            svg.append("text")

            // Position in the centre of the shape (vertical position is
            // manually set due to cross-browser problems with baseline)
            .attr("x", parseFloat(shape.attr("x")) + parseFloat(shape.attr("width"))/2)
            .attr("y", y._scale(d.height))
            .attr("dy", "-1em")

            // Centre align
            .style("text-anchor", "middle")
            .style("font-size", "10px")
            .style("font-family", "sans-serif")

            // Make it a little transparent to tone down the black
            .style("opacity", 0.7)

            // Format the number
            .text(d3.format(",.2f")(d.yValue));
        });	   
	}//--end function
	*/
}//--end class
//---------------------------------------------------End class-------------------------------------------------//
chartutil = new ChartUtil();

//-------------------------------------------------------AppUtil Class---------------------------------------------//
function AppUtil()
{	
    // global hook - unblock UI when ajax request completes
	//$(document).ajaxStart($.blockUI).ajaxStop($.unblockUI);
	/*Following are bootstrap css classed. We can move it above to global iwidetutil class*/
	var alertclass  = "alert ";
	var dangerclass = alertclass + "alert-danger";
	var successclass = alertclass + "alert-success";
		
	/*initialisation function, containing most of the logic when the * dashboard page (inclusive of sidebar.html) will be loaded.
	 * initval: array values to passed from the base.html. it can be any value required into init() 
	 */ 
	this.init = function(initval) 
	{
		
		/* This piece of code initialise the map
		 * and add it to the side bar of the map represented with id (DOM)
		 */
//        leafletutil.loadMap(iwidgetutil.mapcontainer);
//        var lat = 50.7236000; //initial lat
//        var lng = -3.5275100; //initial lng
//        var marker = leafletutil.createMarker(lat, lng); //create marker
//        var icon   = leafletutil.getIcon(iwidgetutil.usericon); //create icon
//        leafletutil.setIcon(marker,icon);	//set icon
//        leafletutil.addLayer(marker);	//add to map
//        //var content = "<html><address><strong>"+initval[0]+"<br>Exeter, UK</strong></address></html>";	//this content can be geolocated address
//        leafletutil.addPopup(marker,content,true);	//add popup to marker
//        leafletutil.setFocus(lat,lng,16);		//focus the map
        this.inithousehold();
        this.initpanel();
   
	}//--end init
		
	/*
	 * This function initialises the household form with relevant form values 
	 */
	this.inithousehold = function()
	{
        /*This small piece of code create the form dropdown option with values 
         *	from 1 to 100. the return value can then easily to append to any dropdown  
         */
        //var numbers = 100;
        //var option = "<option value=''>Please Select</option>";
        //for (i=0;i<=numbers;i++){
        //	option += '<option value="'+ i + '">' + i + '</option>';	
        //}//--end for
        ////add the number list to the dropdown with a class name .numddl
        //$('.numddl').append(option);
        
        /*this list order must not be changed as it is corresponding to loop variable value and database id.
         * This can be read from DB and added to the list of dropdown values to avoid any logical error
         */
        //var list = ["Detached","Semi Detached","Flat","Tenement"];
        //add the number list to the dropdown
        //$('#property_type').append(domutil.getoption(list));

        /*this list order must not be changed as it is corresponding to loop variable value and database id.
         * This can be read from DB and added to the list of dropdown values to avoid any logical errors 
         */
        //var list = ["Before 1970","1971-1990","1991-2000","After 2001"];
        //add the number list to the dropdown
        //$('#contruction_period').append(domutil.getoption(list));

        /*this list order must not be changed as it is corresponding to loop variable value and database id.
         * This can be read from DB and added to the list of dropdown values to avoid any logical errors 
         */
        //var list = ["Owned","Rented"];
        //add the number list to the dropdown
        //$('#ownership_status').append(domutil.getoption(list));

        /*this list order must not be changed as it is corresponding to loop variable value and database id.
         * This can be read from DB and added to the list of dropdown values to avoid any logical errors 
         */
        //var list = ["Flat rate tariff","Water metering tariff","Rising block tariff","Declining block tariff","Seasonal tariff","Time-of-day tariff","Social tariff"];
        //add the number list to the dropdown
        //$('#water_pricing').append(domutil.getoption(list));

        //Added by Chris Pantazis
        //var list = ["<= 50","51 - 100", "101 - 200", "> 200"];
        //add the number list to the dropdown
        //$('#property_area').append(domutil.getoption(list));

        //var list = ["<= 20","21 - 50", "51 - 100", "> 100"];
        //add the number list to the dropdown
        //$('#garden_area').append(domutil.getoption(list));

        //var list = ["<= 20","21 - 50", "51 - 70", "> 70"];
        //add the number list to the dropdown
        //$('#pervious_area').append(domutil.getoption(list));

        //var list = ["<= 50","51 - 100", "101 - 200", "> 200"];
        //add the number list to the dropdown
        //$('#roof_area').append(domutil.getoption(list));
        
	}//--end function

	/* This method is for policy.html page and execute when the complete page loaded.
	 * This method set the applet to encapsulate inside the responsive container
	 */ 
	this.appletsize = function()
	{
		var appwidth = document.getElementById("app").offsetWidth; //get the width of the app container set by responsive bootstrap
	    var applet = document.getElementById('myapplet');	//get applet id
	    applet.setAttribute('width', (appwidth-50) );	//set applet width-50 to make sure it does not spill out of responsive container		
	}//--end function
	
	/* This method initialise the jquery code for the panel 
	 * open/colleapse. This code is taken from bootsnipp.com
	 * 
	 */
	this.initpanel = function()
	{
		$(document).on('click', '.panel-heading span.clickable', function (e) {
		    var $this = $(this);
		    if (!$this.hasClass('panel-collapsed')) {
		        $this.parents('.panel').find('#fold').slideUp();
		        $this.addClass('panel-collapsed');
		        $this.find('i').removeClass('glyphicon-minus').addClass('glyphicon-plus');
		    } else {
		        $this.parents('.panel').find('#fold').slideDown();
		        $this.removeClass('panel-collapsed');
		        $this.find('i').removeClass('glyphicon-plus').addClass('glyphicon-minus');
		    }
		});
		
		$(document).on('click', '.panel div.clickable', function (e) {
		    var $this = $(this);
		    if (!$this.hasClass('panel-collapsed')) {
		        $this.parents('.panel').find('#fold').slideUp();
		        $this.addClass('panel-collapsed');
		        $this.find('i').removeClass('glyphicon-minus').addClass('glyphicon-plus');
		    } else {
		        $this.parents('.panel').find('#fold').slideDown();
		        $this.removeClass('panel-collapsed');
		        $this.find('i').removeClass('glyphicon-plus').addClass('glyphicon-minus');
		    }
		});			
	}//--end function
	
	/* This method populate user profile form
	 * from a value obtained by AJAX request
	 * This is needed to keep the form upded with values
	 */
	this.setuser = function()
	{
		var dataObj = {};
		var url = iwidgetutil.baseURL+iwidgetutil.getuser;
		dataObj.csrfmiddlewaretoken = domutil.getcsrftoken('csrftoken');	
		data = ajaxutil.postAjax(dataObj,url); //send data to server
		//id's (DOM) are related to profile-form
		$("#first_name").val(data[0].fields['first_name']);
		$("#last_name").val(data[0].fields['last_name']);
		$("#email").val(data[0].fields['email']);		
	}//--end function
	
	/* This method populate household profile form
	 * from a value obtained by AJAX request
	 * this is needed to keep the form upded with values
	 * id: logged user id or any other household id
	 */
	this.sethousehold = function(id)
	{
		var url = iwidgetutil.baseURL+iwidgetutil.gethousehold;		
		dataObj.csrfmiddlewaretoken = domutil.getcsrftoken('csrftoken');
		dataObj.id = id;
		data = ajaxutil.postAjax(dataObj,url); //send data to server
		alert(data[0].fields["num_of_occupants"]);
		alert(data[0].fields["property_type"]);
		$("#num_of_occupants").val(data[0].fields['num_of_occupants']);
		$("#property_type").val(data[0].fields['property_type']);
	}//--end function
	
	/*shows effectively the form submission message (fade in and fade out effect) to inside provided div id
	 * id: div content id (DOM)
	 * cssclass: classess to display alert
	 * msg: any error, warning or alert messages
	*/
	this.showmessage = function(id,cssclass,msg)
	{
        $(id).empty();
		$(id).append(msg);
        domutil.setCssclass(id,cssclass);
        $(id).fadeIn(200).delay(6000).fadeOut(200);
        domutil.setdelay(function(){domutil.removeCssclass(id,cssclass)},6500); //delay should be > 6000+200 
	}
	
	/*
	 * This method return the form name/value pair in the json format
	 * id: It is the form id (DOM)
	 * return: json object
	 */
	this.createjson = function(id)
	{
		var dataObj = {};
		var inputs = $(id).serializeArray(); //get name/value pair from form
		for (i=0;i<inputs.length;i++)
		{
			if(inputs[i]['name']=='csrfmiddlewaretoken')
				dataObj[inputs[i]['name']] = inputs[i]['value'];
			else
				dataObj[inputs[i]['name']] = inputs[i]['value'];
		}
		return dataObj;
	}//--end
	/* This method submits form to the server using ajax. It validated form, collect data in dictionary 
	 * and send it to server. Methods also process any error code and data from server
	 * id: It is the form id (DOM)
	 */
	this.sendToserver = function(id)
	{
		if(formutil.getValidation(id))
		{		
			if(id==iwidgetutil.loginform) //if if matched login form id
			{
				var dataObj = {};
				dataObj.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val(); 
				dataObj.username = $('#username').val();
				dataObj.password = $('#password').val();
				
				var status = ajaxutil.postAjax(dataObj,formutil.getAction(id)); //send data to server
				if(status==false)
					this.showmessage(iwidgetutil.loginmsg,dangerclass,"Invalid username or password");
				else if(status==true)
					window.location.replace(iwidgetutil.dashboard); //redirect and no back option for login page
				else if(status==0)
					this.showmessage(iwidgetutil.loginmsg,dangerclass,"Inactive account status");
				else
					this.showmessage(iwidgetutil.loginmsg,dangerclass,iwidgetutil.unexpectederror);				
			}//--end login-form logic
			else if(id==iwidgetutil.passwordform) //if matched password form id
			{
				var dataObj = {};
				dataObj.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
				dataObj.oldpasswd = $('#oldpasswd').val();
				dataObj.newpasswd = $('#newpasswd').val();
				var status = ajaxutil.postAjax(dataObj,formutil.getAction(id)); //send data to server
				if(status==false)
					this.showmessage(iwidgetutil.passwordmsg,dangerclass,"Incorrect password");
				else if(status==true)
					this.showmessage(iwidgetutil.passwordmsg,successclass,"Your password has changed successfully");
				else
					this.showmessage(iwidgetutil.passwordmsg,dangerclass,iwidgetutil.unexpectederror);
				
				formutil.resetForm(id);
			}//--end password-form logic
			else if(id==iwidgetutil.profileform) //if matched profile form id
			{				
				var answer = ajaxutil.postAjax(this.createjson(id),formutil.getAction(id)); //send data to server
					this.showmessage(iwidgetutil.profilemsg,successclass, answer);
					//this.showmessage(iwidgetutil.profilemsg,dangerclass,iwidgetutil.unexpectederror);
			}//--end profile-form logic
			else if(id==iwidgetutil.householdform) //if matched household form id
			{
				var answer = ajaxutil.postAjax(this.createjson(id),formutil.getAction(id)); //send data to server
				this.showmessage(iwidgetutil.householdmsg, successclass, answer);
				//if(status==true) {
				//	this.showmessage(iwidgetutil.householdmsg, successclass, "Your household profile has updated successfully");
				//	this.showmessage(iwidgetutil.householdmsg2, successclass, "Your household profile has updated successfully");
				//}
				//else {
				//	this.showmessage(iwidgetutil.householdmsg, dangerclass, iwidgetutil.unexpectederror);
				//	this.showmessage(iwidgetutil.householdmsg2, dangerclass, iwidgetutil.unexpectederror);
				//}
			}//--end household-form
			else if(id==iwidgetutil.c_uc53form) //if matched forecast form id
			{
				var dataObj = {};
				dataObj.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
				dataObj.algo   = "mlp";//$("#c_uc53algo").val(); //get algorithm
				dataObj.period = $('input[name=c_uc53duration]:checked').val(); //get period
				if (dataObj.period==null)
				{
					alert("Please select months");
					return;
				}	
				var data = ajaxutil.postAjax(dataObj,formutil.getAction(id)); //send ajax request
				
				var error = data["error"];
				if (error){
					this.showmessage(iwidgetutil.c_uc53msg, dangerclass, error);
					return;
				} else {
					// End of strict execution sequence block
					domutil.removeCssclass("#c_uc53cont","hide"); //make chart container visible 
					$("#c_uc53chartcont").empty(); //clear previous chart			    
					var w = domutil.getdivwidth("c_uc53chartcont");
				    var dim = {"width":w,"height":450}; //chart container width
				    //alert(JSON.stringify(data["price_break"]));
				  	chartutil.barplot("#c_uc53chartcont",dim,data["data"],data["price_break"]); //plot the bar chart
				  	
					//add title
					$("#c_uc53ftitle").html('<p class="bg-primary text-center"><strong>'+data["title"]+'</strong></p>');
					
					//adding chart details
					$("#c_uc53fsum").html("Total: £"+data["billdata"]["sum"]);
					$("#c_uc53favg").html("<div class='text-warning'>Average Monthly Bill: £"+data["billdata"]["avg"]+"</div");
					$("#c_uc53fhigh").html("<div class='text-danger'>Highest Monthly Bill: £"+data["billdata"]["high"]["max"]+" in "+data["billdata"]["high"]["date"]+"</div");
					$("#c_uc53flow").html("<div class='text-success'>Lowest Monthly Bill: £"+data["billdata"]["low"]["min"]+" in "+data["billdata"]["low"]["date"]+"</div");			  	
				    //chartutil.barplot("#c_uc53chartcont",dim,chartdata,price_break); //plot the bar char with line plot also on top
				}
			}//--end forecast-form
			else if(id==iwidgetutil.c_uc41form) //if matched forecast form id
			{
				
				var dataObj = {};
				dataObj.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
				dataObj.algo   = "mlp";//$("#c_uc53algo").val(); //get algorithm
				dataObj.period = $('input[name=c_uc41_per]:checked').val(); //get period
				if (dataObj.period==null)
				{
					alert("Please select months");
					return;
				}
				var data = ajaxutil.postAjax(dataObj,formutil.getAction(id)); //send ajax request
				
				var error = data["error"];
				if (error){
					this.showmessage(iwidgetutil.c_uc41msg, dangerclass, error);
					return;
				} else {				
					domutil.removeCssclass("#c_uc41cont","hide"); //make chart container visible 
					$("#c_uc41chartcont").empty(); //clear previous chart			    
					var w = domutil.getdivwidth("c_uc41chartcont");
				    var dim = {"width":w,"height":450}; //chart container width
				    //alert(JSON.stringify(data["price_break"]));
				  	chartutil.barplot("#c_uc41chartcont",dim,data["data"],data["price_break"]); //plot the bar chart
				  	
					//add title
					$("#c_uc41ftitle").html('<p class="bg-primary text-center"><strong>'+data["title"]+'</strong></p>');
					
					//adding chart details
					
					$("#c_uc41fsum").html("Total: £"+data["billdata"]["sum"]);
					$("#c_uc41favg").html("<div class='text-warning'>Average Monthly Bill: £"+data["billdata"]["avg"]+"</div");
					$("#c_uc41fhigh").html("<div class='text-danger'>Highest Monthly Bill: £"+data["billdata"]["high"]["max"]+" in "+data["billdata"]["high"]["date"]+"</div");
					$("#c_uc41flow").html("<div class='text-success'>Lowest Monthly Bill: £"+data["billdata"]["low"]["min"]+" in "+data["billdata"]["low"]["date"]+"</div");
	
					$("#c_uc41sum").html("Total: £"+data["monthdata"]["sum"]);
					$("#c_uc41avg").html("<div class='text-warning'>Average Monthly Bill: £"+data["monthdata"]["avg"]+"</div");
					$("#c_uc41high").html("<div class='text-danger'>Highest Monthly Bill: £"+data["monthdata"]["high"]["max"]+" in "+data["monthdata"]["high"]["date"]+"</div");
					$("#c_uc41low").html("<div class='text-success'>Lowest Monthly Bill: £"+data["monthdata"]["low"]["min"]+" in "+data["monthdata"]["low"]["date"]+"</div");
					
				    //chartutil.barplot("#c_uc53chartcont",dim,chartdata,price_break); //plot the bar char with line plot also on top
				}
			}//--end forecast-form
			
			else if(id==iwidgetutil.c_uc32form)
			{
				var dataObj = {};
				var title   = "";
				dataObj.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
				//dataObj.analysis = $("#c_uc52_analysis").val(); //get analysis type
				dataObj.compare = $('#c_uc32select').val(); //get period
				dataObj.year    = $('#c_uc32year').val();   //get year
				
				dataObj.period  = $('input[name=c_uc32_per]:checked').val(); //get period
				if(dataObj.period=="days") //if period selected
				{
					
					dataObj.stdate = $("#c_uc32styear").val()+"-"+$("#c_uc32stmonth").val()+"-01";
					dataObj.endate = $("#c_uc32endyear").val()+"-"+$("#c_uc32endmonth").val()+"-01"; //at the server side get the last day of the month (Python)
					var s = dateutil.strtodate(dataObj.stdate);
					var e = dateutil.strtodate(dataObj.endate);
				}//--end if
				else if(dataObj.period=="season")
				{
					dataObj.season 	   = $("#c_uc32_seasons").val();
					dataObj.seasonyear = $("#c_uc32_seasonyear").val();
				}//--end if
				
				if (dataObj.compare=="summer")
					title = "Summer ("+dataObj.year+") consumption comparison"; 
				else if (dataObj.compare=="winter")
					title = "Winter ("+dataObj.year+") consumption comparison";				
				else if (dataObj.compare=="night")
				{
					dataObj.period   = $('input[name=c_uc32_per]:checked').val(); //get period
					title = "Last "+dataObj.period+" months night units comparison";
					
				}
				else if (dataObj.compare=="day")
				{
					dataObj.period  = $('input[name=c_uc32_per]:checked').val(); //get period
					title = "Last "+dataObj.period+" months day units comparison";
					
				}
				
				data  = ajaxutil.postAjax(dataObj,formutil.getAction(id)); //send ajax request
				var error = data["error"];
				if (error){
					this.showmessage(iwidgetutil.c_uc32msg, dangerclass, error);
					return;
				}
				var tr_title1 = data["title1"]; //translated title from unexe/views.py:734 (Chris Pantazis)
				var tr_title2 = data["title2"]; //translated title from unexe/views.py:734 (Chris Pantazis)
				var tr_title3 = data["title3"]; //translated title from unexe/views.py:734 (Chris Pantazis)
				var tr_title4 = data["title4"]; //translated title from unexe/views.py:734 (Chris Pantazis)
				domutil.removeCssclass("#c_uc32cont","hide"); //make chart container visible
				$("#c_uc32chartcont").empty(); //clear previous chart
				$("#c_uc32donutchart").empty(); //clear previous chart
				$("#c_uc32title").empty();
				$("#c_uc32title").html('<p class="bg-primary text-center"><strong>'+title+'</strong></p>');
				
				var w = domutil.getdivwidth("c_uc32chartcont"); //get width of chart div as it changed dynamically due to bootstrap responsive layout
				var dim = {"width":w,"height":450}; //width and height of chart container
				
				var household = data["area"]["areadata"]["household"];
				$("#c_uc32household").html("<div class='text-muted'>" + tr_title1 +": "+household+" m<sup>3</sup></div>");
				
				var occupant = data["area"]["areadata"]["occupant"];
				$("#c_uc32occupant").html("<div class='text-muted'>" + tr_title2 + ": "+occupant+" m<sup>3</sup></div>");
				
				//household
				household = data["you"]["yourdata"]["household"];
				$("#c_uc32hhold").html("<div class='text-primary'> " + tr_title3 + ": "+household+" m<sup>3</sup></div>");

				occupant = data["you"]["yourdata"]["occupant"];
				$("#c_uc32occup").html("<div class='text-primary'>" + tr_title4 +": "+occupant+" m<sup>3</sup></div>");
				
				
				//if(dataObj.period=="season")
				//{
					/*
					household = data["you"]["yourdata"]["household"];
					$("#c_uc32hhold").html("<div class='text-primary'>Total Units Consumed for household: "+household+" m<sup>3</sup></div>");
	
					occupant = data["you"]["yourdata"]["occupant"];
					$("#c_uc32occup").html("<div class='text-primary'>Units consumed per occupant: "+occupant+" m<sup>3</sup></div>");
					*/
				//}
				
				/*
				else
				{
					household = data["you"]["billdata"]["sum"];
					$("#c_uc32hhold").html("<div class='text-primary'>Total Units Consumed for household: "+household+" m<sup>3</sup></div>");
	
					occupant = data["you"]["billdata"]["occupant"];
					$("#c_uc32occup").html("<div class='text-primary'>Units consumed per occupant: "+occupant+" m<sup>3</sup></div>");					
				}
				*/
				//draw line chart
				chartutil.c_uc33linechart("#c_uc32chartcont", dim, data);
				//draw donut chart
				var w = domutil.getdivwidth("c_uc32donutchart"); //get width of chart div as it changed dynamically due to bootstrap responsive layout
				var dim = {"width":w,"height":450}; //width and height of chart container
				chartutil.c_uc33comparechart("#c_uc32donutchart", dim, data);
				
				
				/*
				var you = data["you"];
				var yourdata  = you[you.length-1]; //available after day series data at position xx, where xx = number of months				

				var area 	  = data["area"];
				var areadata  = area[area.length-1]; //available after day series data at position xx, where xx = number of months		
				
				//area
				var household = areadata["areadata"]["household"];
				household     = mathutil.floatFixed(mathutil.stringTofloat(household),2);
				$("#c_uc32household").html("<div class='text-muted'>Units consume per household "+household+" (Units)</div>");

				var occupant = areadata["areadata"]["occupant"];
				occupant     = mathutil.floatFixed(mathutil.stringTofloat(occupant),2);
				$("#c_uc32occupant").html("<div class='text-muted'>Units consume per occupants "+occupant+" (Units)</div>");				

				//household
				household = yourdata["yourdata"]["sum"];
				household = mathutil.floatFixed(mathutil.stringTofloat(household),2);
				$("#c_uc32hhold").html("<div class='text-primary'>Units consume per household "+household+" (Units)</div>");

				occupant = yourdata["yourdata"]["avg"];
				occupant = mathutil.floatFixed(mathutil.stringTofloat(occupant),2);
				$("#c_uc32occup").html("<div class='text-primary'>Units consume per occupants "+occupant+" (Units)</div>");	
				
				
				var youchart = ""
				for (i=0;i<you.length-1;i++)
				{
					if(i<you.length-2)
						youchart = youchart + JSON.stringify(you[i])+",";
					else
						youchart = youchart + JSON.stringify(you[i]);
				}
				youchart = "["+youchart+"]";
				youchart = jQuery.parseJSON(youchart);
				
				var areachart = ""
				for (i=0;i<area.length-1;i++)
				{
					if(i<area.length-2)
						areachart = areachart + JSON.stringify(area[i])+",";
					else
						areachart = areachart + JSON.stringify(area[i]);
				}
				areachart = "["+areachart+"]";
				areachart = jQuery.parseJSON(areachart);
				
				//draw line chart
				chartutil.c_uc33linechart("#c_uc32chartcont",dim,youchart,areachart);
				//draw donut chart
				var w = domutil.getdivwidth("c_uc32donutchart"); //get width of chart div as it changed dynamically due to bootstrap responsive layout
				var dim = {"width":w,"height":450}; //width and height of chart container
				chartutil.c_uc33comparechart("#c_uc32donutchart",dim,data["comparechart"]);
				*/						
				/*
				var total = 5; //total item to remove from JSON (4 stats + 1 title) 
				var dataObj = {};
				dataObj.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
				dataObj.compare  = $("#compare").val(); //get algorithm
				dataObj.occupants= domutil.getchkboxvalue("#occupants"); //get occupants
				dataObj.property = domutil.getchkboxvalue("#property");  //get property
				var data = ajaxutil.postAjax(dataObj,formutil.getAction(id)); //send ajax request
				var len = data.length; 				
				
				//parse json and get all extra data and leave only timeseries for chart plotting
				var title = data[len-1].title; //get title
				for(i=len-total;i<len-1;i++) //len-1 because last one is title and we dont want to touch in this loop
				{
					//i have to use javascript here because jquery seems to unable to find DOM id when added using django template
					document.getElementById(data[i].period+" month").innerHTML='';
					var text = "<strong>Over "+ data[i].period +" months period:</strong><br/>Total Household: "+data[i].household+", Total Occupants: "+data[i].occupant+",Average Occupant/Household: "+data[i].average;
					document.getElementById(data[i].period+" month").innerHTML = text;
				}
				
				var chartdata="";
				for (i=0;i<len-total;i++)
				{
					if(i<(len-total-1))
						chartdata = chartdata + JSON.stringify(data[i])+",";
					else
						chartdata = chartdata + JSON.stringify(data[i]);
				}
				chartdata = "["+chartdata+"]";
				chartdata = jQuery.parseJSON(chartdata);
				
				$("#dmachart").empty(); //clear previous chart
				$("#dmatitle").empty(); //clear previous chart
				$("#dmatitle").html('<p class="bg-primary text-center"><strong>'+title+'</strong></p>');
				var w = domutil.getdivwidth("dmachart"); //get width of chart div as it changed dynamically due to bootstrap responsive layout
				dim = {"width":w,"height":450}; //width and height of chart container	
				chartutil.uc32barplot1("#dmachart",dim,chartdata);
				*/				
				//dataObj.period  = $('input[name=duration]:checked').val(); //get period
			}
			else if(id==iwidgetutil.c_uc52form)
			{
				var avgmsg = "Average per month:";
				var dataObj = {};
				dataObj.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
				//dataObj.analysis = $("#c_uc52_analysis").val(); //get analysis type
				//dataObj.period   = $('input[name=c_uc52_per]:checked').val(); //get period
				dataObj.period = domutil.getradiovalue('c_uc52_per');
				if(dataObj.period=="days")
				{
					avgmsg = "Average per day:";
					dataObj.stdate = $("#styear").val()+"-"+$("#stmonth").val()+"-01";
					dataObj.endate = $("#endyear").val()+"-"+$("#endmonth").val()+"-01";
					var s = dateutil.strtodate(dataObj.stdate)
					var e = dateutil.strtodate(dataObj.endate)
				}//--end if	(days)
				else if(dataObj.period=="season")
				{
					dataObj.season 	   = $("#c_uc52_seasons").val();
					dataObj.seasonyear = $("#c_uc52_seasonyear").val();
				}//--end if
					
				var data = ajaxutil.postAjax(dataObj,formutil.getAction(id)); //send ajax request				
				var error = data["error"];
				if (error) {
					this.showmessage(iwidgetutil.c_uc52msg, dangerclass, error);
					return;
				}

				$("#c_uc52chartcont").empty();
				$("#c_uc52compchart").empty(); 
				$("#c_uc52title").empty(); //clear previous chart
				$("#c_uc52title").html('<p class="bg-primary text-center"><strong>'+data["title"]+'</strong></p>');

				//adding chart details (tariff1)
				$("#c_uc52t1sum").html("Total: £"+data["tariff1data"]["sum"]);
				$("#c_uc52t1avg").html("<div class='text-warning'>Average Per Month: £"+data["tariff1data"]["avg"]+"</div");
				$("#c_uc52t1high").html("<div class='text-danger'>Highest: £"+data["tariff1data"]["high"]["max"]+" in "+data["tariff1data"]["high"]["date"]+"</div");
				$("#c_uc52t1low").html("<div class='text-success'>Lowest: £"+data["tariff1data"]["low"]["min"]+" in "+data["tariff1data"]["low"]["date"]+"</div");

				
				//adding chart details (tariff2)
				$("#c_uc52t2sum").html("Total: £"+data["tariff2data"]["sum"]);
				$("#c_uc52t2avg").html("<div class='text-warning'>Average Per Month: £"+data["tariff2data"]["avg"]+"</div");	
				$("#c_uc52t2high").html("<div class='text-danger'>Highest: £"+data["tariff2data"]["high"]["max"]+" in "+data["tariff2data"]["high"]["date"]+"</div");
				$("#c_uc52t2low").html("<div class='text-success'>Lowest: £"+data["tariff2data"]["low"]["min"]+" in "+data["tariff2data"]["low"]["date"]+"</div");
				
				//draw line chart				
				var w = domutil.getdivwidth("c_uc52chartcont"); //get width of chart div as it changed dynamically due to bootstrap responsive layout
				var dim = {"width":w,"height":450}; //width and height of chart container
				chartutil.c_uc52linechart("#c_uc52chartcont",dim,data["tariff1"],data["tariff2"]);
				
				//draw compare bar chart
				w = domutil.getdivwidth("c_uc52compchart"); //get width of chart div as it changed dynamically due to bootstrap responsive layout
				dim = {"width":w,"height":450}; //width and height of chart container
				
				chartutil.c_uc52comparechart("#c_uc52compchart",dim,data["comparechart"]);				
				
			}
			else if(id==iwidgetutil.c_uc33form)
			{
				var dataObj = {};
				var title   = "";
				dataObj.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
				//dataObj.analysis = $("#c_uc52_analysis").val(); //get analysis type
				dataObj.compare = $('#c_uc33select').val(); //get period
				dataObj.year    = $('#c_uc33year').val();   //get year
				
				dataObj.period  = $('input[name=c_uc33_per]:checked').val(); //get period
				if(dataObj.period=="days") //if period selected
				{
					
					dataObj.stdate = $("#c_uc33styear").val()+"-"+$("#c_uc33stmonth").val()+"-01";
					dataObj.endate = $("#c_uc33endyear").val()+"-"+$("#c_uc33endmonth").val()+"-01"; //at the server side get the last day of the month (Python)
					var s = dateutil.strtodate(dataObj.stdate)
					var e = dateutil.strtodate(dataObj.endate)
				}//--end if
				
				else if(dataObj.period=="season")
				{
					dataObj.season 	   = $("#c_uc33_seasons").val();
					dataObj.seasonyear = $("#c_uc33_seasonyear").val();
				}//--end if
				
				if (dataObj.compare=="summer")
					title = "Summer ("+dataObj.year+") consumption comparison"; 
				else if (dataObj.compare=="winter")
					title = "Winter ("+dataObj.year+") consumption comparison";				
				else if (dataObj.compare=="night")
				{
					dataObj.period   = $('input[name=c_uc33_per]:checked').val(); //get period
					title = "Last "+dataObj.period+" months night units comparison";
					
				}
				else if (dataObj.compare=="day")
				{
					dataObj.period   = $('input[name=c_uc33_per]:checked').val(); //get period
					title = "Last "+dataObj.period+" months day units comparison";
					
				}
				
				var data 	  = ajaxutil.postAjax(dataObj,formutil.getAction(id)); //send ajax request
				var error = data["error"];
				if (error) {
					this.showmessage(iwidgetutil.c_uc33msg, dangerclass, error);
					return;
				}

				var tr_title1b = data["title1"]; //translated title from unexe/views.py:734 (Chris Pantazis)
				var tr_title2b = data["title2"]; //translated title from unexe/views.py:734 (Chris Pantazis)
				var tr_title3b = data["title3"]; //translated title from unexe/views.py:734 (Chris Pantazis)
				var tr_title4b = data["title4"]; //translated title from unexe/views.py:734 (Chris Pantazis)
				domutil.removeCssclass("#c_uc33cont","hide"); //make chart container visible
				$("#c_uc33chartcont").empty(); //clear previous chart
				$("#c_uc33donutchart").empty(); //clear previous chart
				$("#c_uc33title").empty();
				$("#c_uc33title").html('<p class="bg-primary text-center"><strong>'+title+'</strong></p>');
				
				var w 		  = domutil.getdivwidth("c_uc33chartcont"); //get width of chart div as it changed dynamically due to bootstrap responsive layout
				var dim 	  = {"width":w,"height":450}; //width and height of chart container
				//var you 	  = data["you"];
				//var yourdata  = you[you.length-1]; //available after day series data at position xx, where xx = number of months				

				//var area 	  = data["area"];
				//var areadata  = area[area.length-1]; //available after day series data at position xx, where xx = number of months		
				
				//area
				
				var household = data["area"]["areadata"]["household"];
				$("#c_uc33household").html("<div class='text-muted'>" + tr_title1b +": "+household+" m<sup>3</sup></div>");
				
				var occupant = data["area"]["areadata"]["occupant"];
				$("#c_uc33occupant").html("<div class='text-muted'>" + tr_title2b +": "+occupant+" m<sup>3</sup></div>");
				
				//household
				household = data["you"]["yourdata"]["household"];
				$("#c_uc33hhold").html("<div class='text-primary'>" + tr_title3b +": "+household+" m<sup>3</sup></div>");

				occupant = data["you"]["yourdata"]["occupant"];
				$("#c_uc33occup").html("<div class='text-primary'>" + tr_title4b +": "+occupant+" m<sup>3</sup></div>");
				/*
				if(dataObj.period=="season")
				{
					household = data["you"]["seasondata"]["household"];
					$("#c_uc33hhold").html("<div class='text-primary'>Total Units Consumed for household: "+household+" m<sup>3</sup></div>");
	
					occupant = data["you"]["seasondata"]["occupant"];
					$("#c_uc33occup").html("<div class='text-primary'>Units consumed per occupant: "+occupant+" m<sup>3</sup></div>");
				}
				else
				{
					household = data["you"]["billdata"]["sum"];
					$("#c_uc33hhold").html("<div class='text-primary'>Total Units Consumed for household: "+household+" m<sup>3</sup></div>");
	
					occupant = data["you"]["billdata"]["occupant"];
					$("#c_uc33occup").html("<div class='text-primary'>Units consumed per occupant: "+occupant+" m<sup>3</sup></div>");					
				}
				*/
				/*
				var youchart = ""
				for (i=0;i<you.length-1;i++)
				{
					if(i<you.length-2)
						youchart = youchart + JSON.stringify(you[i])+",";
					else
						youchart = youchart + JSON.stringify(you[i]);
				}
				youchart = "["+youchart+"]";
				youchart = jQuery.parseJSON(youchart);
				
				var areachart = ""
				for (i=0;i<area.length-1;i++)
				{
					if(i<area.length-2)
						areachart = areachart + JSON.stringify(area[i])+",";
					else
						areachart = areachart + JSON.stringify(area[i]);
				}
				areachart = "["+areachart+"]";
				areachart = jQuery.parseJSON(areachart);
				*/
				//draw line chart
				chartutil.c_uc33linechart("#c_uc33chartcont",dim, data);
				//chartutil.c_uc33linechart("#c_uc33chartcont",dim,youchart,areachart);
				//draw donut chart
				var w = domutil.getdivwidth("c_uc33donutchart"); //get width of chart div as it changed dynamically due to bootstrap responsive layout
				var dim = {"width":w,"height":450}; //width and height of chart container
				chartutil.c_uc33comparechart("#c_uc33donutchart",dim,data);
				//chartutil.c_uc52donutchart("#c_uc33donutchart",dim,data["donutchart"]);				
				
			}
			else if(id==iwidgetutil.c_uc34form)
			{
				var dataObj = {};
				var title   = "";
				dataObj.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
				//dataObj.analysis = $("#c_uc52_analysis").val(); //get analysis type
				dataObj.compare = $('#c_uc34select').val(); //get period
				dataObj.year    = $('#c_uc34year').val();   //get year
				
				dataObj.period  = $('input[name=c_uc34_per]:checked').val(); //get period
				if(dataObj.period=="days") //if period selected
				{
					
					dataObj.stdate = $("#c_uc34styear").val()+"-"+$("#c_uc34stmonth").val()+"-01";
					dataObj.endate = $("#c_uc34endyear").val()+"-"+$("#c_uc34endmonth").val()+"-01"; //at the server side get the last day of the month (Python)
					var s = dateutil.strtodate(dataObj.stdate)
					var e = dateutil.strtodate(dataObj.endate)
				}//--end if
				else if(dataObj.period=="season")
				{
					dataObj.season 	   = $("#c_uc34_seasons").val();
					dataObj.seasonyear = $("#c_uc34_seasonyear").val();
				}//--end if
				
				if (dataObj.compare=="summer")
					title = "Summer ("+dataObj.year+") consumption comparison"; 
				else if (dataObj.compare=="winter")
					title = "Winter ("+dataObj.year+") consumption comparison";				
				else if (dataObj.compare=="night")
				{
					dataObj.period   = $('input[name=c_uc34_per]:checked').val(); //get period
					title = "Last "+dataObj.period+" months night units comparison";
					
				}
				else if (dataObj.compare=="day")
				{
					dataObj.period   = $('input[name=c_uc34_per]:checked').val(); //get period
					title = "Last "+dataObj.period+" months day units comparison";
					
				}
				
				var data 	  = ajaxutil.postAjax(dataObj,formutil.getAction(id)); //send ajax request
				
				var error = data["error"];
				if (error) {
					this.showmessage(iwidgetutil.c_uc34msg, dangerclass, error);
					return;
				}
				
				domutil.removeCssclass("#c_uc34cont","hide"); //make chart container visible
				$("#c_uc34chartcont").empty(); //clear previous chart
				$("#c_uc34donutchart").empty(); //clear previous chart
				$("#c_uc34title").empty();
				$("#c_uc34title").html('<p class="bg-primary text-center"><strong>'+title+'</strong></p>');
				
				var w 		  = domutil.getdivwidth("c_uc34chartcont"); //get width of chart div as it changed dynamically due to bootstrap responsive layout
				var dim 	  = {"width":w,"height":450}; //width and height of chart container
				
				var household = data["area"]["areadata"]["household"];
				$("#c_uc34household").html("<div class='text-muted'>Total Units Consumed for household: "+household+" m<sup>3</sup></div>");
				
				var occupant = data["area"]["areadata"]["occupant"];
				$("#c_uc34occupant").html("<div class='text-muted'>Units consumed per occupant: "+occupant+" m<sup>3</sup></div>");				
				
				//household
				household = data["you"]["yourdata"]["household"];
				$("#c_uc34hhold").html("<div class='text-primary'>Total Units Consumed for household: "+household+" m<sup>3</sup></div>");

				occupant = data["you"]["yourdata"]["occupant"];
				$("#c_uc34occup").html("<div class='text-primary'>Units consumed per occupant: "+occupant+" m<sup>3</sup></div>");				
				
				//draw line chart
				chartutil.c_uc34linechart("#c_uc34chartcont",dim,data["you"]["data"],data["area"]["data"]);
				//chartutil.c_uc33linechart("#c_uc33chartcont",dim,youchart,areachart);
				//draw donut chart
				var w = domutil.getdivwidth("c_uc34donutchart"); //get width of chart div as it changed dynamically due to bootstrap responsive layout
				var dim = {"width":w,"height":450}; //width and height of chart container
				chartutil.c_uc34comparechart("#c_uc34donutchart",dim,data["comparechart"]);				
				//chartutil.c_uc52donutchart("#c_uc33donutchart",dim,data["donutchart"]);				
			}
			else if(id==iwidgetutil.ukcsregform)
			{
				var dataObj = {};
				dataObj.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
				dataObj.ukcsregfname 		= $("#ukcsregfname").val();
				dataObj.ukcsreglname 		= $("#ukcsreglname").val();
				dataObj.ukcsregemail 		= $("#ukcsregemail").val();
				dataObj.ukcsregaddress		= $("#ukcsregaddress").val();
				
				var data = ajaxutil.postAjax(dataObj,formutil.getAction(id));
				if(data==iwidgetutil.NOT_FOUND)
				{
					alert("Incorrect Address: Please provide the correct address.");
					return;
				}
				if(data==iwidgetutil.ALREADY_EXIST)
				{
					alert("This address is already registered.");
					return;
				}				
				
				if(data==true)
					window.location.replace(iwidgetutil.ukcsconfirm);
				
			}
			else{}
		}//--end if
		else 
			return false;
	}//--end class
}
//---------------------------------------------------End class-------------------------------------------------//
apputil = new AppUtil();

//--------------------------------------------------overriding methods----------------------------------------------//
//this method overriding the core methods of the jquery validation plugin , just for showing message in appropraite colour and position on form
jQuery.validator.setDefaults({
    highlight: function(element) {
        $(element).closest('.form-group').addClass('has-error');
    },
    unhighlight: function(element) {
        $(element).closest('.form-group').removeClass('has-error');
    },
    errorElement: 'span',
    errorClass: 'text-danger',
    errorPlacement: function(error, element) {
        if(element.parent('.input-group').length) {
            error.insertAfter(element.parent());
        } else {
            error.insertAfter(element);
        }
    }		
});
//--------------------------------------------------End overriding methods-----------------------------------------//

//added by Chris Pantazis to load the table of events after hiding a user event

function hideEventAndReload(id, username){
    $("#user_events").empty().load("/uc_03_6/events/" + username + "/?f=new&hide=" + id);
}

function loadFaultHistory(username){
    $("#cuc36").empty().load("uc_03_6/events/history/" + username +"/");
}

function addUserPageView(username, page_title, url){
	ajaxutil.postAjax({'user': username, 'page': page_title}, url) ;
}
