from django.http import HttpResponse
from django.shortcuts import render

import logging

logger = logging.getLogger(__name__)

    
def logging(request):
    error = 'security'
    logger.info(f"Error causer due to {error} User accessed my_view.")
    logger.warning("Potential issue detected.")
    logger.error("Something went wrong!")

    # Render the HTML template index.html with the data in the context variable
    return HttpResponse('All Good')

