import sys, os
from psRestUtilities import *

def getData ( recordLimit ):
	
	psPlanOutput, t, status = getRest( psPlanUrl, session, payload, requestHeader, authorization, recordLimit, log )

	psPlanIdList = getPsPlanId( psPlanOutput, log )	

	for p in psPlanIdList:
		plan = p['PlanId']
		log.info( 'Plan: %s' % ( p.values() ) )
		planUrl = getUrl ( url, rootResource, str( plan ) )
		planDetails, t, status = getRest( planUrl, session, payload, requestHeader, authorization, None, log )
		filename = str( plan ) + '.' + rootResource
		writeCsv ( [planDetails], filename, outDir )
		log.info('\t\tStatusCode: %s\t%5s Records \t%s sec \t%s' % (status, ( len( [ planDetails ] )), t, rootResource))
		for r in resources:
			toUrl = getUrl ( url, rootResource, str( plan ), 'child', r )
			#print ( toUrl )
			restOutput, t, status = getRest ( toUrl, session, payload, requestHeader, authorization, recordLimit, log )
			filename = str( plan ) + '.' + r
			if restOutput[ 'items' ]:
				log.info('\t\tStatusCode: %s\t%5s Records \t%s sec \t%s' % (status, ( len( restOutput[ 'items' ] )), t, r))
				writeCsv ( restOutput[ 'items' ], filename, outDir )
			else:
				log.info('\t\tStatusCode: %s\t%5s Records \t%s sec \t%s' % ( status, '-', t, r ) )
		log.info('\n')


if __name__ == "__main__":
	
	log = setLogging()
	variables = setVariables('psRest.xml')
	outDir = variables['psOutputDirectory']
	inputDir = variables['psInputDirectory']
	resourceList = variables['resourceList']
	rootResource = variables['rootResource']
	recordLimit = variables['recordLimit']
	url = variables['url']
	planId = variables['planId']
	resFile = os.path.join(inputDir, resourceList)
	resources = getResources( resFile )
	username = variables['user']
	password = variables['password']
	
	session, authorization, requestHeader, payload = scmAuth ( username, password )
	
	log.info('REST Server: %s' % ( url ))
	psPlanUrl = getUrl( url, rootResource)
	
	getData( recordLimit )


	
