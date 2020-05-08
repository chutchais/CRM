from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from .forms import UploadFileForm
from .models import (Container,FileType,ShoreFile,Vessel,Shipper,Booking,Port,Origin,ContainerType)
import django_excel as excel
import xlrd
import re
import datetime
from django.db.models import Count,Sum,Value, When,Case,IntegerField,CharField

def index(request,year=None,month=None):

	import datetime
	if not month:
		today= datetime.date.today()
		year = today.strftime('%Y')#-%m-%d %H:%M
		month = today.strftime('%m')
		# print(year,month,today)

	sf = ShoreFile.objects.filter(year=year,month=month)
	c = Container.objects.filter(shorefile__in = sf)
	# print(sf.count())
	#-------By Daily------
	file_by_filetype = sf.values('day').annotate(
		number=Count('name')
		)

	container_by_filetype = c.values('shorefile__day').annotate(
		number=Count('number')
		)
	ziped = zip(file_by_filetype,container_by_filetype)
	# ----------------------

	# By Liner and Service
	# liner = c.values('booking__line').annotate(
	# 	number=Count('number')
	# 	)

	context={
		'title':'Monthly report of '  ,
		'date': sf[0].created_date,
		'lists': ziped,
		'files':file_by_filetype,
		'total_file':sf.count(),
		'containers': container_by_filetype,
		'total_container': c.count(),
		'year':year,
		'month':month
		}
	return render(
		request,
		'daily.html',context)

def daily(request,year,month,day):
	# print(day,month,year)
	if day == '99' :
		# print ('Month Summary')
		title = 'Month summary of '
		sf = ShoreFile.objects.filter(year=year,month=month)
	else :
		# print ('Month List')
		title = 'Summary of '
		sf = ShoreFile.objects.filter(year=year,month=month,day=day)
	
	# print (sf.count())
	c = Container.objects.filter(shorefile__in = sf)
	
	file_by_filetype = sf.values('filetype').annotate(
		number=Count('name')
		)

	container_by_filetype = c.values('shorefile__filetype','booking__line').annotate(
		number=Count('number')
		)
	context={
		'title':title  ,
		'date': sf[0].created_date,
		'files':file_by_filetype,
		'total_file':sf.count(),
		'containers': container_by_filetype,
		'total_container': c.count(),
		'year':year,
		'month':month,
		'day':day
		}
	return render(
		request,
		'index.html',context)

# Create your views here.
def upload(request):
	if request.method == "POST":
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			filehandle = request.FILES['file']
			book = xlrd.open_workbook(file_contents=filehandle.read())
			# return excel.make_response(filehandle.get_sheet(), "csv",
			#                            file_name="download")
	else:
		form = UploadFileForm()
	return render(
		request,
		'upload_form.html',
		{
			'form': form,
			'title': 'Excel file upload and download example',
			'header': ('Please choose any excel file ' +
					   'from your cloned repository:')
		})

def confirm_data(request):
	import math
	slug = request.POST.get('slug', '')
	rows = request.POST.get('rows', '')
	sf = ShoreFile.objects.get(slug=slug)
	print ('Confirm - Data')
	if slug:
		import ast
		datas = ast.literal_eval(rows)
		for i, d in enumerate(datas):
			if d['new'] =='Yes':
				vessel ,created = Vessel.objects.get_or_create(name=d['vessel'])
				if 'shipper' in d.keys():
					shipper,created = Shipper.objects.get_or_create(name=d['shipper'])
				else:
					shipper = None

				# booking,created = Booking.objects.get_or_create(number=d['booking'],voy=d['voy'],pod=d['pod'],
				# 	shipper=shipper,vessel=vessel,line=d['line'],agent=d['agent'])

				booking,created = Booking.objects.get_or_create(number=d['booking'],voy=d['voy'],pod=d['pod'],
					shipper=shipper,vessel=vessel,line=d['line'],agent=d['agent'],
					terminal = d['terminal'])

				if created:
					if d['origin'] != '' :
						booking.origin =  Origin.objects.get(name=d['origin'])
						booking.save()
					print('Created new Booking')

				line = d['line']
				dg_class = d['dg_class'] if d['dg_class'] != None else d['dg_class']
				unno = d['unno'] if d['unno'] != None else d['unno']
				
				# To Insert VGM data
				vgm_kwarg = {}
				if 'vgm' in d :
					if d['vgm']=='':
						newVgm=0
					else:
						newVgm = math.ceil(float(d['vgm']))
					vgm_kwarg ={'vgm':newVgm}
					# print ('VGM data %s' % vgm_kwarg)
				else:
					print('No VGM data')
				# End VGM


				container = Container.objects.create(number= d['container'],booking=booking,
									container_type = d['type'],
									container_size = d['size'],
									container_high = d['high'],
									dg_class = dg_class,
									unno = unno,
									# vgm = newVgm,
									payment = d['term'],
									draft=True,
									shorefile= sf,**vgm_kwarg)
				if d['type'] =='RE':
					if d['temp'] != None and d['temp']!='':
						container.temperature = float(d['temp'])
						container.save()

				print('%s -- %s' % (booking,container))

		sf.status='A'
		sf.save()
		print('Confirm Done')
	# return HttpResponseRedirect(reverse('upload'))
		form = UploadFileForm()
	return render(
		request,
		'upload_form.html',
		{
		'form': form,
		'title': 'Import excel data into database',
		'header': 'Please upload Shore xls file:',
		'slug': slug,
		'completed' : True
		})


def delete_data(request):
	slug = request.POST.get('slug', '')
	if slug:
		sf = ShoreFile.objects.get(slug=slug)
		sf.delete()
		print('Delete Done')
	return HttpResponseRedirect(reverse('upload'))

def import_data(request):

	terminalIn 	=	''
	originIn 	= 	''

	if request.method == "POST":
		form = UploadFileForm(request.POST,
		request.FILES)

		terminalIn =''

		if form.is_valid():
			filehandle =request.FILES['file']
			book = xlrd.open_workbook(file_contents=filehandle.read())
			# sheet_names = book.sheet_names()
			# print (sheet_names)
			xl_sheet = book.sheet_by_index(0)
			# print ('Sheet name: %s' % xl_sheet.name)
			# print ('Total row %s' % xl_sheet.nrows )
			# print ('Total col %s' % xl_sheet.ncols)

			#Find First row in sheet
			# get Shore File Type
			fileTypeIn 	= form.cleaned_data['filetype']
			terminalIn 	= form.cleaned_data['terminal']
			originIn 	= form.cleaned_data['origin']
			print (originIn)


			obj = FileType.objects.get(name=fileTypeIn)
			fobj = ShoreFile.objects.filter(name=filehandle)
			if fobj.count() == 0:
				fileInName=filehandle
			else:
				fileInName= str(filehandle) + datetime.datetime.now().strftime("%Y%m%d%H%M")
				
			

			if obj:
				# print ('-----Using File Type Configuration---')
				headerContainerToCheck = [obj.container_col]
				headerBookingToCheck = [obj.booking_col]
				headerVoyToCheck =[obj.voy_col]
				headerPodToCheck = [obj.pod_col]
				headerShipperToCheck = [obj.shipper_col]
				headerVesselToCheck = [obj.vessel_col]
				headerTypeToCheck = [obj.container_type_col]
				headerSizeToCheck = [obj.container_size_col]
				headerHighToCheck = [obj.container_high_col]
				headerTermToCheck = [obj.payment_col]
				headerUnnoToCheck = [obj.unno_col]
				headerDGclassToCheck = [obj.dgclass_col]
				headerTempToCheck = [obj.temp_col]
				headerLineToCheck = [obj.line_col]
				headerAgentToCheck = [obj.agent_col]
				headerVGMToCheck = [obj.vgm_col]
				headerTspToCheck = [obj.tsp_col]
			else:
				# print ('-----ot found File Type ---')
				headerContainerToCheck = ['CNTR NO.','Conts. No.','CTNR NO','cont', 'Container','container', 'CNTR','Cont no.','Container Nos']
				headerBookingToCheck = ['Booking No.','BOOKING NO','Booking No.','Bkg','Booking','BKG','BOOKING','BKG NO','Bkg','BK Number']
				headerVoyToCheck =['Voyage','VOY','Voy.','Voy. ','Voy','voy','Feeder Voyage']
				headerPodToCheck = ['TSP 1','pod','POD','DISH PORT','Final']
				headerShipperToCheck = ['Shipper/Consignee','SHIPPER NAME','Shipper Name.','Shipper Name','Shipper','SHIPPER','Shipper']
				headerVesselToCheck = ['Vessel Info.','VESSEL NAME','vessel','Vessel Name','Vessel','Feeder Vessel']
				headerTypeToCheck = ['SzTp','TYP','Type.','Conts.Type','Size','D2','SZ','Size Type']
				headerSizeToCheck = ['SzTp','Size.','Conts.Size','Size','SZ','Size Type']
				headerHighToCheck = ['SzTp','HGT','High','Conts.HGT','Size','SZ','Size Type']
				headerTermToCheck = ['TERM','term','Term','Payment','payment','PAYMENT']
				headerUnnoToCheck = ['UNN','UNNO','UN NUMBER','UN NO.','UNDG No.','Unno']
				headerDGclassToCheck = ['IMDG','DG','DG Class']
				headerTempToCheck = ['Temp','TEMP','Temp.','Set Temp']
				headerLineToCheck = ['OPR','LINE(NYK&TSK)','Line','LINE']
				headerTspToCheck = ['TSP 1']

			found_Container = False
			found_Booking = False

			for row_index in range(0, xl_sheet.nrows):
				for col_index in range(xl_sheet.ncols):
					vCell = xl_sheet.cell(row_index, col_index).value.__str__().strip()

					if any(header in vCell  for header in headerContainerToCheck):
						head_index = row_index
						Container_index = col_index
						Container_col_name = vCell
						found_Container = True
						# print('Header on row %s' % row_index)
						# print ('Container data on col %s' % Container_index )
					
					if any(header in vCell for header in headerBookingToCheck):
						head_index = row_index
						Booking_index = col_index
						Booking_col_name = vCell
						found_Booking = True
						# print ('Booking data on col %s' % Booking_index )
											#VOY

					
						
					if found_Container and found_Booking :
						break

				if found_Container and found_Booking :
						break
			ContSize_index = None
			ContHigh_index = None
			ContTerm_index = None
			ContUnno_index = None
			ContDGclass_index = None
			ContTemp_index = None
			ContLine_index =None
			Shipper_index = None
			ContAgent_index =None
			ContVgm_index = None
			ContTsp_index = None

			for col_index in range(xl_sheet.ncols):
				vCell = xl_sheet.cell(head_index, col_index).value.__str__().strip()
				if any( header == vCell for header in headerVoyToCheck):
						Voy_index = col_index
				if any( header == vCell for header in headerPodToCheck):
						Pod_index = col_index
						# print ('POD on %s' % col_index)
				if any( header == vCell for header in headerShipperToCheck):
						Shipper_index = col_index
				if any( header == vCell for header in headerVesselToCheck):
						Vessel_index = col_index
				if any( header == vCell for header in headerTypeToCheck):
						ContType_index = col_index
				if any( header == vCell for header in headerSizeToCheck):
						ContSize_index = col_index
				if any( header == vCell for header in headerHighToCheck):
						ContHigh_index = col_index
				if any( header == vCell for header in headerTermToCheck):
						ContTerm_index = col_index
				if any( header == vCell for header in headerUnnoToCheck):
						ContUnno_index = col_index
				if any( header == vCell for header in headerDGclassToCheck):
						ContDGclass_index = col_index
				if any( header == vCell for header in headerTempToCheck):
						ContTemp_index = col_index
				if any( header == vCell for header in headerLineToCheck):
						ContLine_index = col_index
				if any( header == vCell for header in headerAgentToCheck):
						ContAgent_index = col_index
				if any( header == vCell for header in headerVGMToCheck):
						ContVgm_index = col_index

				if headerTspToCheck != '':
					if any( header == vCell for header in headerTspToCheck):
						ContTsp_index = col_index
						# print ('TSP on %s' % col_index)


			#Make Key(header)
			keys = [xl_sheet.cell(head_index, col_index).value for col_index in range(xl_sheet.ncols)]
			#Replace Col to standard name
			keys[Booking_index] = 'booking'
			keys[Container_index] = 'container'
			keys[Voy_index] = 'voy'
			keys[Pod_index] = 'pod'
			# keys[Shipper_index] = 'shipper'
			keys[Vessel_index] = 'vessel'
			keys[ContType_index] = 'type'

			if Shipper_index != None :
					keys[Shipper_index] = 'shipper'

			if ContType_index != ContSize_index:
				if ContSize_index != None :
					keys[ContSize_index] = 'size'
			if ContType_index != ContHigh_index:
				if ContHigh_index != None:
					keys[ContHigh_index] = 'high'

			if ContTerm_index != None:
				keys[ContTerm_index] = 'term'
			if ContUnno_index != None:
				keys[ContUnno_index] = 'unno'
				# print ('found index of unno')
			if ContDGclass_index != None:
				keys[ContDGclass_index] = 'dg_class'
			if ContTemp_index != None:
				keys[ContTemp_index] = 'temp'

			if ContLine_index != None:
				keys[ContLine_index] = 'line'

			if headerLineToCheck != headerAgentToCheck:
				if ContAgent_index != None:
					keys[ContAgent_index] = 'agent'

			if ContVgm_index != None:
				keys[ContVgm_index] = 'vgm'
			
			# Add on Sep 11,2018
			#To support Transhipment port

			if ContTsp_index != None :
				keys[ContTsp_index] = 'tsp'


			dict_list = []
			regex='^[A-Z]{4}[0-9]{7}$'
			item_count =0
			new_count = 0

			change_list =[]

			import ast
			for row_index in range(head_index+1, xl_sheet.nrows):
				vContainerData = xl_sheet.cell(row_index, Container_index).value.__str__().strip()
				vBooingData = xl_sheet.cell(row_index, Booking_index).value.__str__().strip()
				vVoyData = xl_sheet.cell(row_index, Voy_index).value.__str__().strip()
				vPodData = xl_sheet.cell(row_index, Pod_index).value.__str__().strip()
				vVesselData = xl_sheet.cell(row_index, Vessel_index).value.__str__().strip()
				# print (vVesselData)
				if ContTsp_index != None:
					vTspData = xl_sheet.cell(row_index, ContTsp_index).value.__str__().strip()
				else :
					vTspData = 'None'
					

				if (vContainerData !='' and re.match(regex,vContainerData)) :
					d = {keys[col_index]: xl_sheet.cell(row_index, col_index).value.__str__().strip()
						 for col_index in range(xl_sheet.ncols)}
					import copy
					c = copy.copy(d)
					
					if len(vTspData) > 0 and vTspData != 'None'   :
						# print ('Using new POD from %s to %s' % (vPodData,vTspData))
						vPodData = 	vTspData
						d['pod'] = vTspData

					# if int(d['booking'])>0:
					# print ('Booking %s' % d['booking'].replace('.0',''))
					# By CHutchai on Sep 28,2018
					# To remove '.0' out from booking in case booking is numeric
					d['booking'] = d['booking'].replace('.0','')
					


					# d['pod'] = vPodData


					# Added by Chutchai on March 7,2018
					# To check Is Booking or POD is changed?
					# print('Voy : %s' % vVoyData )
					#Mapping Cus8omer POD to Our POD (EMC)
					if vPodData == 'HKHKG':
						vPodData='HKHKG'
					if vPodData == 'CNXHK':
						vPodData='CNSHK'
					if vPodData == 'JPTYO':
						vPodData='JPTYO'
					if vPodData == 'JPYKH':
						vPodData='JPYOK'
					if vPodData == 'JPNGY':
						vPodData='JPNGO'
					if vPodData == 'CNSHG':
						vPodData='CNSHA'
					if vPodData == 'CNNBO':
						vPodData='CNNPO'
					#-------------------------------------
					#Swap POD (for all)
					if len(vPodData) == 5:
						vPodData = vPodData[2:] + vPodData[:2]
						newPod = pod_convert(vPodData)
						d['pod'] = newPod if vPodData != newPod else vPodData
						# print ('Current POD %s' % d['pod'])


					from datetime import date, timedelta
					d7=date.today()-timedelta(days=14)
					objContVoy = Container.objects.filter(number=vContainerData,created_date__gte=d7)

					if objContVoy :
						objCurrVoy = objContVoy.last()
						if (objCurrVoy.booking.number != vBooingData or 
							objCurrVoy.booking.pod != vPodData or 
							objCurrVoy.booking.vessel.name != vVesselData or 
							objCurrVoy.booking.voy != vVoyData) :

							d['new'] ='Yes'
							c['new'] ='Yes'
							new_count+=1
							if objCurrVoy.booking.pod != vPodData:
								c['pod'] ='%s  (old: %s)' % (vPodData,objCurrVoy.booking.pod)
							if objCurrVoy.booking.number != vBooingData :
								c['booking'] = '%s  (old: %s)' % (vBooingData,objCurrVoy.booking.number)
							if objCurrVoy.booking.vessel.name != vVesselData :
								c['vessel'] = '%s  (old: %s)' % (vVesselData,objCurrVoy.booking.vessel.name)
							if objCurrVoy.booking.voy != vVoyData :
								# print(vVoyData)
								c['voy'] = '%s  (old: %s)' % (vVoyData,objCurrVoy.booking.voy)


							change_list.append(c)
							# print ('Exist change Container %s (%s,%s)-(%s,%s)' % 
							# 	(vContainerData,objCurrVoy.booking.number,objCurrVoy.booking.pod,vBooingData,vPodData))
						else:
							d['new'] ='No'
							c['new'] ='No'

						c['terminal'] = terminalIn
						d['terminal'] = terminalIn

						c['origin'] = originIn.name if originIn != None else ''
						d['origin'] = originIn.name if originIn != None else ''
						# 	print ('Exist Container %s (%s,%s)' % (vContainerData,objCurrVoy.booking.number,objCurrVoy.booking.voy))
					else:
						# print ('New Container %s' % vContainerData)
						c['new'] ='Yes'
						d['new'] ='Yes'

						c['terminal'] = terminalIn
						d['terminal'] = terminalIn
						c['origin'] = originIn.name if originIn != None else ''
						d['origin'] = originIn.name if originIn != None else ''


						new_count+=1

					# Check Container and Booking Exist.
					# objContBook = Container.objects.filter(number=vContainerData,booking__number=vBooingData)
					# if objContBook:
					# 	d['new'] ='No'
					# else:
					# 	d['new'] ='Yes'
					# 	new_count+=1
					item_count= item_count+1
					dict_list.append(d)



			# dict_list.append({'container_index':Container_index })
			# dict_list.append({'booking_index':Booking_index })
			# print (dict_list)
			filename = filehandle
			# dict_list.update({'line': 'MSC'})
			# print (dict_list)
			if obj:
				for i, d in enumerate(dict_list): 
					# if obj.line_col != None or obj.line_col !='':
					# 	d['line'] = obj.line_default
					if obj.line_col == None or obj.line_col =='':
						d['line'] = obj.line_default if obj.line_default != None else ''

					if headerLineToCheck == headerAgentToCheck:
						d['agent'] = d['line']

					if obj.agent_col == None or obj.agent_col =='':
						# print (obj.agent_default)
						d['agent'] = obj.agent_default if obj.agent_default != None else ''

					if obj.payment_col == None or obj.payment_col =='':
						# print (obj.payment_default)
						d['term'] = obj.payment_default if obj.payment_default != None else ''


					
					# if obj.tsp_col != None or obj.tsp_col =='':
					# 	# print ('Using new POD from %s to %s' % (d['term'], d['tsp']))
					# 	if d['tsp'] != 'None':
					# 		d['pod'] = d['tsp']
						


			#Adjust data follow TypeIn
					# d['high'] ='8.6' #Comment on Nov 17,2017
# Comment on Sep 12,2018
# Process POD on previous process
					# #Mapping Cus8omer POD to Our POD (EMC)
					# if d['pod'].strip() == 'HKHKG':
					# 	d['pod']='HKHKG'
					# if d['pod'].strip() == 'CNXHK':
					# 	d['pod']='CNSHK'
					# if d['pod'].strip() == 'JPTYO':
					# 	d['pod']='JPTYO'
					# if d['pod'].strip() == 'JPYKH':
					# 	d['pod']='JPYOK'
					# if d['pod'].strip() == 'JPNGY':
					# 	d['pod']='JPNGO'
					# if d['pod'].strip() == 'CNSHG':
					# 	d['pod']='CNSHA'
					# if d['pod'].strip() == 'CNNBO':
					# 	d['pod']='CNNPO'
					# #-------------------------------------
					# #Swap POD (for all)
					# if len(d['pod']) == 5:
					# 	d['pod'] = d['pod'][2:] + d['pod'][:2]
					

					
					

					#Change CASH to Y (for all)
					if 'term' in d.keys():
						if d['term']=='CASH':
							d['term'] ='Y'
						else:
							d['term'] = 'N'
					else:
						d['term'] ='Y'

					# print (fileTypeIn,fileTypeIn.__str__())
					# if fileTypeIn.__str__() == 'MSC Shore File' or fileTypeIn.__str__() == 'MSC Shore file (A0)':
					# print(fileTypeIn.__str__().strip())
					if fileTypeIn.__str__() == 'MSC Shore File' or fileTypeIn.__str__() == 'MSC Shore file (A0)':
						# print ('MSC ')
						container_long = d['type'][:2]
						container_type = d['type'][2:]
						d['size'] = container_long
						# print('Size = %s' % container_long)
						# print (d['type'],len(d['type']),container_long)
						d['long'] =  d['type'][:2]

						if container_type=='DV':
							d['type'] = 'DV'
							# d['high'] = '8.6'
							# print(d['high'])
							if 'high' in d.keys():
								# print ('MSC shore - High data %s' % d['high'])
								pass
								
							else:
								# print ('MSC shore - No High data - set to 8.6')
								d['high'] = '8.6'
								

						if container_type=='RE':
							d['type'] = 'RE'
							d['high'] = '8.6'

						if container_type=='OT':
							d['type'] = 'OT'
							d['high'] = '8.6'


						if container_type=='HC':
							d['type'] = 'DV'
							d['high'] = '9.6'

						if container_type=='HR':
							d['type'] ='RE'
							if container_long =='40' :
								d['high'] = '9.6'

						# print(d['term'],len(d['term']))
						if d['term']=='CASH' or d['term']=='Y':
							d['term'] ='Y'
						else:
							d['term'] = 'N'

						# --End MSC--


					
					

					# Modify data
					# d['high'] ='8.6' #Add on Nov 17,2017
					d['type'] = d['type'].replace('.0','')

					if d['type']=='GP':
						d['type'] = 'DV'
						d['high'] = '8.6'

					if d['type']=='HC':
						d['high'] = '9.6'
						d['type'] = 'DV'

					if d['type']=='RE':
						d['high'] = '9.6'
						d['type'] = 'RE'

					if d['type']=='RF':
						d['high'] = '8.6'
						d['type'] = 'RE'

					if d['type']=='HQ':
						d['type'] = 'DV'

					if d['type']=='RH':
						d['type'] = 'RE'

					if d['type']=='4510':
						d['high'] = '9.6'
						d['type'] = 'DV'
						d['size'] = '40'

					if d['type']=='4530':
						d['high'] = '9.6'
						d['type'] = 'RE'
						d['size'] = '40'

					if d['type']=='2210':
						d['high'] = '8.6'
						d['type'] = 'DV'
						d['size'] = '20'

					if d['type']=='4310':
						d['high'] = '8.6'
						d['type'] = 'DV'
						d['size'] = '40'
					
					if d['type']=='40DV':
						d['high'] = '8.6'
						d['type'] = 'DV'
						d['size'] = '40'

					if d['type']=='40ST':
						d['high'] = '8.6'
						d['type'] = 'DV'
						d['size'] = '40'

					if d['type']=='20ST':
						d['high'] = '8.6'
						d['type'] = 'DV'
						d['size'] = '20'

					if d['type']=='40HC':
						# d['high'] = '8.6'
						d['high'] = '9.6'
						d['type'] = 'DV'
						d['size'] = '40'

					if d['type']=='40GP':
						# d['high'] = '8.6'
						d['high'] = '8.6'
						d['type'] = 'DV'
						d['size'] = '40'

					if d['type']=='20RF':
						d['high'] = '8.6'
						d['type'] = 'RE'
						d['size'] = '20'

					if d['type']=='40RF':
						d['high'] = '9.6'
						d['type'] = 'RE'
						d['size'] = '40'

					if d['type'].upper() == '20GP':
						d['high'] = '8.6'
						d['type'] = 'DV'
						d['size'] = '20'

					# Added on Oct 21,2019 -- To support convert Type
					ct = ContainerType.objects.filter(name=d['type']).first()
					if ct :
						print ('Found Container type : %s' % d['type'])
						d['type'] = ct.ctype
						d['high'] = ct.cHigh
						d['size'] = ct.csize


					# Add by Chutchai on Nov 22,2017
					#if high is not in key , add high
					if not 'high' in d:
						# print ('Not found high -- add new to 8.6')
						d['high'] = '8.6'
					#----------------------------------

					# print(d['type'],len(d['type']))
					# print (d['size'])
					d['size'] = d['size'].replace('.0','') if '.0' in d['size'] else d['size']
					d['size'] = d['size'].replace('\'','') 

					# print (d['high'])
					d['high'] = d['high'].replace('.0','') if '.0' in d['high'] else d['high']
					d['high'] = '8.6' if d['high'] == '86' else d['high']
					d['high'] = '9.6' if d['high'] == '96' else d['high']

					d['high'] = '9.6' if d['high'] == '906' else d['high']



					if 'dg_class' in d.keys():
						d['dg_class'] = d['dg_class'].replace('.0','') if '.0' in d['dg_class'] else d['dg_class']
					else:
						d['dg_class'] =''

					if 'unno' in d.keys():
						d['unno'] = d['unno'].replace('.0','') if '.0' in d['unno'] else d['unno']
					else:
						d['unno'] =''

					d['voy'] = d['voy'].replace('.0','') if '.0' in d['voy'] else d['voy']
					if d['temp']:
						d['temp'] = d['temp'].replace('C','')
						d['temp'] = d['temp'].replace('\'','')		

					# d['vgm'] ='TEXT'			

			# Save to Shore File
			# instance = ShoreFile(name=fileInName,filetype=obj,filename=request.FILES['file'],status='D')
			instance = ShoreFile(name=fileInName,filetype=obj,
								filename=request.FILES['file'],status='D',
								terminal = terminalIn)
			instance.save()
			vSlug = instance.slug
			# print (dict_list)

		else:
			return None
	else:
		form = UploadFileForm()
		dict_list = None
		change_list = None
		filename = None
		item_count = None
		new_count =None
		vSlug = None
	return render(
		request,
		'upload_form.html',
		{
		'form': form,
		'title': 'Import excel data into database',
		'header': 'Please upload Shore xls file:',
		'rows' : dict_list,
		'filename' : filename,
		'total' : item_count,
		'new' : new_count,
		'slug': vSlug,
		'changes' :change_list,
		'terminal' : terminalIn
		})



def pod_convert(pod):
	try:
		p = Port.objects.get(name=pod,status='A')
		new_pod = p.new_port
	except ObjectDoesNotExist:
		new_pod = pod
	return new_pod


def export_booking_csv(request):
	import csv
	slug = request.POST.get('slug', '')

	print ('Export Slug %s' % slug)
	if slug:
		sf = ShoreFile.objects.get(slug=slug)
		print(sf.containers)
	else :
		return None

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="%s.csv"' % sf.name

	writer = csv.writer(response)
	writer.writerow(['terminal','shipper_code','shipper_name','line','size','hight','type','iso','unit',
						'vessel_code','vessel_name','voy_out','booking','spod','pod',
						'temperature','imo','un','payment','vgm','origin','status','gross_weight','seal',
						'stow','ow_hight','ow_left','ow_right','destination','category','frghtkind','remark'])

	# users = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
	# for user in users:
	#     writer.writerow(user)
	cons = sf.containers.all().values_list('booking__terminal','booking__shipper__name','booking__shipper__name',
							'booking__line','container_size','container_high','container_type','iso',
							'number','booking__vessel__code','booking__vessel__name','booking__voy','booking__number',
							'booking__pod','booking__pod','temperature','dg_class','unno','payment','vgm',
							'booking__origin__name')
	for c in cons :
		c = list(c)
		c.append('F') #Status
		# c.append('') #ISO
		c.append('') #Gross Weight
		c.append('') #Seal
		c.append('') #stow
		c.append('') #ow_hight
		c.append('') #ow_left
		c.append('') #ow_right
		# c.append('') #Origin
		c.append('') #destination
		c.append('Export') #category
		c.append('FCL') #frhtkind
		c.append('') #remark
		# SPOD
		# c[13]= '%s%s' % (c[13][-2:],c[13][0:3])
		# POD
		c[14]= '%s%s' % (c[14][-2:],c[14][0:3])
		c[13]=c[14]
		# Vgm (19),Gross(22)
		c[22] = c[19]
		c = tuple(c)
		print(c)
		# Modify POD

		writer.writerow(c)

	return response