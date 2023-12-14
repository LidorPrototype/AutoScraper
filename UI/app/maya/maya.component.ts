import { Component, Inject, Optional } from '@angular/core';
import { UntypedFormBuilder, Validators } from '@angular/forms';
import { DatePipe } from '@angular/common'
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { MatDialog, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ScheduleDialogComponent } from '../schedule-dialog/schedule-dialog.component';

@Component({
  selector: 'app-maya',
  templateUrl: './maya.component.html',
  styleUrls: ['./maya.component.css']
})
export class MayaComponent {
  mayaForm = this.fb.group({
    serviceType: [null],
    engName: [null, Validators.required],
    hebName: [null, Validators.required],
    dFrom: [null, Validators.required],
    dTo: [null, Validators.required],
    format: [null]
  });
  disableBtn = false;
  loader = false;
  dataToSchedule:any = null;
  showSchedule = true;
  serviceType = 'PDF';
  currentUrl = '';
  submited = false;
  values = [];
  formats = [
    {name: 'HTML', value: 'html', disable: false },
    {name: 'JSON', value: 'json', disable: false },
    {name: 'CSV', value: 'csv', disable: true}
  ];
  defaultTabIndex = 0;
  hideSchedule: boolean = false;
  preData = {
    "DAG_Name": "",
    "DestinationID": "",
    "PartitionKey": "",
    "RowKey": "",
    "cron": "",
    "description": "",
    "start_date": "",
    "end_date": "",
    "output_name": "",
    "serviceID": "",
    "status": "",
    "user": "",
  }

  constructor(private fb: UntypedFormBuilder,public datepipe: DatePipe,private http: HttpClient, public dialog: MatDialog, @Inject(MAT_DIALOG_DATA) @Optional() public data: any) {
    if (data != null && data.Parameters.length > 0) {
      this.mayaForm.controls['serviceType'].setValue(data.Parameters[0].parameterValue.replace(/"/g, ''));
      this.serviceType = data.Parameters[0].parameterValue.replace(/"/g, '');
      this.mayaForm.controls['engName'].setValue(data.Parameters[1].parameterValue.replace(/"/g, ''));
      this.mayaForm.controls['hebName'].setValue(data.Parameters[2].parameterValue.replace(/"/g, ''));
      this.mayaForm.controls['dFrom'].setValue(new Date(data.Parameters[3].parameterValue.replace(/"/g, '')));
      this.mayaForm.controls['dTo'].setValue(new Date(data.Parameters[4].parameterValue.replace(/"/g, '')));
      this.mayaForm.controls['format'].setValue(data.Parameters[5].parameterValue.replace(/"/g, ''));
      switch (this.mayaForm.controls['serviceType'].value) {
        case 'pdf':
        case 'Pdf':
        case 'PDF':
          this.defaultTabIndex = 0;
          break;
        case 'html':
        case 'Html':
        case 'HTML':
          this.defaultTabIndex = 1;
          break;
      }
      this.preData["DAG_Name"] = data.DAG_Name;
      this.preData["DestinationID"] = data.DestinationID;
      this.preData["PartitionKey"] = data.PartitionKey;
      this.preData["RowKey"] = data.RowKey;
      this.preData["cron"] = data.cron;
      this.preData["description"] = data.description;
      this.preData["start_date"] = data.start_date;
      this.preData["end_date"] = data.end_date;
      this.preData["output_name"] = data.output_name;
      this.preData["serviceID"] = data.serviceID;
      this.preData["status"] = data.status;
      this.preData["user"] = data.user;
      this.hideSchedule = data.hideSchedule;
    }
  }

  addValue(){}
  

  SetServiseType($event: any){
    if($event.index == 0)
      this.serviceType = "PDF";
    else
      this.serviceType = "HTML";
  console.log($event.index);
  console.log("MAYA:", this.mayaForm.value);
  }


  onSubmit(): void {
    this.loader = true;
    this.disableBtn = true;
  try {
    this.loader = true;
    this.mayaForm.value.dFrom = this.datepipe.transform(this.mayaForm.value.dFrom, 'dd-MM-yyyy');
    this.mayaForm.value.dTo = this.datepipe.transform(this.mayaForm.value.dTo, 'dd-MM-yyyy');
    this.mayaForm.value.serviceType = this.serviceType;
    const eng = this.mayaForm.value.engName;
    const heb = this.mayaForm.value.hebName;
    const start = this.mayaForm.value.dFrom;
    const end = this.mayaForm.value.dTo;
    const type = this.mayaForm.value.serviceType;
    const innerf = this.mayaForm.value.format==null?'html':this.mayaForm.value.format;
    this.currentUrl = "service_type="+this.serviceType+"&eng_report="+eng+"&heb_report="+heb+"&start_date="+start+"&end_date="+end+"&inner_format="+innerf;
    console.log("innerf: ",innerf);
    console.log("mayaForm: ",this.mayaForm.value);
    const requestBody = {
      "maya_model": {
        "service_type": this.serviceType,
        "eng_report": eng,
        "heb_report": heb,
        "start_date": start,
        "end_date": end,
        "inner_format": innerf
      }
    }
    const reqUrl = "https://<INSERT DOMAIN NAME>.azurewebsites.net/post_maya";
    const headers = { 'accept': 'application/json', 'content-type': 'application/json'}  
    const body=JSON.stringify(requestBody);
    this.dataToSchedule = body;
    console.log(body)
    this.http.post(reqUrl, body, {'headers':headers, responseType: 'arraybuffer'}  
    ).subscribe((response: any) => {
      this.downLoadFile(response, innerf,eng);
      this.loader = false;
    });
      this.disableBtn = false;
  } catch (error) {
    this.loader = false;
  }
    this.submited = true;
  }

  openSchedule(){
    let dialogResult = this.dialog.open(ScheduleDialogComponent,{width:'600px',data:{parameters:this.dataToSchedule, serviceID:2, preData:this.preData}});
    dialogResult.afterClosed().subscribe(result => {
      console.log(`result from dialog:`,result);
    })
  }

SendRequest(){
  if (true) {
    console.log(this.mayaForm.value);
    alert("Request Sent To IT Team");
  }
}


 downLoadFile(data: any, type: string, name:string) {
  this.loader = false;
  console.log(data);
  let blob = new Blob([data], {
      type: this.createFileType(type),
  });
  const a = document.createElement('a');
  const objectUrl = URL.createObjectURL(blob)
  a.href = objectUrl
  a.download = name;
  a.click();
  URL.revokeObjectURL(objectUrl);
  this.showSchedule = false;
}
 
createFileType(e: any): string {
  let fileType: string = "";
  if (e == 'csv') {
    fileType = 'application/csv';
  }
  if(e == 'html' || e == 'json' || e == 'pdf'){
    fileType = 'application/x-zip-compressed';
  }
  console.log("fileType: ",fileType);
  return fileType;
}

}
