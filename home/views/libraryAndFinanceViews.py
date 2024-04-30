from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..externalModuleApis import financeModuleApis

@login_required
def all_invoices(request):
  invoices = financeModuleApis.get_student_invoices(request.user.user_id)
  return render(request ,"finance/invoices.html", {'invoices':invoices})

@login_required
def libraryAccountInfo(request):
  messages.info(request, "Check you library information")
  return render(request, "library/libraryInfo.html")

@login_required
def graduation_status(request):
  eligible = True
  notEligible = False
  std_info = financeModuleApis.get_student_info(request.user.user_id)
  print(std_info)
  if std_info['hasOutstandingBalance'] == True:
    eligible = False
    notEligible = True

  params ={"eligible":eligible, "notEligible":notEligible}
  return render(request, "finance/graduationStatus.html", params)