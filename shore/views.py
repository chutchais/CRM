from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
# Create your views here.
from .forms import UploadFileForm
from .models import (Container,FileType,ShoreFile,Vessel,Shipper,Booking)
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
		print(year,month,today)

	sf = ShoreFile.objects.filter(year=year,month=month)
	c = Container.objects.filter(shorefile__in = sf)
	print(sf.count())
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
	sf = ShoreFile.objects.filter(year=year,month=month,day=day)
	c = Container.objects.filter(shorefile__in = sf)
	
	file_by_filetype = sf.values('filetype').annotate(
		number=Count('name')
		)

	container_by_filetype = c.values('shorefile__filetype','booking__line').annotate(
		number=Count('number')
		)
	context={
		'title':'Summary Shore Pass file of '  ,
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
				booking,created = Booking.objects.get_or_create(number=d['booking'],voy=d['voy'],pod=d['pod'],
					shipper=shipper,vessel=vessel,line=d['line'],agent=d['agent'])
				if created:
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
					print ('VGM data %s' % vgm_kwarg)
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
	return HttpResponseRedirect(reverse('upload'))

def delete_data(request):
	slug = request.POST.get('slug', '')
	if slug:
		sf = ShoreFile.objects.get(slug=slug)
		sf.delete()
		print('Delete Done')
	return HttpResponseRedirect(reverse('upload'))

def import_data(request):
	if request.method == "POST":
		form = UploadFileForm(request.POST,
		request.FILES)
		if form.is_valid():
			filehandle =request.FILES['file']
			book = xlrd.open_workbook(file_contents=filehandle.read())
			# sheet_names = book.sheet_names()
			# print (sheet_names)
			xl_sheet = book.sheet_by_index(0)
			print ('Sheet name: %s' % xl_sheet.name)
			print ('Total row %s' % xl_sheet.nrows )
			print ('Total col %s' % xl_sheet.ncols)

			#Find First row in sheet
			# get Shore File Type
			fileTypeIn = form.cleaned_data['filetype']
			obj = FileType.objects.get(name=fileTypeIn)
			fobj = ShoreFile.objects.filter(name=filehandle)
			if fobj.count() == 0:
				fileInName=filehandle
			else:
				fileInName= str(filehandle) + datetime.datetime.now().strftime("%Y%m%d%H%M")
				
			

			if obj:
				print ('-----Using File Type Configuration---')
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
			else:
				print ('-----ot found File Type ---')
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
						print('Header on row %s' % row_index)
						print ('Container data on col %s' % Container_index )
					
					if any(header in vCell for header in headerBookingToCheck):
						head_index = row_index
						Booking_index = col_index
						Booking_col_name = vCell
						found_Booking = True
						print ('Booking data on col %s' % Booking_index )
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

			for col_index in range(xl_sheet.ncols):
				vCell = xl_sheet.cell(head_index, col_index).value.__str__().strip()
				if any( header == vCell for header in headerVoyToCheck):
						Voy_index = col_index
				if any( header == vCell for header in headerPodToCheck):
						Pod_index = col_index
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


			dict_list = []
			regex='^[A-Z]{4}[0-9]{7}$'
			item_count =0
			new_count = 0
			import ast
			for row_index in range(head_index+1, xl_sheet.nrows):
				vContainerData = xl_sheet.cell(row_index, Container_index).value.__str__().strip()
				vBooingData = xl_sheet.cell(row_index, Booking_index).value.__str__().strip()
				if (vContainerData !='' and re.match(regex,vContainerData)) :
				    d = {keys[col_index]: xl_sheet.cell(row_index, col_index).value.__str__().strip()
				         for col_index in range(xl_sheet.ncols)}
				    # Check Container and Booking Exist.
				    objContBook = Container.objects.filter(number=vContainerData,booking__number=vBooingData)
				    
				    # if headerLineToCheck == headerAgentToCheck:
				    # 	d['agent'] = d['line']

				    if objContBook:
				    	d['new'] ='No'
				    else:
				    	d['new'] ='Yes'
				    	new_count+=1
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




			#Adjust data follow TypeIn
					# d['high'] ='8.6' #Comment on Nov 17,2017

					#Mapping Cus8omer POD to Our POD (EMC)
					if d['pod'].strip() == 'HKHKG':
						d['pod']='HKHKG'
					if d['pod'].strip() == 'CNXHK':
						d['pod']='CNSHK'
					if d['pod'].strip() == 'JPTYO':
						d['pod']='JPTYO'
					if d['pod'].strip() == 'JPYKH':
						d['pod']='JPYOK'
					if d['pod'].strip() == 'JPNGY':
						d['pod']='JPNGO'
					if d['pod'].strip() == 'CNSHG':
						d['pod']='CNSHA'
					if d['pod'].strip() == 'CNNBO':
						d['pod']='CNNPO'
					#-------------------------------------
					#Swap POD (for all)
					if len(d['pod']) == 5:
						d['pod'] = d['pod'][2:] + d['pod'][:2]
					
					

					#Change CASH to Y (for all)
					if 'term' in d.keys():
						if d['term']=='CASH':
							d['term'] ='Y'
						else:
							d['term'] = 'N'
					else:
						d['term'] ='Y'

					# print (fileTypeIn,fileTypeIn.__str__())
					if fileTypeIn.__str__() == 'MSC Shore File':
						container_long = d['type'][:2]
						container_type = d['type'][2:]
						d['size'] = container_long
						# print (d['type'],len(d['type']),container_long)
						d['long'] =  d['type'][:2]

						if container_type=='DV':
							d['type'] = 'DV'
							# d['high'] = '8.6'
							# print(d['high'])
							if 'high' in d.keys():
								print ('MSC shore - High data %s' % d['high'])
								
							else:
								print ('MSC shore - No High data - set to 8.6')
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

					# if d['type']=='20DV':
					# 	d['high'] = '9.6'
					# 	d['type'] = 'RE'
					# 	d['size'] = '40'

					if d['type'].upper() == '20GP':
						d['high'] = '8.6'
						d['type'] = 'DV'
						d['size'] = '20'


					# Add by Chutchai on Nov 22,2017
					#if high is not in key , add high
					if not 'high' in d:
						print ('Not found high -- add new to 8.6')
						d['high'] = '8.6'
					#----------------------------------

					# print(d['type'],len(d['type']))
					d['size'] = d['size'].replace('.0','') if '.0' in d['size'] else d['size']
					d['size'] = d['size'].replace('\'','') 

					print (d['high'])
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
					d['temp'] = d['temp'].replace('C','')
					d['temp'] = d['temp'].replace('\'','')		

					# d['vgm'] ='TEXT'			

			# Save to Shore File
			instance = ShoreFile(name=fileInName,filetype=obj,filename=request.FILES['file'],status='D')
			instance.save()
			vSlug = instance.slug
			# print (dict_list)
		else:
			return None
	else:
		form = UploadFileForm()
		dict_list = None
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
		'slug': vSlug
		})